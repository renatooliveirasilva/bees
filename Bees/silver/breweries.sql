-- Databricks notebook source
-- DBTITLE 1,Create Schema
-- Create the Silver schema if it does not exist
CREATE SCHEMA IF NOT EXISTS bees.silver

-- COMMAND ----------

-- DBTITLE 1,Transformation
-- Query data from the Bronze layer
CREATE OR REPLACE TEMPORARY VIEW vw_breweries AS
  SELECT
      id,
      name,
      lower(brewery_type) AS type,
      country,
      state,
      state_province,
      city,
      address_1,
      address_2,
      address_3,
      postal_code,
      phone,
      double(longitude) AS longitude,
      double(latitude) AS latitude,
      website_url,
      _ingestion
  FROM bees.bronze.breweries

-- COMMAND ----------

-- DBTITLE 1,Create table
-- Create the Silver table if it does not already created
-- If the table already exists, only perform the merge in the next step
CREATE TABLE IF NOT EXISTS bees.silver.breweries
USING DELTA
PARTITIONED BY (country, state, city)
TBLPROPERTIES ('quality' = 'silver')
COMMENT "Curated and partitioned brewery data."
AS
  SELECT * FROM vw_breweries

-- COMMAND ----------

-- DBTITLE 1,Merge
-- Merge changes into the Silver table for upsert logic (update or insert based on ID match)
MERGE INTO bees.silver.breweries AS target
USING vw_breweries AS source
    ON target.id = source.id
WHEN MATCHED THEN
  UPDATE SET *
WHEN NOT MATCHED THEN
  INSERT *

-- COMMAND ----------

-- DBTITLE 1,Vaccum and Optimize
-- Vacuum and Optimize the Silver table
VACUUM bees.silver.breweries;
OPTIMIZE bees.silver.breweries
