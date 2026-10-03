import json
import math
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

DATA = [
  { "region": "apac", "service": "catalog", "latency_ms": 184.44, "uptime_pct": 97.439, "timestamp": 20250301 },
  { "region": "apac", "service": "analytics", "latency_ms": 186.87, "uptime_pct": 98.353, "timestamp": 20250302 },
  { "region": "apac", "service": "checkout", "latency_ms": 190.23, "uptime_pct": 99.012, "timestamp": 20250303 },
  { "region": "apac", "service": "catalog", "latency_ms": 182.11, "uptime_pct": 97.881, "timestamp": 20250304 },
  { "region": "apac", "service": "analytics", "latency_ms": 188.45, "uptime_pct": 98.120, "timestamp": 20250305 },
  { "region": "apac", "service": "checkout", "latency_ms": 191.05, "uptime_pct": 99.155, "timestamp": 20250306 },
  { "region": "apac", "service": "catalog", "latency_ms": 185.33, "uptime_pct": 97.662, "timestamp": 20250307 },
  { "region": "apac", "service": "analytics", "latency_ms": 187.90, "uptime_pct": 98.401, "timestamp": 20250308 },
  { "region": "apac", "service": "checkout", "latency_ms": 189.50, "uptime_pct": 99.005, "timestamp": 20250309 },
  { "region": "apac", "service": "catalog", "latency_ms": 183.99, "uptime_pct": 97.550, "timestamp": 20250310 },
  { "region": "apac", "service": "analytics", "latency_ms": 188.12, "uptime_pct": 98.222, "timestamp": 20250311 },
  { "region": "apac", "service": "checkout", "latency_ms": 190.88, "uptime_pct": 99.110, "timestamp": 20250312 },
  { "region": "emea", "service": "catalog", "latency_ms": 145.22, "uptime_pct": 99.881, "timestamp": 20250301 },
  { "region": "emea", "service": "analytics", "latency_ms": 148.99, "uptime_pct": 99.762, "timestamp": 20250302 },
  { "region": "emea", "service": "checkout", "latency_ms": 151.34, "uptime_pct": 99.991, "timestamp": 20250303 },
  { "region": "emea", "service": "catalog", "latency_ms": 144.11, "uptime_pct": 99.855, "timestamp": 20250304 },
  { "region": "emea", "service": "analytics", "latency_ms": 149.05, "uptime_pct": 99.780, "timestamp": 20250305 },
  { "region": "emea", "service": "checkout", "latency_ms": 150.22, "uptime_pct": 99.950, "timestamp": 20250306 },
  { "region": "emea", "service": "catalog", "latency_ms": 146.33, "uptime_pct": 99.890, "timestamp": 20250307 },
  { "region": "emea", "service": "analytics", "latency_ms": 147.88, "uptime_pct": 99.740, "timestamp": 20250308 },
  { "region": "emea", "service": "checkout", "latency_ms": 152.01, "uptime_pct": 99.988, "timestamp": 20250309 },
  { "region": "emea", "service": "catalog", "latency_ms": 145.80, "uptime_pct": 99.870, "timestamp": 20250310 },
  { "region": "emea", "service": "analytics", "latency_ms": 148.44, "uptime_pct": 99.755, "timestamp": 20250311 },
  { "region": "emea", "service": "checkout", "latency_ms": 151.10, "uptime_pct": 99.995, "timestamp": 20250312 },
  { "region": "amer", "service": "catalog", "latency_ms": 195.66, "uptime_pct": 98.111, "timestamp": 20250301 },
  { "region": "amer", "service": "analytics", "latency_ms": 198.22, "uptime_pct": 98.555, "timestamp": 20250302 },
  { "region": "amer", "service": "checkout", "latency_ms": 210.45, "uptime_pct": 98.777, "timestamp": 20250303 },
  { "region": "amer", "service": "catalog", "latency_ms": 196.12, "uptime_pct": 98.222, "timestamp": 20250304 },
  { "region": "amer", "service": "analytics", "latency_ms": 199.01, "uptime_pct": 98.444, "timestamp": 20250305 },
  { "region": "amer", "service": "checkout", "latency_ms": 211.33, "uptime_pct": 98.888, "timestamp": 20250306 },
  { "region": "amer", "service": "catalog", "latency_ms": 194.88, "uptime_pct": 98.050, "timestamp": 20250307 },
  { "region": "amer", "service": "analytics", "latency_ms": 197.66, "uptime_pct": 98.601, "timestamp": 20250308 },
  { "region": "amer", "service": "checkout", "latency_ms": 209.90, "uptime_pct": 98.750, "timestamp": 20250309 },
  { "region": "amer", "service": "catalog", "latency_ms": 195.40, "uptime_pct": 98.150, "timestamp": 20250310 },
  { "region": "amer", "service": "analytics", "latency_ms": 198.80, "uptime_pct": 98.490, "timestamp": 20250311 },
  { "region": "amer", "service": "checkout", "latency_ms": 212.12, "uptime_pct": 98.665, "timestamp": 20250312 }
]

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
