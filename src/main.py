import os
import sys
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp

# Import the new API routes
from api_routes import api_bp  # Add this import

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# CORS Configuration - Allow your Vercel frontend
CORS(app, origins=[
    'https://frontend-project-k39t.vercel.app',
    'http://localhost:3000',  # For local development
    'http://localhost:5173'   # For Vite dev server
])

app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(api_bp, url_prefix='/api')  # Add this line

# Database settings
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Health check endpoint at root level
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "AI Content Automation Backend is running",
        "endpoints": {
            "health": "/health",
            "api_health": "/api/health",
            "stats": "/api/stats",
            "channels": "/api/channels",
            "previews": "/api/previews",
            "system_status": "/api/system/status"
        }
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve static files or return API info for root path"""
    if path == "":
        # Return API information when accessing root
        return jsonify({
            "name": "AI Content Automation Backend",
            "status": "running",
            "version": "1.0.0",
            "frontend_url": "https://frontend-project-k39t.vercel.app",
            "api_endpoints": [
                "/health",
                "/api/health",
                "/api/stats", 
                "/api/channels",
                "/api/previews",
                "/api/system/status",
                "/api/system/toggle"
            ]
        })
    
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
        
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({"error": "index.html not found", "requested_path": path}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
