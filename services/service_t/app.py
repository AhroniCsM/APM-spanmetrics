from flask import Flask, request, jsonify
import logging
import time
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Service configuration
SERVICE_PORT = int(os.getenv('SERVICE_PORT', 5004))

# Track incoming traffic
traffic_log = []

@app.route('/receive', methods=['POST'])
def receive_request():
    """Receive and log incoming traffic from Service B"""
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
            "service": "service-t"
        }
        
        traffic_log.append(traffic_entry)
        
        logger.info(f"Service T received traffic from {source}: {message}")
        logger.info(f"Total traffic received: {len(traffic_log)} requests")
        
        # Keep only last 50 entries to prevent memory issues
        if len(traffic_log) > 50:
            traffic_log.pop(0)
        
        return jsonify({
            "status": "received",
            "service": "service-t",
            "message": f"Traffic processed from {source}",
            "traffic_count": len(traffic_log)
        }), 200
        
    except Exception as e:
        logger.error(f"Service T error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/traffic', methods=['GET'])
def get_traffic():
    """Get traffic data"""
    logger.info("Service T traffic data requested")
    return jsonify({
        "service": "service-t",
        "total_requests": len(traffic_log),
        "recent_traffic": traffic_log[-5:] if traffic_log else [],
        "sources": list(set(entry["source"] for entry in traffic_log)) if traffic_log else []
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    logger.info("Service T health check requested")
    return jsonify({"status": "healthy", "service": "service-t"})

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    logger.info("Service T root endpoint accessed")
    return jsonify({
        "service": "service-t",
        "description": "Receives traffic from Service B (routed from Service J)",
        "status": "running",
        "traffic_received": len(traffic_log)
    })

if __name__ == '__main__':
    logger.info(f"Service T starting on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False) 