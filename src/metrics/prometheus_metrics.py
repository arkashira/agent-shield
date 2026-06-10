from prometheus_client import start_http_server, Gauge, Counter, Histogram

class PrometheusMetrics:
    def __init__(self):
        self.tool_call_latency = Histogram('tool_call_latency_seconds', 'Tool call latency in seconds')
        self.memory_usage = Gauge('memory_usage_bytes', 'Memory usage in bytes')
        self.error_rate = Counter('error_rate_total', 'Error rate total')
        self.request_count = Counter('request_count_total', 'Request count total')
        self.successful_calls = Counter('successful_calls_total', 'Successful calls total')
        self.failed_calls = Counter('failed_calls_total', 'Failed calls total')
        self.average_response_time = Gauge('average_response_time_seconds', 'Average response time in seconds')
        self.cpu_usage = Gauge('cpu_usage_percent', 'CPU usage in percent')
        self.disk_usage = Gauge('disk_usage_percent', 'Disk usage in percent')
        self.network_traffic = Gauge('network_traffic_bytes', 'Network traffic in bytes')

    def start(self):
        start_http_server(8000)

prometheus_metrics = PrometheusMetrics()