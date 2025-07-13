from flask import Flask, jsonify
import requests
import logging
import time
import threading
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Service configuration
SERVICE_B_URL = os.getenv('SERVICE_B_URL', 'http://service-b:5001')
SERVICE_PORT = int(os.getenv('SERVICE_PORT', 5000))

def send_traffic_to_b():
    """Send periodic requests to Service B"""
    while True:
        try:
            logger.info(f"Service K sending request to Service B at {SERVICE_B_URL}")
            response = requests.post(
                f"{SERVICE_B_URL}/forward",
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

        time.sleep(3)  # Send request every 3 seconds

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
        "description": "Generates traffic to Service B",
        "status": "running"
    })

if __name__ == '__main__':
    # Start traffic generation in a separate thread
    traffic_thread = threading.Thread(target=send_traffic_to_b, daemon=True)
    traffic_thread.start()

    logger.info(f"Service K starting on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)