# Snowflake Basics

## What is Snowflake?

Snowflake is a cloud-native data warehouse platform that provides a complete solution for data warehousing, data lakes, data engineering, data science, and data application development. It's built from the ground up for the cloud and separates compute from storage.

## Core Architecture

### Multi-Cluster Shared Data Architecture

Snowflake's unique architecture consists of three main layers:

#### 1. Database Storage Layer
- **Centralized Storage**: All data is stored in a centralized location
- **Cloud Storage**: Uses cloud storage (AWS S3, Azure Blob, GCP Storage)
- **Automatic Management**: Snowflake manages all aspects of data storage
- **Columnar Format**: Data stored in compressed, columnar format
- **Immutable**: Data files are immutable and encrypted

#### 2. Query Processing Layer (Compute)
- **Virtual Warehouses**: Independent compute clusters
- **Auto-scaling**: Can scale up/down based on workload
- **Multi-cluster**: Multiple clusters can access same data simultaneously
- **Isolation**: Each warehouse operates independently
- **Pay-per-use**: Only pay for compute time used

#### 3. Cloud Services Layer
- **Metadata Management**: Stores metadata about databases, tables, users
- **Query Optimization**: Handles query parsing and optimization
- **Security**: Authentication, authorization, encryption
- **Transaction Management**: ACID compliance
- **Infrastructure Management**: Automatic maintenance and updates

## Key Features

### Performance Features
- **Automatic Query Optimization**: Self-tuning query optimizer
- **Result Caching**: Automatic caching of query results
- **Micro-partitioning**: Automatic data partitioning
- **Clustering**: Automatic and manual clustering options
- **Materialized Views**: Pre-computed query results

### Scalability Features
- **Elastic Scaling**: Scale compute resources up/down instantly
- **Multi-cluster Warehouses**: Handle concurrent users
- **Automatic Scaling**: Auto-suspend and auto-resume
- **Near-unlimited Storage**: Scales to petabytes

### Data Sharing & Collaboration
- **Secure Data Sharing**: Share data without copying
- **Data Marketplace**: Access third-party data
- **Cross-cloud Sharing**: Share across different cloud providers
- **Real-time Data Sharing**: Live data access

### Security Features
- **End-to-End Encryption**: Data encrypted at rest and in transit
- **Role-based Access Control**: Granular permission management
- **Multi-factor Authentication**: Enhanced security
- **Network Policies**: IP whitelisting and restrictions
- **Private Connectivity**: VPC/VNet integration

## Snowflake Objects Hierarchy

```
Account
├── Organizations
├── Databases
│   ├── Schemas
│   │   ├── Tables
│   │   ├── Views
│   │   ├── Stored Procedures
│   │   ├── User-Defined Functions
│   │   ├── Sequences
│   │   └── File Formats
│   └── Stages (Internal/External)
├── Warehouses
├── Users
├── Roles
└── Resource Monitors
```

## Virtual Warehouses

### Sizes and Specifications
- **X-Small**: 1 node, 8 credits/hour
- **Small**: 2 nodes, 16 credits/hour
- **Medium**: 4 nodes, 32 credits/hour
- **Large**: 8 nodes, 64 credits/hour
- **X-Large**: 16 nodes, 128 credits/hour
- **2X-Large**: 32 nodes, 256 credits/hour
- **3X-Large**: 64 nodes, 512 credits/hour
- **4X-Large**: 128 nodes, 1024 credits/hour

### Warehouse Features
- **Auto-suspend**: Automatically suspend after inactivity
- **Auto-resume**: Automatically resume when queries submitted
- **Multi-cluster**: Scale out to handle concurrency
- **Resource Monitors**: Set spending limits and alerts

## Data Types

### Numeric Types
- `NUMBER` - Fixed-point numbers
- `DECIMAL/NUMERIC` - Alias for NUMBER
- `INT/INTEGER` - Whole numbers
- `BIGINT` - Large integers
- `SMALLINT` - Small integers
- `TINYINT` - Tiny integers
- `BYTEINT` - Single byte integers
- `FLOAT/DOUBLE` - Floating-point numbers
- `REAL` - Single-precision floating-point

