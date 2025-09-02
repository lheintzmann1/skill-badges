"""
Vercel API endpoint to list available badges
Usage: /api/list
"""

from http.server import BaseHTTPRequestHandler
import json
from .badge_utils import VercelBadgeGenerator


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Initialize badge generator
            generator = VercelBadgeGenerator()
            
            # Get all available badges
            available_badges = generator.get_available_badges()
            
            # Prepare response data
            response_data = {
                "total": len(available_badges),
                "badges": sorted(available_badges),
            }
            
            # Set response headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'public, max-age=3600')  # Cache for 1 hour
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Send JSON response
            json_response = json.dumps(response_data, indent=2)
            self.wfile.write(json_response.encode('utf-8'))
            
        except Exception as e:
            # Error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({"error": str(e)})
            self.wfile.write(error_response.encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
