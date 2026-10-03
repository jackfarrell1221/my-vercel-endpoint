import json
import math
import os
from typing import List
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Email"] = "jackfarrell2006@gmail.com"
    return response

# Read data from data.json
data_path = os.path.join(os.path.dirname(__file__), "data.json")
try:
    with open(data_path, "r") as f:
        DATA = json.load(f)
except Exception:
    DATA = []

class MetricsRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

def percentile(data: List[float], p: float) -> float:
    if not data:
        return 0.0
    s_data = sorted(data)
    k = (len(s_data) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s_data[int(k)]
    d0 = s_data[int(f)] * (c - k)
    d1 = s_data[int(c)] * (k - f)
    return d0 + d1

@app.post("/")
@app.post("/api")
@app.post("/api/index")
def get_metrics(req: MetricsRequest):
    results = {}
    for region in req.regions:
        region_data = [d for d in DATA if d["region"] == region]
        if not region_data:
            results[region] = {
                "avg_latency": 0.0,
                "p95_latency": 0.0,
                "avg_uptime": 0.0,
                "breaches": 0
            }
            continue
            
        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]
        
        avg_latency = sum(latencies) / len(latencies)
        avg_uptime = sum(uptimes) / len(uptimes)
        p95_latency = percentile(latencies, 0.95)
        breaches = sum(1 for l in latencies if l > req.threshold_ms)
        
        results[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }
    return {"regions": results}
