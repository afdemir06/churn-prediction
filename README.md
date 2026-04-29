# AI-Powered Customer Churn Prediction System

This project provides an end-to-end machine learning pipeline designed to predict customer churn. It leverages professional-grade preprocessing workflow using Imbalanced-Learn pipelines and Scikit-Learn data preprocessing utils, served via a high-performance FastAPI backend and fully containerized with Docker for seemless deployment.

## Key Features
- **Automated Preprocessing:** Standardized data cleaning and feature engineering using custom Scikit-Learn classes.
- **Scalable Architecture:** Modular design separating the API logic from the machine learning pipeline.
- **Production-Ready:** Fully containerized environment ensuring consistent performance across different operating systems.
- **RESTful API:** Easy-to-integrate endpoints for real-time churn predictions.

## Tech Stack
- **Language:** Python 3.12
- **ML Framework:** Scikit-Learn
- **API Framework:** FastAPI
- **Deployment:** Docker & Docker Compose

## Getting Started
To run this project locally, ensure you have Docker installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/afdemir06/churn-prediction.git
   cd churn-prediction
   ```

2. Start the service using Docker Compose:
    ```bash
    docker-compose up --build
    ```