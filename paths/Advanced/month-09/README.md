# Month 09 — Distributed Systems

Master event-driven architectures and real-time processing.

---

## Why It Matters

Modern AI systems operate in real-time with massive data streams. Understanding distributed messaging, event-driven architectures, and stream processing is essential for building responsive, scalable AI applications. This month covers the infrastructure that powers real-time ML.

---

## Prerequisites

- Month 08: MLOps (Kubernetes, deployment)
- Month 07: Data Engineering (pipelines, Spark)
- Understanding of distributed systems concepts
- Experience with message queues helpful

---

## Learning Goals

Based on your selected stack, this month focuses on:

### Tier 3 Focus
- **Kafka**: Event streaming platform
- **RabbitMQ**: Message broker
- **Kinesis**: AWS streaming service
- **Azure Stream Analytics**: Real-time analytics
- **EventBridge**: AWS event bus

### Concepts
- Event-driven architecture
- Pub/sub patterns
- Stream processing
- Event sourcing
- CQRS (Command Query Responsibility Segregation)
- Exactly-once semantics
- Backpressure handling

---

## Main Project: Real-Time ML System

Build a real-time ML prediction system with event streaming.

### Deliverables

1. **Kafka Infrastructure**
   - Cluster setup
   - Topic design
   - Producer/consumer patterns
   - Schema registry

2. **Stream Processing**
   - Real-time feature engineering
   - Window operations
   - Aggregations
   - Join patterns

3. **Real-Time ML**
   - Online prediction service
   - Feature freshness
   - Low-latency inference
   - Result streaming

4. **Event-Driven Architecture**
   - Event sourcing
   - Service communication
   - Error handling
   - Dead letter queues

### Definition of Done

- [ ] Kafka processes 10K+ messages/second
- [ ] Stream processing computes features in real-time
- [ ] ML predictions delivered within 100ms
- [ ] System handles failures gracefully
- [ ] Event replay capability works
- [ ] Documentation covers architecture patterns

---

## Stretch Goals

- [ ] Add Kinesis as alternative stream
- [ ] Implement CQRS pattern
- [ ] Build event replay system
- [ ] Add Azure Stream Analytics job
- [ ] Create multi-region setup

---

## Weekly Breakdown

### Week 1: Kafka Fundamentals
- Kafka architecture
- Producers and consumers
- Partitioning strategy
- Schema management

### Week 2: Stream Processing
- Kafka Streams / Flink intro
- Window operations
- Stateful processing
- Real-time aggregations

### Week 3: Event-Driven ML
- Real-time feature engineering
- Online inference
- Event sourcing for ML
- Handling late data

### Week 4: Production Patterns
- Multi-service communication
- Error handling
- Monitoring streams
- Documentation

---

## Claude Prompts

### Planning
```
/plan-week — I'm in Month 9 focusing on distributed systems. Help me plan a week learning Kafka and event streaming.
```

### Building
```
As the Builder agent, help me set up a Kafka cluster and design topics for an ML inference system.
```

### Stream Processing
```
As the Builder, help me implement real-time feature engineering using Kafka Streams. I need to compute rolling averages.
```

### Architecture
```
As the Researcher, explain event-driven architecture patterns for ML systems. Include event sourcing and CQRS.
```

### Debugging
```
/debug-learning — My Kafka consumers are lagging behind. How do I diagnose and fix this?
```

---

## How to Publish

### Demo
- Live Kafka message flow
- Real-time dashboard
- Stream processing visualization
- Failure recovery demo

### Write-up Topics
- Why event streaming for ML
- Kafka architecture explained
- Real-time feature engineering
- Lessons from production streaming

---

## Resources

### Documentation
- [Apache Kafka Docs](https://kafka.apache.org/documentation/)
- [RabbitMQ Docs](https://www.rabbitmq.com/documentation.html)
- [AWS Kinesis Docs](https://docs.aws.amazon.com/kinesis/)
- [Confluent Platform](https://docs.confluent.io/)

### Papers
- "Kafka: a Distributed Messaging System for Log Processing"
- "The Log: What every software engineer should know"

### Tools
- Apache Kafka
- Kafka Connect
- Schema Registry
- AKHQ (Kafka UI)

---

## Next Month Preview

**Month 10**: Cloud & Scale — Multi-cloud architectures, scaling patterns, and cloud-native ML services.
