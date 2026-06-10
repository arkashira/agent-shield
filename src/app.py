from flask import Flask
from src.metrics.prometheus_metrics import prometheus_metrics

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    return prometheus_metrics._collector_registry.generate_latest().decode()

if __name__ == '__main__':
    prometheus_metrics.start()
    app.run(port=8080)