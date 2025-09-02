"""
Vercel API endpoint for static badge grids
Usage: /api/s?c=python,react,nodejs&perline=3
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from .badge_utils import VercelBadgeGenerator


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse URL and query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Get badges from 'c' parameter
            badge_query = query_params.get('c', [''])[0]
            
            # Get per line parameter (default: 4)
            try:
                per_line = int(query_params.get('perline', ['4'])[0])
                per_line = max(1, min(per_line, 20))  # Limit between 1-20
            except (ValueError, IndexError):
                per_line = 4
            
            # Initialize badge generator
            generator = VercelBadgeGenerator()
            
            # Parse badge names from query
            badge_names = generator.parse_badges_from_query(badge_query)
            
            if not badge_names:
                # Show available badges as example
                available = generator.get_available_badges()[:20]  # First 20 as example
                example_badges = ','.join(available[:8])
                svg_content = generator.generate_error_svg(f"Usage: ?c={example_badges}&perline=4")
            else:
                # Generate badge grid
                svg_content = generator.generate_badge_grid_svg(badge_names, per_line)
            
            # Set response headers
            self.send_response(200)
            self.send_header('Content-Type', 'image/svg+xml')
            self.send_header('Cache-Control', 'public, max-age=3600')  # Cache for 1 hour
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Send SVG content
            self.wfile.write(svg_content.encode('utf-8'))
            
        except Exception as e:
            # Error response
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error generating badges: {str(e)}'.encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
