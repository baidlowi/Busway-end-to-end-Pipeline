# <p align="center"><strong>TransJakarta Data end-to-end Pipeline</strong><p>

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

![Untitled (100 × 100 cm)](https://user-images.githubusercontent.com/79616397/230957215-4daeeadb-353e-431e-95df-3243d1a9bfa1.png)

A data pipeline in this case is a set of processes that are used to collect, process, and store data. By collecting data from a variety of sources point area and storing it in a central location, data pipelines make it easier to access and analyze data. This can help TransJakarta bussiness to make better decisions by providing them with a better understanding of customers, operations, and  markets.


### Tools
- **Google Cloud Platform** (GCP): Cloud-based auto-scaling platform by Google
- **Google Cloud Storage** (GCS): Data Lake
- **BigQuery**: Data Warehouse
- **Terraform**: Infrastructure-as-Code (IaC)
- **Docker**: Containerization
- **Prefect**: Workflow Orchestration
- **DBT**: Data Transformation

***

## Step-by-step Guide

### Part 1: Infrastructure as Code Cloud Resource with Terraform

1. Install `gcloud SDK`, `terraform`, and create a GCP project. 
2. Create a service account with **Storage Admin**, **Storage Pbject Admin**, **BigQuery Admin** role. 
3. Create and Download the JSON credential and store it on `.google/credentials/google_credential.json`
4. Edit `1-terraform/main.tf` in a text editor, and change `de-1199` with GCP's project id.
5. Move directory to `1-terraform` by executing
    ```
    cd 1-terraform
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

  
### Part 2: Run Prefect to Scrape, Ingest, and Warehouse Data
1. Go to source directory
    ```
    cd ..
    ```
2. Then, replace `de-1199` in `.env` file to project ID.

3. Build Prefect docker images
    ```
    docker-compose build
    ```
4. Run Prefect docker containers
    ```
    docker-compose up
    ```
5. Access the Prefect webserver through web browser on `localhost:4200` c
6. Create block **GCS Bucket** (with name your GCS Bucket) and **GCS Credentials** (from file `google_credential.json`)
6. Run Workflow `parent-workflow.py` and schedule it in every night
    ```
    prefect deployment build parent-workflow.py:etl_parent_flow -n "Parameterized ETL"
    ```
    ![image](https://user-images.githubusercontent.com/79616397/230938319-f8cab849-eb08-4fa4-8c43-86b6c89b4b73.png)
    ![image](https://user-images.githubusercontent.com/79616397/230957720-77728d87-2bcd-41cc-82d9-235a6f395852.png)

6. Run prefect agent to start queue schedule
    ```
    prefect agent start --work-queue "default" 
    ```

7. After done, check GCP Console, then both in Google Cloud Storage and BigQuery to check the data.

    ![image](https://user-images.githubusercontent.com/79616397/230944184-a4f75913-d9fa-435a-b96b-913ac681b1ca.png)
    ![image](https://user-images.githubusercontent.com/79616397/230944066-989c1113-71dc-4726-927c-4f0d195d2e03.png)


### Part 3: Visualize Data
1. Open Looker Website or Tableau Desktop, and connect to BigQuery.
2. Authorize credentials service aaccount from `google_credential.json`
2. Visualize the dashboard, publish to Public.

![image](https://user-images.githubusercontent.com/79616397/230955196-088a05e8-9d5e-49ec-a67a-404e7f638df0.png)

### Part 4: Stopping Project
1. To shut down the project, just stop the docker container
```
docker-compose down
```

### Data Engineering Zoomcamp by DataTalksClub
https://github.com/DataTalksClub/data-engineering-zoomcamp
