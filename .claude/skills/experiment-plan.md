# Skill: Experiment Plan

Design and track ML experiments systematically to avoid wasted effort and enable reproducibility.

## Trigger

Use this skill when:
- Comparing multiple model architectures
- Tuning hyperparameters
- Testing different features or data augmentations
- Need to justify why one approach is better

## Prerequisites

- Baseline model established
- Clear evaluation metric
- Experiment tracking tool (MLflow, W&B, or simple CSV)
- Version control for code

## Steps

### 1. Define the Question (10 min)

```markdown
## Experiment: [Name]

**Question**: What are we trying to learn?
**Hypothesis**: What do we expect and why?
**Success Criteria**: How will we know we answered the question?
**Scope**: What's in/out of this experiment?
```

Example:
```markdown
## Experiment: Embedding Model Comparison

**Question**: Which embedding model gives best retrieval accuracy?
**Hypothesis**: OpenAI ada-002 will outperform sentence-transformers
              due to larger training data, but at higher cost.
**Success Criteria**: MRR@10 improvement > 5% justifies cost increase
**Scope**: Compare 3 models, fixed chunking strategy, 1000 doc sample
```

### 2. Design Experiment Matrix (15 min)

```python
from itertools import product

# Define variants to test
experiment_grid = {
    'embedding_model': ['ada-002', 'all-MiniLM-L6-v2', 'bge-base-en'],
    'chunk_size': [256, 512],
    'overlap': [0, 50],
}

# Generate all combinations
experiments = [dict(zip(experiment_grid.keys(), v))
               for v in product(*experiment_grid.values())]

print(f"Total experiments: {len(experiments)}")
for i, exp in enumerate(experiments):
    print(f"  {i+1}. {exp}")
```

### 3. Set Up Tracking (15 min)

```python
import json
from datetime import datetime
from pathlib import Path

class ExperimentTracker:
    def __init__(self, experiment_name):
        self.name = experiment_name
        self.results = []
        self.log_path = Path(f"experiments/{experiment_name}")
        self.log_path.mkdir(parents=True, exist_ok=True)

    def log_run(self, config, metrics, notes=""):
        run = {
            "timestamp": datetime.now().isoformat(),
            "config": config,
            "metrics": metrics,
            "notes": notes
        }
        self.results.append(run)

        # Save incrementally
        with open(self.log_path / "results.jsonl", "a") as f:
            f.write(json.dumps(run) + "\n")

        return run

    def summary(self):
        import pandas as pd
        return pd.DataFrame([
            {**r["config"], **r["metrics"]}
            for r in self.results
        ])

# Usage
tracker = ExperimentTracker("embedding_comparison_v1")
```

### 4. Run Experiments (varies)

```python
for config in experiments:
    print(f"Running: {config}")

    # Set up this variant
    model = load_embedding_model(config['embedding_model'])
    chunks = chunk_documents(docs,
                            size=config['chunk_size'],
                            overlap=config['overlap'])

    # Run evaluation
    embeddings = model.encode(chunks)
    metrics = evaluate_retrieval(embeddings, test_queries)

    # Log results
    tracker.log_run(
        config=config,
        metrics={
            'mrr@10': metrics['mrr'],
            'recall@10': metrics['recall'],
            'latency_ms': metrics['latency'],
            'cost_per_1k': metrics['cost']
        },
        notes="First run, fixed test set"
    )
```

### 5. Analyze Results (20 min)

```python
import pandas as pd

results = tracker.summary()

# Sort by primary metric
results.sort_values('mrr@10', ascending=False, inplace=True)
print("Top 5 configurations:")
print(results.head())

# Statistical significance (if applicable)
from scipy import stats

baseline_results = results[results['embedding_model'] == 'ada-002']['mrr@10']
challenger_results = results[results['embedding_model'] == 'bge-base-en']['mrr@10']

t_stat, p_value = stats.ttest_ind(baseline_results, challenger_results)
print(f"P-value: {p_value:.4f}")
```

### 6. Document Conclusions (15 min)

```markdown
## Experiment Results: Embedding Model Comparison

### Summary
Tested 3 embedding models across 4 chunking configurations (12 total runs).

### Key Findings
1. **bge-base-en** achieved highest MRR@10 (0.78) with 512/50 config
2. **ada-002** was 2nd (0.75) but 10x more expensive
3. **all-MiniLM-L6** was fastest but lowest accuracy (0.68)

### Best Configuration
- Model: bge-base-en
- Chunk size: 512
- Overlap: 50
- MRR@10: 0.78
- Cost: $0.002/1k tokens

### Decision
Proceed with bge-base-en for production. Cost savings justify
slight accuracy trade-off vs. ada-002.

### Next Experiment
Test impact of query expansion on retrieval accuracy.
```

## Artifacts Produced

1. **Experiment Log** — `experiments/{name}/results.jsonl`
2. **Analysis Notebook** — Jupyter notebook with visualizations
3. **Conclusions Document** — Markdown summary
4. **Best Model** — Saved model/config for best variant

## Quality Bar

Your experiment is complete when:

- [ ] Question is clearly stated
- [ ] All variants are defined before running
- [ ] Results are logged consistently
- [ ] Statistical significance considered (if applicable)
- [ ] Conclusions answer the original question
- [ ] Decision is documented and justified
- [ ] Best configuration is saved/reproducible

## Common Pitfalls

1. **No hypothesis** — Running experiments without expectations
2. **Changing metrics mid-experiment** — Invalidates comparisons
3. **p-hacking** — Running until you get the result you want
4. **No baseline** — Can't tell if results are good or bad
5. **Forgetting to log** — Lose track of what you tried

## Experiment Types

### A/B Comparison
Compare two specific approaches directly.

### Grid Search
Exhaustively try all combinations.

### Random Search
Sample from configuration space (often more efficient).

### Ablation Study
Remove components to understand their contribution.

### Sensitivity Analysis
Vary one parameter to understand its impact.
