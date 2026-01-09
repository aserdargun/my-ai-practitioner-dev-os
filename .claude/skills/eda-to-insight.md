# Skill: EDA to Insight

Exploratory Data Analysis workflow for discovering insights and preparing data for modeling.

## Trigger

Use this skill when:
- Starting a new dataset analysis
- Preparing data for a machine learning project
- Looking for patterns, anomalies, or insights
- Validating data quality

## Prerequisites

- Dataset accessible (CSV, database, API)
- Python environment with pandas, numpy, matplotlib/seaborn
- Jupyter notebook or similar environment
- Clear question or objective for exploration

## Steps

### 1. Data Loading and First Look (15 min)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('data.csv')

# First look
print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nBasic stats:\n{df.describe()}")
```

### 2. Data Quality Assessment (20 min)

```python
# Missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
print(f"Missing values:\n{missing[missing > 0]}")

# Duplicates
duplicates = df.duplicated().sum()
print(f"\nDuplicate rows: {duplicates}")

# Data types check
for col in df.columns:
    unique = df[col].nunique()
    print(f"{col}: {unique} unique values ({df[col].dtype})")
```

### 3. Univariate Analysis (30 min)

For each important column:

```python
# Numerical columns
for col in df.select_dtypes(include=[np.number]).columns:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Distribution
    df[col].hist(bins=50, ax=axes[0])
    axes[0].set_title(f'{col} Distribution')

    # Box plot
    df[col].plot(kind='box', ax=axes[1])
    axes[1].set_title(f'{col} Box Plot')

    plt.tight_layout()
    plt.show()

    # Summary stats
    print(f"{col}:")
    print(f"  Mean: {df[col].mean():.2f}")
    print(f"  Median: {df[col].median():.2f}")
    print(f"  Std: {df[col].std():.2f}")
    print(f"  Skew: {df[col].skew():.2f}")

# Categorical columns
for col in df.select_dtypes(include=['object', 'category']).columns:
    print(f"\n{col} value counts:")
    print(df[col].value_counts().head(10))
```

### 4. Bivariate Analysis (30 min)

```python
# Correlation matrix (numerical)
corr = df.select_dtypes(include=[np.number]).corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.show()

# Key relationships
# Scatter plots for highly correlated pairs
high_corr = np.where(np.abs(corr) > 0.5)
for i, j in zip(*high_corr):
    if i < j:
        col1, col2 = corr.columns[i], corr.columns[j]
        print(f"{col1} vs {col2}: {corr.iloc[i, j]:.2f}")
```

### 5. Target Variable Analysis (if applicable, 20 min)

```python
# For classification
if df['target'].dtype == 'object' or df['target'].nunique() < 20:
    print(df['target'].value_counts(normalize=True))

# For regression
else:
    df['target'].hist(bins=50)
    plt.title('Target Distribution')
    plt.show()
```

### 6. Document Insights (20 min)

Create a summary of findings:
- Key statistics
- Data quality issues found
- Interesting patterns
- Recommended next steps
- Questions for stakeholders

## Artifacts Produced

1. **EDA Notebook** — Jupyter notebook with all analysis
2. **Data Quality Report** — Summary of missing values, duplicates, anomalies
3. **Insights Document** — Key findings and recommendations
4. **Visualization Gallery** — Important plots saved as images

## Quality Bar

Your EDA is complete when:

- [ ] Every column has been examined
- [ ] Missing values are quantified and explained
- [ ] Distributions are understood (skew, outliers)
- [ ] Key relationships are identified
- [ ] Target variable is characterized (if applicable)
- [ ] Data quality issues are documented
- [ ] Insights are written in plain language
- [ ] Next steps are recommended

## Common Pitfalls

1. **Skipping the "why"** — Always connect findings to business context
2. **Ignoring missing patterns** — Missing data often isn't random
3. **Correlation ≠ causation** — Be careful with interpretations
4. **Outlier reflexes** — Don't remove outliers without understanding them
5. **Tunnel vision** — Look at the data from multiple angles

## Examples

### Sample Insight Summary

```markdown
## EDA Summary: Customer Churn Dataset

### Key Findings
1. **Class imbalance**: 85% retained, 15% churned
2. **Strong predictors**: tenure (r=-0.35), monthly charges (r=0.19)
3. **Data quality**: 2% missing in TotalCharges (correlates with new customers)

### Concerns
- Tenure highly skewed (many new customers)
- Some features are proxies for each other (multicollinearity)

### Recommendations
1. Address class imbalance in modeling (SMOTE or class weights)
2. Create tenure buckets for interpretability
3. Check with business: is TotalCharges missing = $0 or unknown?
```
