from prometheus_client import Counter, Histogram, start_http_server
from src.utils.telemetry import monitor_latency, REQUEST_COUNT, start_telemetry_server
import time

REQUEST_COUNT = Counter("api_requests_total", "Total number of API requests")
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Latency of API requests")

# cycle time monitoring
def monitor_latency(func):
    """Decorator to monitor latency of functions."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency)
        return result
    return wrapper

# Prometheus start server
def start_telemetry_server(port=8001):
    """Start the Prometheus telemetry server."""
    start_http_server(port)
    print(f"Telemetry server running on http://localhost:{port}/metrics")

# Telemetry
@monitor_latency
async def analyze_repo(repo_url: str):
    REQUEST_COUNT.inc()  
    # logic
    pass

# start telemetry from main
if __name__ == "__main__":
    start_telemetry_server(port=8001)
    asyncio.run(main())

