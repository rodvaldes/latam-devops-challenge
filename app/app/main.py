from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import bigquery
import os



app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O restringe a ["https://midominio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = bigquery.Client()

@app.get("/datos")
def leer_datos():
    query = """
        SELECT * FROM `cyberstage.challenge.raw_events`
        ORDER BY timestamp DESC
        LIMIT 5
    """
    query_job = client.query(query)
    resultados = [dict(row) for row in query_job.result()]
    return resultados
