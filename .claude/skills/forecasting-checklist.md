# Skill: Forecasting Checklist

Time series forecasting workflow from data preparation to model evaluation.

## Trigger

Use this skill when:
- Predicting future values of a time-indexed series
- Building demand forecasting, sales prediction, or capacity planning
- Working with temporal patterns (seasonality, trends)

## Prerequisites

- Time series data with consistent frequency
- Clear forecast horizon (how far ahead)
- Understanding of business context
- Python with pandas, numpy, statsmodels/prophet/etc.

## Steps

### 1. Data Preparation (30 min)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load and parse dates
df = pd.read_csv('data.csv', parse_dates=['date'])
df = df.set_index('date').sort_index()

# Check frequency
print(f"Date range: {df.index.min()} to {df.index.max()}")
print(f"Frequency: {pd.infer_freq(df.index)}")

# Handle missing timestamps
full_range = pd.date_range(df.index.min(), df.index.max(), freq='D')
df = df.reindex(full_range)
print(f"Missing values after reindex: {df.isnull().sum()}")

# Fill or interpolate missing values
df = df.interpolate(method='time')
```

### 2. Visual Exploration (20 min)

```python
fig, axes = plt.subplots(3, 1, figsize=(14, 10))

# Full series
df['value'].plot(ax=axes[0], title='Full Time Series')

# Seasonal decomposition
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(df['value'], period=7)  # weekly
decomposition.plot()
plt.tight_layout()
plt.show()

# Autocorrelation
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))
plot_acf(df['value'], lags=50, ax=ax1)
plot_pacf(df['value'], lags=50, ax=ax2)
plt.show()
```

### 3. Train/Test Split (10 min)

```python
# Time series split (no shuffle!)
train_size = int(len(df) * 0.8)
train = df.iloc[:train_size]
test = df.iloc[train_size:]

print(f"Train: {train.index.min()} to {train.index.max()} ({len(train)} points)")
print(f"Test: {test.index.min()} to {test.index.max()} ({len(test)} points)")

# For walk-forward validation
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
```

### 4. Baseline Models (30 min)

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_forecast(y_true, y_pred, name="Model"):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    print(f"{name}: MAE={mae:.2f}, RMSE={rmse:.2f}, MAPE={mape:.1f}%")
    return {'mae': mae, 'rmse': rmse, 'mape': mape}

# Naive: last value
naive_pred = np.full(len(test), train['value'].iloc[-1])
evaluate_forecast(test['value'], naive_pred, "Naive (last value)")

# Seasonal naive: same day last week
seasonal_naive = train['value'].iloc[-7:].values
seasonal_naive_pred = np.tile(seasonal_naive, len(test)//7 + 1)[:len(test)]
evaluate_forecast(test['value'], seasonal_naive_pred, "Seasonal Naive")

# Moving average
ma_window = 7
ma_pred = train['value'].rolling(ma_window).mean().iloc[-1]
ma_pred = np.full(len(test), ma_pred)
evaluate_forecast(test['value'], ma_pred, f"MA({ma_window})")
```

### 5. Statistical Models (45 min)

```python
# ARIMA
from statsmodels.tsa.arima.model import ARIMA

# Fit ARIMA (order selection via AIC or manual)
arima_model = ARIMA(train['value'], order=(1, 1, 1))
arima_fit = arima_model.fit()
arima_pred = arima_fit.forecast(steps=len(test))
evaluate_forecast(test['value'], arima_pred, "ARIMA(1,1,1)")

# Exponential Smoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing

hw_model = ExponentialSmoothing(
    train['value'],
    seasonal_periods=7,
    trend='add',
    seasonal='add'
)
hw_fit = hw_model.fit()
hw_pred = hw_fit.forecast(len(test))
evaluate_forecast(test['value'], hw_pred, "Holt-Winters")
```

### 6. ML Models (Optional, 45 min)

```python
# Feature engineering for ML
def create_features(df):
    df = df.copy()
    df['dayofweek'] = df.index.dayofweek
    df['month'] = df.index.month
    df['lag_1'] = df['value'].shift(1)
    df['lag_7'] = df['value'].shift(7)
    df['rolling_mean_7'] = df['value'].rolling(7).mean()
    return df

train_feat = create_features(train).dropna()
test_feat = create_features(pd.concat([train.tail(7), test])).iloc[7:]

feature_cols = ['dayofweek', 'month', 'lag_1', 'lag_7', 'rolling_mean_7']

# LightGBM or XGBoost
from sklearn.ensemble import GradientBoostingRegressor

gb_model = GradientBoostingRegressor(n_estimators=100)
gb_model.fit(train_feat[feature_cols], train_feat['value'])
gb_pred = gb_model.predict(test_feat[feature_cols])
evaluate_forecast(test['value'], gb_pred, "Gradient Boosting")
```

### 7. Model Selection and Validation (20 min)

```python
# Walk-forward validation for fair comparison
def walk_forward_validation(train, test, model_fn, step=7):
    predictions = []
    actuals = []

    for i in range(0, len(test), step):
        # Train on all available data
        train_window = pd.concat([train, test.iloc[:i]])

        # Predict next step
        model = model_fn(train_window)
        pred = model.forecast(min(step, len(test) - i))

        predictions.extend(pred)
        actuals.extend(test['value'].iloc[i:i+step])

    return np.array(actuals), np.array(predictions)

# Compare models with walk-forward
models = {
    'ARIMA': lambda x: ARIMA(x['value'], order=(1,1,1)).fit(),
    'HW': lambda x: ExponentialSmoothing(x['value'],
                                         seasonal_periods=7,
                                         trend='add',
                                         seasonal='add').fit()
}

for name, model_fn in models.items():
    actuals, preds = walk_forward_validation(train, test, model_fn)
    evaluate_forecast(actuals, preds, f"{name} (Walk-Forward)")
```

### 8. Document Results (15 min)

```markdown
## Forecasting Results

### Best Model: Holt-Winters

**Performance (Walk-Forward Validation)**:
- MAE: 45.2
- RMSE: 62.1
- MAPE: 8.3%

**Why this model**:
- Captures weekly seasonality well
- Stable across validation windows
- Simple to deploy and interpret

**Limitations**:
- Struggles with holiday effects
- May need retraining monthly
```

## Artifacts Produced

1. **Clean Dataset** — Preprocessed time series data
2. **Model Comparison** — Results table for all models
3. **Best Model** — Serialized model file
4. **Forecast Visualization** — Actuals vs. predictions plot
5. **Documentation** — Model selection rationale

## Quality Bar

Your forecasting is complete when:

- [ ] Data is clean and at consistent frequency
- [ ] Naive baselines are computed
- [ ] Multiple models compared fairly
- [ ] Walk-forward or time-series CV used
- [ ] Best model is selected with rationale
- [ ] Forecast uncertainty is understood
- [ ] Model is saved and reproducible

## Common Pitfalls

1. **Random train/test split** — Always split temporally
2. **Look-ahead bias** — Using future data in features
3. **Ignoring seasonality** — Check for daily, weekly, yearly patterns
4. **Overfitting to recent data** — Validate on multiple windows
5. **Point forecasts only** — Include prediction intervals
