# Datadog tracing imports - must be first
import ddtrace.auto
from ddtrace import tracer

from flask import Flask, request, jsonify
import logging
import time
import os
import requests
import threading

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Service configuration
SERVICE_PORT = int(os.getenv('SERVICE_PORT', 5000))
SERVICE_B_URL = os.getenv('SERVICE_B_URL', 'http://service-b:5001')

# Track incoming traffic for analysis
traffic_log = []

def send_traffic_to_b():
    while True:
        try:
            logger.info(f"Service K sending request to Service B at {SERVICE_B_URL}")
            response = requests.post(
                f"{SERVICE_B_URL}/receive",
                json={
                    "source": "service-k",
                    "message": f"Request from Service K at {time.time()}",
                    "timestamp": time.time()
                },
                timeout=5
            )
            logger.info(f"Service K received response from Service B: {response.status_code}")
        except Exception as e:
            logger.error(f"Service K failed to send request to Service B: {str(e)}")
        time.sleep(3)

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
            "service": "service-k"
        }
        
        traffic_log.append(traffic_entry)
        
        logger.info(f"Service K received traffic from {source}: {message}")
        logger.info(f"Total traffic received: {len(traffic_log)} requests")
        
        # Forward to Service B
        try:
            b_response = requests.post(f"{SERVICE_B_URL}/receive", json=data, timeout=5)
            logger.info(f"Forwarded to Service B: {b_response.status_code}")
        except Exception as e:
            logger.error(f"Failed to forward to Service B: {str(e)}")
        
        # Keep only last 100 entries to prevent memory issues
        if len(traffic_log) > 100:
            traffic_log.pop(0)
        
        return jsonify({
            "status": "received",
            "service": "service-k",
            "message": f"Traffic logged from {source}",
            "traffic_count": len(traffic_log)
        }), 200
        
    except Exception as e:
        logger.error(f"Service K error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/traffic', methods=['GET'])
def get_traffic():
    """Get traffic analysis data"""
    logger.info("Service K traffic analysis requested")
    return jsonify({
        "service": "service-k",
        "total_requests": len(traffic_log),
        "recent_traffic": traffic_log[-10:] if traffic_log else [],
        "sources": list(set(entry["source"] for entry in traffic_log)) if traffic_log else []
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    logger.info("Service K health check requested")
    return jsonify({"status": "healthy", "service": "service-k"})

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    logger.info("Service K root endpoint accessed")
    return jsonify({
        "service": "service-k",
        "description": "Primary routing service for traffic analysis",
        "status": "running",
        "traffic_received": len(traffic_log)
    })

if __name__ == '__main__':
    traffic_thread = threading.Thread(target=send_traffic_to_b, daemon=True)
    traffic_thread.start()
    logger.info(f"Service K starting on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)