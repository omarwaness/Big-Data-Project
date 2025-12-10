# Smart Agriculture IoT Data Pipeline

## Overview

This system is designed to monitor plant health using simulated sensor data. It represents a full-stack big data pipeline that moves data from the edge to actionable insights for the end-user. The pipeline includes preprocessing at the edge, batch storage in HDFS, advanced analytics and machine learning with Apache Spark, and a responsive application layer powered by MongoDB.

## Key Features

- **Edge Computing**: Simulates sensors (Temperature, Humidity, Soil Moisture) and performs initial data cleaning and validation.
- **Big Data Storage**: Utilizes HDFS for robust storage of raw and processed batch data.
- **Advanced Analytics**: Apache Spark jobs handle cleaning, statistics, aggregations, anomaly detection, and disease prediction.
- **Actionable Insights**: Processed data is stored in MongoDB for fast retrieval.
- **User Application**: A web dashboard and API provide real-time alerts (e.g., irrigation needs) and disease risk warnings.

## Architecture

The system consists of four main layers:

1.  **Edge Layer**:

    - Generates simulated data and labels.
    - Performs initial cleaning and feature extraction.
    - Sends verified data to the ingestion pipeline.

2.  **Big Data Layer**:

    - **HDFS**: Stores raw incoming batch files and Spark-cleaned datasets.
    - **Apache Spark**: Runs jobs for ETL, statistical analysis, and Machine Learning tasks.
    - **Kafka** (Optional): Handles streaming data ingestion.

3.  **Storage Layer**:

    - **MongoDB**: Acts as the serving database for the application, storing schemas for sensor readings, predictions, and alerts.

4.  **App Layer**:
    - **Backend**: API services handling data requests and recommendation logic.
    - **Frontend**: A Vite-based web application for visualizing data and receiving notifications.

## Project Structure

```text
project-root/
│
├── edge-layer/
│   ├── sensors/                # Sensor simulators (Temp, Humidity, Soil, etc.)
│   ├── gateway/                # Preprocessing and validation scripts
│   └── requirements.txt
│
├── bigdata-layer/
│   ├── kafka/                  # Kafka configuration and topics
│   ├── hdfs/                   # Raw and processed data storage
│   ├── spark/                  # Spark jobs (Cleaning, ML, Stats) and utils
│   └── notebooks/              # Jupyter notebooks for EDA and experiments
│
├── storage-layer/
│   ├── mongodb/                # MongoDB schemas and seeds
│
├── app-layer/
│   ├── backend/                # API and business logic services
│   ├── frontend/               # Web application (Vite)
│   └── mobile-app/             # (Optional) Mobile application
│
├── infra/                      # Infrastructure configuration
│   ├── docker-compose-all.yml  # Main composition file
│   ├── kubernetes-manifests/   # K8s deployment files
│   └── monitoring/             # Grafana and Prometheus setup
│
└── README.md
```

## Getting Started Edge Layer

### Prerequisites

- Python 3.8+

### Run

The easiest way to spin up the entire stack is using the main Docker Compose file:

Open a terminal and run this command in the root of the project:

```bash
docker compose up --build
```

You should see something like this in the terminal
```bash
✔ Service gateway          Built                                                                                                               13.6s 
 ✔ Service sensors          Built                                                                                                                8.2s 
 ✔ Network bigdata_default  Created                                                                                                              0.6s 
 ✔ Container gateway        Created                                                                                                              1.8s 
 ✔ Container sensors        Created                                                                                                              1.2s 
Attaching to gateway, sensors
gateway  | INFO:     Started server process [1]
gateway  | INFO:     Waiting for application startup.
gateway  | INFO:     Application startup complete.                                                                                                    
gateway  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)                                                                    
sensors  | 🚀 Starting all sensors...
sensors  | 
sensors  | 🌤️   Weather Sender Started...
sensors  | ☁️   Forecast Sensor Started...                                                                                                             
sensors  | 🌱  Soil Sensor Started...
```


This will start HDFS, Spark, MongoDB, and the Application services.

