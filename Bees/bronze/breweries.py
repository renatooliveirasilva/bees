# Databricks notebook source
# DBTITLE 1,Libraries
import requests
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import current_timestamp

# COMMAND ----------

# DBTITLE 1,Create Catalog
# Create a catalog in Unity Catalog if it does not already exist
unity_catalog_path = "s3://databricks-workspace-stack-7237d-bucket" #AWS S3 bucket

spark.sql(f"CREATE CATALOG IF NOT EXISTS bees MANAGED LOCATION '{unity_catalog_path}/catalog/bees'")

# COMMAND ----------

# DBTITLE 1,Create Schema
# Create a schema for the Bronze layer if it does not already exist
spark.sql("CREATE SCHEMA IF NOT EXISTS bees.bronze")

# COMMAND ----------

# DBTITLE 1,Define the Schema
# Define the schema manually to ensure consistent reading from the API
schema = StructType([
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("brewery_type", StringType(), True),
    StructField("address_1", StringType(), True),
    StructField("address_2", StringType(), True),
    StructField("address_3", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state_province", StringType(), True),
    StructField("postal_code", StringType(), True),
    StructField("country", StringType(), True),
    StructField("longitude", StringType(), True),
    StructField("latitude", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("website_url", StringType(), True),
    StructField("state", StringType(), True),
    StructField("street", StringType(), True)
])

# COMMAND ----------

# DBTITLE 1,Retrieve and save the data
# Perform API request to Open Brewery DB to retrieve brewery data
response = requests.get("https://api.openbrewerydb.org/v1/breweries")

if response.status_code == 200: # Check if the request was successful
    data = response.json()

    # Convert JSON data to Spark DataFrame using the predefined schema
    df = spark.createDataFrame(data, schema=schema) \
        .withColumn("_ingestion", current_timestamp())

    # Write data in Delta Lake format to the Bronze layer
    df.write.format("delta").mode("overwrite") \
        .clusterBy(["country", "state", "city"]) \
        .saveAsTable("bees.bronze.breweries")

    # Vacuum and optimize the table
    spark.sql("VACUUM bees.bronze.breweries")
    spark.sql("OPTIMIZE bees.bronze.breweries")
