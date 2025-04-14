-- Databricks notebook source
-- DBTITLE 1,Create Schema
-- Create the Gold schema if it does not exist
CREATE SCHEMA IF NOT EXISTS bees.gold

-- COMMAND ----------

-- DBTITLE 1,Create View
-- Create the view with aggregated count of breweries by location
CREATE OR REPLACE VIEW bees.gold.breweries_count
COMMENT 'Aggregated brewery counts by location.'
AS
  SELECT type, country, state, city, count(1) as brewery_count
  FROM bees.silver.breweries
  GROUP BY ALL
