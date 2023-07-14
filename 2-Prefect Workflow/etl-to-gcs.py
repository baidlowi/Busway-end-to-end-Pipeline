from pathlib import Path
import pandas as pd
import os
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
import pyspark
from pyspark.sql.types import *
import argparse

#Define parameters to pass for the main script
#Initiate parser
parser = argparse.ArgumentParser(description='Parameters for main script')
parser.add_argument('--dataset', type=str, help='Dataset in BQ to store table.', required=True)
parser.add_argument('--table', type=str, help='Table name to store output from Spark.', required=True)
#Capture arguments as variables
args = parser.parse_args()
dataset = args.dataset
table = args.bq_table

#@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web into pandas DataFrame"""

    df = pd.read_csv(dataset_url)
    return df

#@task()
def write_local(df: pd.DataFrame, file: str, month:list, year:int) -> Path:
    """Write DataFrame out as parquet file"""
    data_dir = f'destination/'
#    dataset_file = os.rename('Data-Penumpang-Bus-Transjakarta-{month}-{year}.csv', '{month}-{year}.csv')
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    path = Path(f'{data_dir}/{file}.parquet')
    df.to_parquet(path, compression='gzip')
    return path

#@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcp_cloud_storage_bucket_block = GcsBucket.load("de")
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=path, to_path=path)
    

    
#@task(name="run_spark_job", log_prints=True)
def append_bq() -> None:
# Saving the data to BigQuery
    df.write.format('bigquery') \
      .option('table', dataset + '.' + table) \
      .mode('append')\
      .save()

#@flow()
def etl_web_to_gcs(year: int, months: list):
    """The main ETL function"""
    months.sort()
    for month in months:
      file = f'Data-Penumpang-Bus-Transjakarta-{month}-{year}'
      dataset_url = f'https://data.jakarta.go.id/dataset/14ab98731e79939ecaa26ee4222531d2/resource/9f1c2bb6164087f0f0c62b3451e24dd9/download/Data-Penumpang-Bus-Transjakarta-{month}-{year}.csv'

    df = fetch(dataset_url)
#    df = clean(df)
    path = write_local(df, file, month, year)
    write_gcs(path)
    append_bq

if __name__ == '__main__':
    year = 2021
    months = ['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','Oktober','November','Desember']
#    months = ['Januari', 'Februari', 'Maret']

    etl_web_to_gcs(year,months)
