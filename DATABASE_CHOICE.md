# Part 11: Database Selection Justification

## Selected Database: Azure Cosmos DB (NoSQL)

For Lab 1, I have selected **Azure Cosmos DB** using the **NoSQL API** and the **Serverless** capacity mode.

### 1. Architectural Fit (JSON Native)
The `TextAnalyzer` function generates hierarchical data in a JSON format. Azure Cosmos DB is a schema-agnostic database that stores data as documents. This allows the application to save complex analysis objects (word counts, metadata, and timestamps) directly without the need for an Object-Relational Mapping (ORM) layer or a rigid table schema required by SQL databases.

### 2. Cost-Efficiency (Serverless Tier)
Since this is a serverless lab environment, the **Serverless capacity mode** is the most cost-effective choice. Unlike the "Provisioned Throughput" model, which charges an hourly rate regardless of use, the Serverless model only charges for the specific Request Units (RUs) consumed when data is written or read. This ensures the lab costs remain at nearly $0 during periods of inactivity.

### 3. Integration with Azure Functions
Cosmos DB has a native Python SDK (`azure-cosmos`) that integrates seamlessly with Azure Functions. It allows for quick persistence of data using unique IDs (UUIDs) and provides robust querying capabilities for the `GetAnalysisHistory` endpoint using a SQL-like syntax over JSON documents.

### 4. Scalability
As a NoSQL service, Cosmos DB offers horizontal scaling and low-latency performance. This ensures that even if the text being analyzed is significantly large, the database can handle the write operations without becoming a bottleneck for the API.
