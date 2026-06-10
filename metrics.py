from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Metrics(BaseModel):
    cpu_usage: float
    memory_usage: float
    request_count: int

class MetricsStore:
    def __init__(self):
        self.metrics = []

    def add_metrics(self, metrics: Metrics):
        self.metrics.append(metrics)

    def get_metrics(self):
        return self.metrics

metrics_store = MetricsStore()

@app.post("/metrics/")
def add_metrics(metrics: Metrics):
    metrics_store.add_metrics(metrics)
    return {"detail": "Metrics added successfully"}

@app.get("/metrics/")
def get_metrics(api_key: Optional[str] = None):
    if not api_key or api_key != "your_api_key":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return metrics_store.get_metrics()