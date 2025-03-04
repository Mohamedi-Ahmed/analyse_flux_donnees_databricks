# Databricks Script - Spark Structured Streaming avec Azure Event Hubs & Apache Kafka

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType

# Création de la session Spark
spark = SparkSession.builder.appName("StreamingPipeline").getOrCreate()

# ========================
# 2.1 - Streaming en Temps Réel avec Azure Databricks
# ========================

# Définition du schéma des données JSON
schema = StructType().add("arrival_time", StringType()).add("creation_time", StringType())     .add("device", StringType()).add("index", StringType()).add("model", StringType())     .add("user", StringType()).add("gt", StringType())     .add("x", DoubleType()).add("y", DoubleType()).add("z", DoubleType())

# Lecture d’un flux JSON depuis Databricks Datasets
df_stream = spark.readStream     .format("json")     .schema(schema)     .load("/databricks-datasets/definitive-guide/data/activity-data")

# Transformation : Filtrer les valeurs où "x" est supérieur à 0.5
df_filtered = df_stream.filter("x > 0.5")

# Écriture des données transformées dans une Delta Table
df_filtered.writeStream     .format("delta")     .outputMode("append")     .option("checkpointLocation", "/delta/checkpoints/streaming")     .start("/delta/streamed_data")

# ========================
# 2.2 - Streaming avec Azure Event Hubs
# ========================

# Connexion à Azure Event Hubs (REMPLACE AVEC TA CONNECTION STRING)
connection_string = ""

df_event_hub = spark.readStream     .format("eventhubs")     .option("eventhubs.connectionString", connection_string)     .load()

# Transformation des données Event Hub
df_transformed = df_event_hub.select(from_json(col("body").cast("string"), schema).alias("data")).select("data.*")

# Écriture dans Delta Table
df_transformed.writeStream     .format("delta")     .outputMode("append")     .option("checkpointLocation", "/delta/checkpoints/eventhub")     .start("/delta/eventhub_data")

# ========================
# 3.2 - Streaming avec Apache Kafka
# ========================

# Connexion à Apache Kafka (REMPLACE AVEC TON SERVEUR KAFKA)
df_kafka = spark.readStream     .format("kafka")     .option("kafka.bootstrap.servers", "kafka-broker:9092")     .option("subscribe", "sensor_data")     .option("startingOffsets", "earliest")     .load()

# Transformation des données Kafka
df_kafka_transformed = df_kafka.selectExpr("CAST(value AS STRING) as json")     .select(from_json(col("json"), schema).alias("data")).select("data.*")

# Écriture des données transformées vers un autre topic Kafka
df_kafka_transformed.selectExpr("to_json(struct(*)) AS value")     .writeStream     .format("kafka")     .option("kafka.bootstrap.servers", "kafka-broker:9092")     .option("topic", "processed_data")     .option("checkpointLocation", "/delta/checkpoints/kafka")     .start()
