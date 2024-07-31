# Recommendation API

This is a Flask-based API for serving recommendations using a LightFM model. The application is Dockerized for ease of deployment.

## Features:

- **Recommendation Engine**: Provides personalized recommendations using a LightFM model.
- **Dockerized**: Easy deployment with Docker.
- **API Endpoint**: Two different endpoints to get recommendations for old and new users

## Installation

### Clone the Repository

```sh
git clone https://github.com/tarikaytek/insider-case-work.git
cd insider-case-work
```

### Build the Docker Image

```sh
docker build -t my-app
```

### Run the Docker Container
```sh
docker run -p 5000:5000 my-app
```

### If not using Docker
- Clone the repo
- Ensure having Python 3.11
- ```pip install requirements.txt```
- ```py app.py```


## API Usage
Example use of API endpoints is demonstrated in notebooks/example_API_requests.ipynb. 
Visit there for clear explanation and use cases.

## Model Development 
Development process of model is detailed in notebooks/recommendation_system_development.ipynb.
Visit there for EDA of dataset, preprocessing, feature engineering, model development, evaluation and inference steps. 

Sevgiler
Tarık Aytek
tarik.aytek99@gmail.com