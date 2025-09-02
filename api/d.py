"""
Vercel API endpoint for dynamic badge grids (future implementation)
Usage: /api/d?c=python,react,nodejs&perline=3
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
            
            # For now, dynamic badges work the same as static
            # Future enhancements could include:
            # - Real-time stats from GitHub/npm/etc
            # - User-specific badge collections
            # - Custom colors/themes
            # - Badge analytics
            
            # Parse badge names from query
            badge_names = generator.parse_badges_from_query(badge_query)
            
            if not badge_names:
                svg_content = generator.generate_error_svg("Dynamic badges: ?c=python,react,nodejs&perline=4")
            else:
                # Generate badge grid (same as static for now)
                svg_content = generator.generate_badge_grid_svg(badge_names, per_line)
            
            # Set response headers
            self.send_response(200)
            self.send_header('Content-Type', 'image/svg+xml')
            self.send_header('Cache-Control', 'public, max-age=300')  # Shorter cache for dynamic
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Send SVG content
            self.wfile.write(svg_content.encode('utf-8'))
            
        except Exception as e:
            # Error response
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error generating dynamic badges: {str(e)}'.encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