### String Types
- `VARCHAR` - Variable-length string (up to 16MB)
- `CHAR/CHARACTER` - Fixed-length string
- `STRING` - Alias for VARCHAR
- `TEXT` - Alias for VARCHAR
- `BINARY` - Binary data
- `VARBINARY` - Variable-length binary

### Date/Time Types
- `DATE` - Date values
- `TIME` - Time values
- `TIMESTAMP` - Date and time values
- `TIMESTAMP_LTZ` - Timestamp with local timezone
- `TIMESTAMP_NTZ` - Timestamp without timezone
- `TIMESTAMP_TZ` - Timestamp with timezone

### Semi-structured Types
- `VARIANT` - JSON-like data
- `OBJECT` - Key-value pairs
- `ARRAY` - Ordered list of values

### Boolean/Geography
- `BOOLEAN` - True/false values
- `GEOGRAPHY` - Geospatial data

## Key Concepts

### Micro-partitions
- Automatic data partitioning (50-500MB compressed)
- Immutable and encrypted
- Contain metadata for pruning
- Enable efficient query processing

### Time Travel
- Query historical data (up to 90 days)
- Restore accidentally deleted data
- Compare changes over time
- Available for tables, schemas, databases

### Zero-Copy Cloning
- Create instant copies without duplicating data
- Clone databases, schemas, or tables
- Independent metadata, shared underlying data
- Useful for testing and development

### Fail-safe
- Additional data protection beyond Time Travel
- 7-day period after Time Travel expires
- Only Snowflake can recover data
- No user access to Fail-safe data

## Loading Data

### Methods
1. **Bulk Loading**
   - COPY command
   - Snowpipe (continuous loading)
   - Third-party ETL tools

2. **Continuous Loading**
   - Snowpipe with cloud messaging
   - Auto-ingest from cloud storage
   - Near real-time data ingestion

3. **Programming Interfaces**
   - Snowflake Connector for Python
   - Snowflake Connector for Spark
   - JDBC/ODBC drivers

### Stages
- **Internal Stages**: Snowflake-managed storage
- **External Stages**: Customer cloud storage
- **User/Table Stages**: Convenient for small files

## Best Practices

### Performance Optimization
- Right-size virtual warehouses
- Use clustering for large tables
- Implement proper data modeling
- Monitor query performance
- Use result caching effectively

### Cost Optimization
- Auto-suspend warehouses
- Use appropriate warehouse sizes
- Monitor credit usage
- Implement resource monitors
- Consider multi-cluster warehouses for concurrency

### Security Best Practices
- Implement role-based access control
- Use service accounts for applications
- Enable MFA for users
- Regular access reviews
- Network security policies

### Data Management
- Organize data in logical databases/schemas
- Use appropriate data types
- Implement data retention policies
- Regular monitoring and maintenance
- Document data lineage

## Common SQL Extensions

### Snowflake-specific Functions
- `PARSE_JSON()` - Parse JSON strings
- `FLATTEN()` - Convert arrays/objects to rows
- `TRY_CAST()` - Safe type conversion
- `LISTAGG()` - String aggregation
- `QUALIFY` - Window function filtering

### Semi-structured Data
```sql
-- Query JSON data
SELECT data:name::string as name
FROM json_table;

-- Flatten arrays
SELECT value
FROM table, LATERAL FLATTEN(input => array_column);
```

## Editions and Pricing

### Editions
- **Standard**: Basic features, 1-day Time Travel
- **Enterprise**: Advanced features, 90-day Time Travel
- **Business Critical**: Enhanced security, compliance
- **Virtual Private Snowflake**: Dedicated environment

### Pricing Model
- **Compute**: Pay for virtual warehouse usage (credits)
- **Storage**: Pay for data stored (monthly)
- **Data Transfer**: Cross-region/cloud charges
- **Cloud Services**: Included up to 10% of compute usage

## Integration Capabilities

### ETL/ELT Tools
- Informatica, Talend, Matillion
- dbt (data build tool)
- Fivetran, Stitch
- AWS Glue, Azure Data Factory

### BI Tools
- Tableau, Power BI, Looker
- Qlik, Sisense
- Native connectors available

### Programming Languages
- Python, Java, .NET
- JavaScript (stored procedures)
- Scala, R support

This covers the fundamental concepts of Snowflake. Each topic can be explored in much greater depth depending on specific use cases and requirements.