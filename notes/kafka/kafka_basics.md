# Apache Kafka Basics

## What is Apache Kafka?

Apache Kafka is a distributed event streaming platform designed to handle high-throughput, fault-tolerant, and scalable data streams in real-time. Originally developed by LinkedIn and open-sourced in 2011, Kafka has become the de facto standard for building real-time data pipelines and streaming applications.

## Core Concepts

### 1. Topics
- **Definition**: A category or feed name to which records are published
- **Characteristics**:
  - Topics are partitioned and replicated across multiple brokers
  - Each topic has a configurable retention period
  - Topics are immutable logs of events
- **Naming**: Use descriptive names like `user-events`, `payment-transactions`, `sensor-data`

### 2. Partitions
- **Purpose**: Enable parallelism and scalability
- **Key Points**:
  - Each topic is divided into one or more partitions
  - Partitions are ordered, immutable sequences of records
  - Each record gets a unique offset within its partition
  - Partitions are distributed across brokers
- **Ordering**: Messages within a partition are strictly ordered, but not across partitions

### 3. Brokers
- **Definition**: Kafka servers that store and serve data
- **Responsibilities**:
  - Store topic partitions
  - Handle client requests (produce/consume)
  - Participate in partition leadership
  - Replicate data across the cluster
- **Cluster**: Multiple brokers form a Kafka cluster

### 4. Producers
- **Role**: Applications that publish records to Kafka topics
- **Key Features**:
  - Can specify partition key for routing
  - Support batching for efficiency
  - Configurable acknowledgment levels
  - Can be synchronous or asynchronous

### 5. Consumers
- **Role**: Applications that subscribe to topics and process records
- **Characteristics**:
  - Pull-based model (consumers pull from brokers)
  - Track their position using offsets
  - Can replay messages by resetting offsets
  - Support parallel processing through consumer groups

### 6. Consumer Groups
- **Purpose**: Enable horizontal scaling and fault tolerance
- **How it works**:
  - Multiple consumers can belong to the same consumer group
  - Each partition is consumed by only one consumer in a group
  - If a consumer fails, its partitions are reassigned to other consumers
  - Different consumer groups can independently consume the same topic

## Kafka Architecture

```
Producer A ----\
Producer B -----+--> [Topic: user-events]
Producer C ----/     Partition 0: [msg1, msg2, msg3, ...]
                     Partition 1: [msg4, msg5, msg6, ...]
                     Partition 2: [msg7, msg8, msg9, ...]
                              |
                              v
Consumer Group 1:     Consumer X (P0, P1)
                     Consumer Y (P2)

Consumer Group 2:     Consumer Z (P0, P1, P2)
```

## Key Features

### 1. Durability and Persistence
- All messages are persisted to disk
- Configurable retention policies (time-based or size-based)
- Data is replicated across multiple brokers
- Survives broker failures

### 2. Scalability
- Horizontal scaling by adding more brokers
- Partition-level parallelism
- Linear scaling for both producers and consumers

### 3. High Throughput
- Optimized for high-volume data streams
- Batch processing capabilities
- Zero-copy data transfer
- Efficient serialization

### 4. Low Latency
- Sub-millisecond latency possible
- Real-time data processing
- Streaming capabilities

## Message Structure

```json
{
  "offset": 12345,
  "timestamp": "2025-06-29T10:30:00Z",
  "key": "user_123",
  "value": {
    "user_id": "user_123",
    "action": "login",
    "timestamp": "2025-06-29T10:30:00Z",
    "metadata": {...}
  },
  "headers": {
    "source": "web-app",
    "version": "1.0"
  }
}
```

## Common Use Cases

### 1. Event Sourcing
- Store all changes as a sequence of events
- Rebuild application state from events
- Audit trails and compliance

### 2. Real-time Analytics
- Stream processing with Kafka Streams or Apache Spark
- Real-time dashboards and monitoring
- Anomaly detection

### 3. Data Integration
- Connect different systems and databases
- ETL/ELT pipelines
- Data lake ingestion

### 4. Microservices Communication
- Asynchronous communication between services
- Event-driven architectures
- Service decoupling

### 5. Log Aggregation
- Centralized logging from multiple services
- Log analysis and monitoring
- Distributed tracing

## Kafka Ecosystem

### Core Components
- **Kafka Broker**: Core messaging system
- **Zookeeper**: Coordination service (being phased out by KRaft)
- **Kafka Connect**: Data integration framework
- **Kafka Streams**: Stream processing library
- **Schema Registry**: Schema management for data serialization

### Tools and Utilities
- **Kafka CLI Tools**: Command-line utilities for administration
- **Kafka Manager/UI**: Web-based management interfaces
- **Kafka Rest Proxy**: RESTful interface to Kafka

## Configuration Basics

### Producer Configuration
```properties
bootstrap.servers=localhost:9092
key.serializer=org.apache.kafka.common.serialization.StringSerializer
value.serializer=org.apache.kafka.common.serialization.StringSerializer
acks=all
retries=Integer.MAX_VALUE
```

### Consumer Configuration
```properties
bootstrap.servers=localhost:9092
group.id=my-consumer-group
key.deserializer=org.apache.kafka.common.serialization.StringDeserializer
value.deserializer=org.apache.kafka.common.serialization.StringDeserializer
auto.offset.reset=earliest
```

## Best Practices

### 1. Topic Design
- Use meaningful topic names
- Plan partition count based on expected throughput
- Consider data retention requirements
- Use appropriate replication factor (usually 3)

### 2. Producer Best Practices
- Use appropriate serialization format (Avro, JSON, Protobuf)
- Implement proper error handling
- Use message keys for partitioning when order matters
- Batch messages for better throughput

### 3. Consumer Best Practices
- Handle duplicate messages (idempotent processing)
- Commit offsets appropriately
- Monitor consumer lag
- Implement proper exception handling

### 4. Operational Best Practices
- Monitor cluster health and performance
- Plan for capacity and scaling
- Implement proper security measures
- Regular backup and disaster recovery planning

## Common Pitfalls to Avoid

1. **Not considering partition count**: Too few partitions limit parallelism
2. **Ignoring consumer lag**: Can indicate performance issues
3. **Poor key selection**: Can lead to partition skew
4. **Not handling rebalancing**: Can cause message processing delays
5. **Inadequate monitoring**: Makes troubleshooting difficult

## Getting Started Commands

### Start Kafka (using Docker Compose)
```bash
# Start Zookeeper and Kafka
docker-compose up -d

# Create a topic
docker exec kafka kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

# List topics
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Produce messages
docker exec -it kafka kafka-console-producer --topic test-topic --bootstrap-server localhost:9092

# Consume messages
docker exec -it kafka kafka-console-consumer --topic test-topic --from-beginning --bootstrap-server localhost:9092
```

## Learning Resources

- **Official Documentation**: [kafka.apache.org](https://kafka.apache.org/documentation/)
- **Confluent Platform**: Enhanced Kafka distribution with additional tools
- **Kafka Streams Documentation**: For stream processing applications
- **Books**: "Kafka: The Definitive Guide" by Gwen Shapira et al.

---

This foundation should prepare you for building robust streaming applications with Kafka. The key is to start simple and gradually incorporate more advanced features as your understanding grows.