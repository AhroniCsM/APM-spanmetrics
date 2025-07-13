from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Service configuration
SERVICE_X_URL = os.getenv('SERVICE_X_URL', 'http://service-x:5003')
SERVICE_T_URL = os.getenv('SERVICE_T_URL', 'http://service-t:5004')
SERVICE_PORT = int(os.getenv('SERVICE_PORT', 5001))

@app.route('/forward', methods=['POST'])
def forward_request():
    """Forward requests based on source service"""
    try:
        data = request.get_json()
        source = data.get('source', 'unknown')

        logger.info(f"Service B received request from {source}")

        if source == 'service-k':
            # Route to Service X
            logger.info(f"Service B forwarding request from {source} to Service X")
            response = requests.post(
                f"{SERVICE_X_URL}/receive",
                json=data,
                timeout=5
            )
            logger.info(f"Service B received response from Service X: {response.status_code}")
            return jsonify({
                "status": "forwarded",
                "from": source,
                "to": "service-x",
                "response": response.json() if response.status_code == 200 else {"error": "Service X error"}
            }), 200

        elif source == 'service-j':
            # Route to Service T
            logger.info(f"Service B forwarding request from {source} to Service T")
            response = requests.post(
                f"{SERVICE_T_URL}/receive",
                json=data,
                timeout=5
            )
            logger.info(f"Service B received response from Service T: {response.status_code}")
            return jsonify({
                "status": "forwarded",
                "from": source,
                "to": "service-t",
                "response": response.json() if response.status_code == 200 else {"error": "Service T error"}
            }), 200

        else:
            logger.warning(f"Service B received request from unknown source: {source}")
            return jsonify({"error": "Unknown source service"}), 400

    except Exception as e:
        logger.error(f"Service B error forwarding request: {str(e)}")
        return jsonify({"error": str(e)}), 500

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
        "description": "Routes traffic from K to X, from J to T",
        "status": "running"
    })

if __name__ == '__main__':
    logger.info(f"Service B starting on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)