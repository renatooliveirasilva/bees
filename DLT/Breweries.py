# Databricks notebook source
# DBTITLE 1,Bronze
import dlt
import requests
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import current_timestamp, col, lower

@dlt.table(
    name="bronze.breweries",
    comment="Raw brewery data loaded from JSON api in bronze zone.",
    cluster_by=["country", "state", "city"],
    table_properties={
        "quality": "bronze"
    }
)
def bronze_brewery_data():
    response = requests.get("https://api.openbrewerydb.org/v1/breweries")

    if response.status_code == 200:
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

        df = spark.createDataFrame(response.json(), schema=schema) \
            .withColumn("_ingestion", current_timestamp())
    else:
        print(f"Erro na requisição: {response.status_code}")

    return df
            

# COMMAND ----------

# DBTITLE 1,Silver
@dlt.table(
    name="silver.breweries",
    comment="Curated and partitioned brewery data.",
    partition_cols=["country", "state", "city"],
    table_properties={
        "quality": "silver"
    }
)
@dlt.expect_or_fail("valid_id", "id IS NOT NULL")
def silver_breweries_clean():
    return dlt.read("bronze.breweries") \
            .select(
                col("id"),
                col("name"),
                lower(col("brewery_type")).alias("type"),
                col("country"),
                col("state"),
                col("state_province"),
                col("city"),
                col("address_1"),
                col("address_2"),
                col("address_3"),
                col("postal_code"),
                col("phone"),
                col("longitude").cast(DoubleType()),
                col("latitude").cast(DoubleType()),
                col("website_url"),
                col("_ingestion")
            )
