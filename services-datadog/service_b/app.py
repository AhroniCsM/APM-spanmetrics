# Datadog tracing imports - must be first
import ddtrace.auto
from ddtrace import tracer

from flask import Flask, request, jsonify
import logging
import time
import os
import requests

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Service configuration
SERVICE_PORT = int(os.getenv('SERVICE_PORT', 5001))
SERVICE_X_URL = os.getenv('SERVICE_X_URL', 'http://service-x:5003')
SERVICE_T_URL = os.getenv('SERVICE_T_URL', 'http://service-t:5004')

# Track incoming traffic for analysis
traffic_log = []

@app.route('/receive', methods=['POST'])
def receive_request():
    """Receive and log all incoming traffic for analysis"""
    try:
        data = request.get_json()
        source = data.get('source', 'unknown')
        message = data.get('message', '')
        timestamp = data.get('timestamp', time.time())
        
        # Log the incoming traffic
        traffic_entry = {
            "source": source,
            "message": message,
            "timestamp": timestamp,
            "received_at": time.time(),
            "service": "service-b"
        }
        
        traffic_log.append(traffic_entry)
        
        logger.info(f"Service B received traffic from {source}: {message}")
        logger.info(f"Total traffic received: {len(traffic_log)} requests")
        
        if source == 'service-k':
            try:
                x_response = requests.post(f"{SERVICE_X_URL}/receive", json=data, timeout=5)
                logger.info(f"Forwarded to Service X: {x_response.status_code}")
            except Exception as e:
                logger.error(f"Failed to forward to Service X: {str(e)}")
        elif source == 'service-j':
            try:
                t_response = requests.post(f"{SERVICE_T_URL}/receive", json=data, timeout=5)
                logger.info(f"Forwarded to Service T: {t_response.status_code}")
            except Exception as e:
                logger.error(f"Failed to forward to Service T: {str(e)}")
        
        # Keep only last 100 entries to prevent memory issues
        if len(traffic_log) > 100:
            traffic_log.pop(0)
        
        return jsonify({
            "status": "received",
            "service": "service-b",
            "message": f"Traffic logged from {source}",
            "traffic_count": len(traffic_log)
        }), 200
        
    except Exception as e:
        logger.error(f"Service B error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/traffic', methods=['GET'])
def get_traffic():
    """Get traffic analysis data"""
    logger.info("Service B traffic analysis requested")
    return jsonify({
        "service": "service-b",
        "total_requests": len(traffic_log),
        "recent_traffic": traffic_log[-10:] if traffic_log else [],
        "sources": list(set(entry["source"] for entry in traffic_log)) if traffic_log else []
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    logger.info("Service B health check requested")
    return jsonify({"status": "healthy", "service": "service-b"})

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    logger.info("Service B root endpoint accessed")
    return jsonify({
        "service": "service-b",
        "description": "Central routing service for traffic distribution",
        "status": "running",
        "traffic_received": len(traffic_log)
    })

if __name__ == '__main__':
    logger.info(f"Service B starting on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)