#Import libraries
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
import argparse


#Define parameters to pass for the main script
#Initiate parser
parser = argparse.ArgumentParser(description='Parameters for main script')

#Definition parser
parser.add_argument('--input', required=True)
parser.add_argument('--output', required=True)

#Capture arguments as variables
args = parser.parse_args()

gcs_input = args.input
output = args.output

#Initialize spark session
spark = SparkSession.builder \
  .appName('End to End Pipeline')\
  .config('spark.jars', 'gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar') \
  .getOrCreate()
  
#Configure temporary bucket
spark.conf.set('temporaryGcsBucket', 'data-spark11-temp')

#Read data from gcs folder
df_data = spark.read.parquet(gcs_input)

#Set Schema for dataframes
schema_data = types.StructType([
    types.StructField('tahun', types.LongType(), True), 
    types.StructField('bulan', types.LongType(), True), 
    types.StructField('jenis', types.StringType(), True), 
    types.StructField('kode_trayek', types.StringType(), True), 
    types.StructField('trayek', types.StringType(), True), 
    types.StructField('jumlah_penumpang', types.LongType(), True)
])

#Read raw data
df = spark.read.option('header','true').schema(schema_data).parquet(gcs_input)

# Saving the data to BigQuery
df.write.format('bigquery') \
  .option('table', output) \
  .mode("overwrite") \
  .save()