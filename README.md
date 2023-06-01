# <p align="center"><strong>TransJakarta Data end-to-end Pipeline</strong><p>
<a target="_blank">[![TransJakarta Mapping](https://github.com/baidlowi/Data-end-to-end-Pipeline/assets/79616397/b2813354-51e0-438e-ab26-ace62ac7f595)](https://transjakarta.co.id/peta-rute/)</a>


## Problem Definition
**A Bus Rapid Transit (BRT) System** is a high-capacity, high-frequency bus system that uses dedicated lanes and stations to provide a fast and efficient alternative to private cars. BRT systems have been shown to be effective in reducing traffic congestion, improving air quality, and increasing access to public transportation.

One city that has implemented a successful BRT system is **Jakarta, Indonesia**. The TransJakarta BRT system was launched in 2004 and has since become one of the most popular modes of transportation in the city. The system currently has over 100 routes and serves over 2 million passengers per day.

The TransJakarta BRT system has been credited with reducing traffic congestion in Jakarta by up to 30%. The system has also helped to improve air quality in the city by reducing the number of cars on the road. In addition, the TransJakarta BRT system has made it easier for people to get around Jakarta, especially those who live in low-income areas.

BRT systems can be a cost-effective way to improve public transportation in a city. The cost of building a BRT system is typically lower than the cost of building a light rail or metro system. In addition, BRT systems can be implemented more quickly than other types of transit systems.

The data collected from buses can be used to improve the efficiency of the busway system in a number of ways. For example, the data can be used to:
- Optimize bus routes: The data can be used to identify the most efficient routes for buses to take. This can help to reduce travel times and improve reliability.
- Improve bus scheduling: The data can be used to improve the scheduling of buses. This can help to ensure that buses are running on time and that there are enough buses to meet demand.
- Identify areas for improvement: The data can be used to identify areas where the busway system can be improved. This information can be used to make changes to the system, such as adding new routes or improving the frequency of service.

## Solution Overview

A data pipeline in this case is a set of processes that are used to collect, process, and store data. By collecting data from a variety of sources point area and storing it in a central location, data pipelines make it easier to access and analyze data. This can help TransJakarta bussiness to make better decisions by providing them with a better understanding of customers, operations, and  markets.

![Batch Data Architechture](https://github.com/baidlowi/Data-end-to-end-Pipeline/assets/79616397/a90e3547-e1e2-4d97-9df9-b2ca77961f8a)
    
### Tools
- **Google Cloud Platform** (GCP): Cloud-based auto-scaling platform by Google
- **Google Cloud Storage** (GCS): Data Lake
- **BigQuery**: Data Warehouse
- **Terraform**: Infrastructure-as-Code (IaC)
- **Docker**: Containerization
- **Prefect**: Workflow Orchestration
- **Apache Spark**: Data Processing and Transformation

***

## Step-by-step Guide

### Part 1: Infrastructure as Code Cloud Resource with Terraform

1. Install `gcloud SDK`, `terraform`, and create a GCP project. 
2. Create a service account with **Storage Admin**, **Storage Pbject Admin**, **BigQuery Admin** role. 
3. Create and Download the JSON credential and store it on `.google/credentials/google_credential.json`
4. Edit `1-Terraform/main.tf` in a text editor, and change `de-1199` with your GCP's project id.
5. Move directory to `1-Terraform` by executing
    ```
    cd 1-Terraform
    ```
6. Initialize Terraform (set up environment and install Google provider)
    ```
    terraform init
    ```
7. Plan Terraform infrastructure creation
    ```
    terraform plan
    ```
8. Create new infrastructure by applying Terraform plan
    ```
    terraform apply
    ```
9. Check GCP console to see newly-created resource `GCS Bucket`, `Big Query Dataset`, and `Virtual Machine`.
    
### Part 2: Run Workflow on Virtual Machine to Scrape, Ingest, and Manipulation Data
1. Go to source directory
    ```
    cd ..
    ```
2. Then, replace `de-1199` in `.env` file to your project ID.

3. Build docker image
    ```
    docker-compose build
    ```
4. Run docker container
    ```
    docker-compose up
    ```

5. Access the Prefect webserver through web browser on [http://localhost:4200](http://localhost:4200)
6. Create block **GCS Bucket** (with name your GCS Bucket) and **GCS Credentials** (from file `google_credential.json`)
6. Run Workflow `etl-to-gcs.py` and schedule it in every night
    ```
    prefect deployment build 2-Prefect Workflow/etl-to-gcs.py:etl_to_gcs -n "Ingest data to GCS"
    ```
    ![image](https://user-images.githubusercontent.com/79616397/230938319-f8cab849-eb08-4fa4-8c43-86b6c89b4b73.png)
    ![image](https://user-images.githubusercontent.com/79616397/230957720-77728d87-2bcd-41cc-82d9-235a6f395852.png)

6. Run prefect agent to start queue schedule
    ```
    prefect agent start --work-queue "default" 
    ```

7. After done, check GCP Console, then both in Google Cloud Storage and BigQuery to check the data.
    ![image](https://github.com/baidlowi/Data-end-to-end-Pipeline/assets/79616397/7c86e73a-f2fb-4273-83b0-98a4b370f354)
 
8. Create folder `code` and upload `spark-to-bigquery.py` to this folder
    
9. Run Spark in shell GCP for loading data to Big Query
    ```
    gcloud dataproc jobs submit pyspark \
    --cluster=cluster-7ec7 \
    --region=us-central1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://data-spark11/code/spark-to-bigquery.py \
    -- \
        --input=gs://data-spark11/data/* \
        --output=databusway.passengerrecords
    ```
 
9. Open Big Query and we can see our data
    ![image](https://github.com/baidlowi/Data-end-to-end-Pipeline/assets/79616397/00e35619-2e26-40b9-bdb8-3eea2a56426e)


### Part 3: Visualize Data
1. Open Looker Website or Tableau Desktop, and connect to BigQuery.
2. Authorize credentials service aaccount from `google_credential.json`
2. Visualize the dashboard and publish to Tableau Public.
    ![image](https://github.com/baidlowi/Data-end-to-end-Pipeline/assets/79616397/84e20830-f775-47d0-8f94-1fd800cef21e)
    > <i>Tableau Public: https://public.tableau.com/app/profile/hasyim2598/viz/TransjakartaPassengers/Dashboard</i>
    
### Part 4: Stopping Project
1. To shut down the project, just stop the docker container
    ```
    docker-compose down
    ```
***

<p align="center"><i>Credit from Data Engineering Zoomcamp by DataTalksClub</i>
<i>https://github.com/DataTalksClub/data-engineering-zoomcamp</i></p>
