# Skill: Baseline Model and Card

Create a simple baseline model with proper documentation (model card) before attempting complex approaches.

## Trigger

Use this skill when:
- Starting a new ML project
- Need a benchmark to beat with more complex models
- Want to establish "good enough" before optimization
- Documenting a model for production or handoff

## Prerequisites

- Completed EDA (see eda-to-insight.md)
- Clear problem definition (classification/regression/etc.)
- Train/validation/test splits defined
- Evaluation metrics chosen

## Steps

### 1. Define the Problem Clearly (10 min)

```markdown
## Problem Definition

**Task**: [Classification / Regression / Ranking / etc.]
**Target**: [What we're predicting]
**Metric**: [Primary evaluation metric and why]
**Baseline Goal**: [What would be "good enough" for v1]
```

### 2. Create Train/Val/Test Splits (15 min)

```python
from sklearn.model_selection import train_test_split

# First split: separate test set (hold out)
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y  # for classification
)

# Second split: train and validation
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
)

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
```

### 3. Establish Trivial Baselines (15 min)

```python
# For classification
from sklearn.dummy import DummyClassifier

# Always predict most frequent class
dummy_mf = DummyClassifier(strategy='most_frequent')
dummy_mf.fit(X_train, y_train)
print(f"Most frequent baseline: {dummy_mf.score(X_val, y_val):.3f}")

# Random baseline (stratified)
dummy_strat = DummyClassifier(strategy='stratified')
dummy_strat.fit(X_train, y_train)
print(f"Stratified random baseline: {dummy_strat.score(X_val, y_val):.3f}")

# For regression
from sklearn.dummy import DummyRegressor

dummy_mean = DummyRegressor(strategy='mean')
dummy_mean.fit(X_train, y_train)
print(f"Mean baseline MSE: {mean_squared_error(y_val, dummy_mean.predict(X_val)):.3f}")
```

### 4. Build Simple Baseline Model (30 min)

```python
# For classification: Logistic Regression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

baseline_clf = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(max_iter=1000))
])

baseline_clf.fit(X_train, y_train)

# Evaluate
from sklearn.metrics import classification_report, confusion_matrix

y_pred = baseline_clf.predict(X_val)
print(classification_report(y_val, y_pred))
print(confusion_matrix(y_val, y_pred))

# For regression: Linear Regression or Ridge
from sklearn.linear_model import Ridge

baseline_reg = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', Ridge())
])

baseline_reg.fit(X_train, y_train)
```

### 5. Evaluate on Test Set (10 min)

```python
# Final evaluation on held-out test set
y_test_pred = baseline_clf.predict(X_test)
print("Test Set Performance:")
print(classification_report(y_test, y_test_pred))
```

### 6. Save Model and Artifacts (10 min)

```python
import joblib
from datetime import datetime

# Save model
model_path = f"models/baseline_{datetime.now().strftime('%Y%m%d')}.joblib"
joblib.dump(baseline_clf, model_path)

# Save predictions for analysis
pd.DataFrame({
    'y_true': y_test,
    'y_pred': y_test_pred
}).to_csv('outputs/baseline_predictions.csv', index=False)
```

### 7. Write Model Card (30 min)

Create `MODEL_CARD.md`:

```markdown
# Model Card: [Model Name] Baseline

## Model Details
- **Version**: v0.1 (baseline)
- **Date**: YYYY-MM-DD
- **Type**: Logistic Regression
- **Framework**: scikit-learn

## Intended Use
- **Primary use**: [What it's for]
- **Users**: [Who will use it]
- **Out of scope**: [What it shouldn't be used for]

## Training Data
- **Source**: [Where data came from]
- **Size**: [N samples]
- **Date range**: [Time period]
- **Preprocessing**: [Steps applied]

## Evaluation Data
- **Validation set**: [N samples, how selected]
- **Test set**: [N samples, how selected]

## Metrics
| Metric | Trivial Baseline | Model | Improvement |
|--------|------------------|-------|-------------|
| Accuracy | 0.85 | 0.91 | +6% |
| Precision | 0.00 | 0.78 | +78% |
| Recall | 0.00 | 0.65 | +65% |
| F1 | 0.00 | 0.71 | +71% |

## Limitations
- [Known limitations]
- [Failure modes]
- [Biases in data or model]

## Ethical Considerations
- [Potential harms]
- [Fairness considerations]
- [Privacy considerations]

## Caveats and Recommendations
- [When to use]
- [When not to use]
- [Future improvements planned]
```

## Artifacts Produced

1. **Trained Model** — Serialized model file (joblib/pickle)
2. **Model Card** — `MODEL_CARD.md` documentation
3. **Evaluation Report** — Metrics on train/val/test
4. **Predictions** — CSV of test predictions for error analysis

## Quality Bar

Your baseline is complete when:

- [ ] Trivial baselines established (random, majority class, mean)
- [ ] Simple model trained (logistic regression, linear regression, decision tree)
- [ ] Model beats trivial baselines meaningfully
- [ ] Train/val/test splits are proper (no leakage)
- [ ] Model card documents key information
- [ ] Model and artifacts are saved and versioned
- [ ] You know what "good" looks like for this problem

## Common Pitfalls

1. **Skipping trivial baselines** — You need something to compare against
2. **Data leakage** — Test data info leaking into training
3. **Wrong metric** — Accuracy is misleading for imbalanced data
4. **Overcomplicating** — Baseline should be simple
5. **No documentation** — Future you will forget everything

## Examples

### Baseline Performance Table

```
| Model                | Accuracy | F1 (weighted) | Notes           |
|----------------------|----------|---------------|-----------------|
| Most Frequent        | 0.850    | 0.000         | Trivial         |
| Stratified Random    | 0.500    | 0.450         | Trivial         |
| Logistic Regression  | 0.912    | 0.710         | **Baseline**    |
| Random Forest        | 0.935    | 0.780         | Next iteration  |
```
