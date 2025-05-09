from fastapi import FastAPI
from google.cloud import bigquery
import os

app = FastAPI()

client = bigquery.Client()

@app.get("/datos")
def leer_datos():
    query = """
        SELECT * FROM `cyberstage.challenge.raw_events`
        ORDER BY timestamp DESC
        LIMIT 10
    """
    query_job = client.query(query)
    resultados = [dict(row) for row in query_job.result()]
    return resultados
