# BEES Data Engineering Case
## Open Brewery DB

### 🌟 Overview
This project is a solution to the BEES Data Engineering challenge. The objective was to design and implement a data pipeline to ingest, transform, and serve brewery data using the Medallion architecture (Bronze, Silver, and Gold layers).

## 🚀 Tech Stack
- **Language**: Python (PySpark), SQL
- **Data Lake Storage**: Delta Lake
- **Orchestration**: Databricks Workflows
- **Data Governance & Lineage**: Unity Catalog
- **API Source**: [Open Brewery DB](https://www.openbrewerydb.org/)

## 📃 Architecture
This project follows the Medallion Architecture pattern:

### ✨ Bronze Layer
- **Raw ingestion** of data from the Open Brewery API
- Persisted as-is with minimal processing
- Includes ingestion timestamp for traceability

### 💖 Silver Layer
- Data curation: lowercase normalization, type casting, and filtering null IDs
- Partitioned by location (`country`, `state`, and `city`)

### 🌟 Gold Layer
- Aggregated view brewery counts by `type` and location (`country`, `state`, and `city`)

## 🪨 Monitoring & Data Quality
- **Orchestration Failures**: Handled via Databricks Workflows with built-in retry logic
- **Alerting**: Can be configured through Databricks Jobs UI or integrated with tools like Slack/Email
- **Lineage Tracking**: Enabled by Unity Catalog, tracks data flows across tables
- **Data Quality**: Enabled by Unity Catalog through the Quality (Catalog page)

## 🔹 Additional Implementation - DLT Pipeline
This project includes an **optional implementation** using Delta Live Tables:
- Simplifies deployment and versioning
- Enforces data quality contracts
- Scales seamlessly with Databricks compute
- DLT Expectations: Enforced data expectations using `@dlt.expect_or_fail`
- The implementation can be found in the `DLT` folder.

## 📋 Running the Project
1. Clone the repository or import the `.dbc` files
2. Create a Workflows job with tasks for each layer (bronze, silver, and gold), and attach the corresponding notebooks (you can find a supporting JSON file in the Workflows folder)
3. Run the job

## ✅ Requirements

### Unity Catalog
Ensure the Unity Catalog is configured and enabled in your Databricks workspace.
- Create catalog and schemas manually or via notebook
- Assign appropriate permissions for table creation and lineage

### AWS
The challenge was developed using AWS S3 Bucket as the data storage, you will need to change the `unity_catalog_path` in the bronze notebook if you are using a different cloud service.

### One more thing...

See more details in `complementary_file.pdf`
