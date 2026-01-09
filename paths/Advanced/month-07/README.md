# Month 07 — Data Engineering

Build production data pipelines with modern orchestration.

---

## Why It Matters

Data engineering is the backbone of ML systems. Without reliable data pipelines, models can't be trained or deployed effectively. Understanding orchestration, transformation, and distributed processing is essential for any AI practitioner working at scale.

---

## Prerequisites

- Month 06: API Development (Docker, CI/CD basics)
- SQL proficiency
- Python programming
- Understanding of databases (SQL and NoSQL)

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 2 Focus
- **Airflow**: Workflow orchestration
- **Azure Data Factory**: Cloud-native ETL
- **dbt**: Data transformation
- **MLflow**: ML lifecycle management

### Tier 3 Focus
- **Spark**: Distributed data processing
- **Hadoop/Hive**: Big data ecosystem
- **Kafka**: Event streaming

### Concepts
- DAG-based orchestration
- ELT vs ETL patterns
- Data quality and validation
- Idempotency in pipelines
- Backfilling strategies
- Data lineage

---

## Main Project: ML Data Pipeline

Build an end-to-end data pipeline for ML training.

### Deliverables

1. **Airflow DAGs**
   - Data ingestion DAG
   - Transformation DAG
   - Model training trigger
   - Monitoring and alerting

2. **dbt Transformations**
   - Staging models
   - Intermediate transformations
   - Final ML-ready tables
   - Data quality tests

3. **Spark Processing**
   - Large-scale data processing
   - Feature engineering at scale
   - Performance optimization

4. **MLflow Integration**
   - Experiment tracking
   - Model registry
   - Artifact storage

### Definition of Done

- [ ] Airflow DAGs run on schedule
- [ ] dbt models pass all tests
- [ ] Spark job processes 1M+ records efficiently
- [ ] MLflow tracks experiments automatically
- [ ] Pipeline recovers from failures gracefully
- [ ] Documentation covers data lineage

---

## Stretch Goals

- [ ] Add Kafka for real-time data ingestion
- [ ] Implement data quality framework (Great Expectations)
- [ ] Build Azure Data Factory pipeline
- [ ] Create data catalog with metadata
- [ ] Add pipeline cost monitoring

---

## Weekly Breakdown

### Week 1: Airflow Fundamentals
- Airflow architecture
- DAG authoring
- Operators and hooks
- Scheduling and triggers

### Week 2: dbt for Transformations
- dbt project setup
- Model development
- Testing and documentation
- Incremental models

### Week 3: Spark Processing
- Spark fundamentals
- PySpark for data engineering
- Optimizing Spark jobs
- Integration with Airflow

### Week 4: Integration & MLflow
- MLflow setup
- Connecting pipelines
- End-to-end testing
- Documentation and demo

---

## Claude Prompts

### Planning
```
/plan-week — I'm in Month 7 focusing on data engineering. Help me plan a week learning Airflow and building DAGs.
```

### Building
```
As the Builder agent, help me create an Airflow DAG for ML data preparation. Include error handling and retries.
```

### dbt Help
```
As the Builder, help me structure a dbt project for ML feature engineering. Show staging and intermediate models.
```

### Spark
```
As the Builder, help me write a PySpark job for processing large-scale feature data. Optimize for performance.
```

### Debugging
```
/debug-learning — My Airflow DAG keeps failing on the Spark task. How do I debug this?
```

---

## How to Publish

### Demo
- Show Airflow UI with running DAGs
- dbt lineage graph
- Spark job execution
- MLflow experiment tracking

### Write-up Topics
- Why data engineering matters for ML
- Airflow best practices
- dbt for ML pipelines
- Spark optimization tips

---

## Resources

### Documentation
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [dbt Docs](https://docs.getdbt.com/)
- [Apache Spark Docs](https://spark.apache.org/docs/latest/)
- [MLflow Docs](https://mlflow.org/docs/latest/)

### Tutorials
- "Building ML Pipelines with Airflow"
- "dbt for Data Scientists"
- "PySpark Best Practices"

### Tools
- Airflow 2.x
- dbt Core
- PySpark 3.x
- MLflow 2.x

---

## Next Month Preview

**Month 08**: MLOps — Production ML systems with Kubernetes, monitoring, and model deployment at scale.
