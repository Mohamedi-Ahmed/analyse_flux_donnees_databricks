# Databricks notebook source
# MAGIC %md
# MAGIC # 2.1 - Streaming en Temps Réel avec Azure Databricks

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType

import jupyter_black

# COMMAND ----------

jupyter_black.load()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Définition du schéma des données JSON
# MAGIC

# COMMAND ----------

schema = (StructType()
          .add("arrival_time", StringType())
          .add("creation_time", StringType())
          .add("device", StringType())
          .add("index", StringType())
          .add("model", StringType())
          .add("user", StringType())
          .add("gt", StringType())
          .add("x", DoubleType())
          .add("y", DoubleType())
          .add("z", DoubleType()))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lecture d’un flux JSON depuis Databricks Datasets

# COMMAND ----------

df_stream = (spark.readStream
                .format("json")     
                .schema(schema)     
                .load("/databricks-datasets/definitive-guide/data/activity-data"))

# COMMAND ----------

display(df_stream)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transformation : Filtrer les valeurs où "x" est supérieur à 0.5
# MAGIC

# COMMAND ----------

df_filtered = df_stream.filter("x > 0.5")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Écriture des données transformées dans une Delta Table

# COMMAND ----------

df_filtered.writeStream.format("delta").outputMode("append").option("checkpointLocation", "/delta/checkpoints/streaming").start("/delta/streamed_data")

# COMMAND ----------

# MAGIC %md
# MAGIC # 2.2 - Streaming avec Azure Event Hubs
# MAGIC

# COMMAND ----------

# Connexion à Azure Event Hubs
connection_string = ""

df_event_hub = spark.readStream     .format("eventhubs")     .option("eventhubs.connectionString", connection_string)     .load()

# Transformation des données Event Hub
df_transformed = df_event_hub.select(from_json(col("body").cast("string"), schema).alias("data")).select("data.*")

# Écriture dans Delta Table
df_transformed.writeStream     .format("delta")     .outputMode("append")     .option("checkpointLocation", "/delta/checkpoints/eventhub")     .start("/delta/eventhub_data")