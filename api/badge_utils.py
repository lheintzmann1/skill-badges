"""
Badge Generator Utilities for Vercel API
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import unquote


class VercelBadgeGenerator:
    """SVG badge generator optimized for Vercel"""
    
    def __init__(self):
        # Badge configuration
        self.height = 30
        self.padding = 16
        self.icon_size = 20
        self.text_padding = 12
        self.border_radius = 15
        self.font_size = 14
        
        # Load configuration
        self.config = self.load_config()
        self.badge_map = {badge["filename"]: badge for badge in self.config.get("badges", [])}
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            config_path = Path(__file__).parent.parent / "badges_config.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] Configuration file not found")
            return {"badges": []}
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parsing error: {e}")
            return {"badges": []}
    
    def calculate_text_width(self, text: str) -> float:
        """Calculate text width for monospace font"""
        char_width = 8.4  # JetBrains Mono 14px bold fixed width
        return len(text) * char_width
    
    def get_text_color(self, bg_color: str) -> str:
        """Determine text color based on background brightness"""
        hex_color = bg_color.lstrip('#')
        if len(hex_color) != 6:
            return "#ffffff"
        
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Calculate relative luminance
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            
            # Return white for dark backgrounds, black for light backgrounds
            return "#000000" if luminance > 0.8 else "#ffffff"
        except ValueError:
            return "#ffffff"
    
    def load_icon_svg(self, filename: str) -> str:
        """Load SVG content of the icon"""
        try:
            icon_path = Path(__file__).parent.parent / "icons" / f"{filename}.svg"
            if not icon_path.exists():
                return ""
            
            with open(icon_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract content between <svg> tags
            start_tag = content.find('<svg')
            if start_tag == -1:
                return ""
            
            tag_end = content.find('>', start_tag)
            if tag_end == -1:
                return ""
            
            end_tag = content.rfind('</svg>')
            if end_tag == -1:
                return ""
            
            svg_content = content[tag_end + 1:end_tag].strip()
            return svg_content
            
        except Exception as e:
            print(f"[ERROR] Error loading icon {filename}: {e}")
            return ""
    
    def generate_badge_svg(self, badge_config: Dict[str, str]) -> str:
        """Generate SVG for a single badge"""
        filename = badge_config["filename"]
        display_name = badge_config["displayName"]
        color = badge_config["color"]
        
        # Calculate dimensions
        text_width = self.calculate_text_width(display_name)
        total_width = self.padding * 2 + self.icon_size + self.text_padding + text_width
        
        # Text color
        text_color = self.get_text_color(color)
        
        # Text position
        text_x = self.padding + self.icon_size + self.text_padding + (text_width / 2)
        text_y = self.height / 2 + (self.font_size * 0.35)
        
        # Load icon
        icon_content = self.load_icon_svg(filename)
        
        # SVG template
        svg_template = f'''<svg width="{int(total_width)}" height="{self.height}" viewBox="0 0 {int(total_width)} {self.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&amp;display=swap');
    </style>
  </defs>

  <rect width="{int(total_width)}" height="{self.height}" rx="{self.border_radius}" fill="{color}"/>
  
  <g transform="translate({self.padding}, {(self.height - self.icon_size) / 2}) scale({self.icon_size / 128})" fill="{text_color}">
    {icon_content}
  </g>
  
  <text x="{text_x}" y="{text_y}" font-family="JetBrains Mono, monospace" font-size="{self.font_size}" font-weight="800" fill="{text_color}" text-anchor="middle">{display_name}</text>
</svg>'''
        
        return svg_template
    
    def parse_badges_from_query(self, query_string: str) -> List[str]:
        """Parse badge names from query string"""
        if not query_string:
            return []
        
        # Decode URL encoding
        decoded = unquote(query_string)
        
        # Split by comma and clean up
        badges = [badge.strip().lower() for badge in decoded.split(',') if badge.strip()]
        
        return badges
    
    def get_badge_config(self, badge_name: str) -> Optional[Dict[str, str]]:
        """Get badge configuration by name"""
        return self.badge_map.get(badge_name.lower())
    
    def generate_badge_grid_svg(self, badge_names: List[str], per_line: int = 4) -> str:
        """Generate SVG grid of badges"""
        if not badge_names:
            return self.generate_error_svg("No badges specified")
        
        valid_badges = []
        invalid_badges = []
        
        # Validate and collect badges
        for name in badge_names:
            config = self.get_badge_config(name)
            if config:
                valid_badges.append(config)
            else:
                invalid_badges.append(name)
        
        if not valid_badges:
            error_msg = f"No valid badges found. Invalid: {', '.join(invalid_badges)}"
            return self.generate_error_svg(error_msg)
        
        # Calculate grid dimensions
        badge_margin = 8
        line_spacing = 8
        
        # Generate individual badges and calculate max width per row
        badge_svgs = []
        badge_widths = []
        
        for config in valid_badges:
            badge_svg = self.generate_badge_svg(config)
            badge_svgs.append(badge_svg)
            
            # Extract width from SVG
            width_start = badge_svg.find('width="') + 7
            width_end = badge_svg.find('"', width_start)
            width = int(badge_svg[width_start:width_end])
            badge_widths.append(width)
        
        # Calculate grid layout
        rows = []
        current_row = []
        current_row_widths = []
        
        for i, (svg, width) in enumerate(zip(badge_svgs, badge_widths)):
            current_row.append(svg)
            current_row_widths.append(width)
            
            if len(current_row) == per_line or i == len(badge_svgs) - 1:
                rows.append((current_row.copy(), current_row_widths.copy()))
                current_row = []
                current_row_widths = []
        
        # Calculate total grid dimensions
        max_row_width = 0
        for row_svgs, row_widths in rows:
            row_width = sum(row_widths) + badge_margin * (len(row_widths) - 1)
            max_row_width = max(max_row_width, row_width)
        
        grid_height = len(rows) * self.height + line_spacing * (len(rows) - 1)
        
        # Generate grid SVG
        grid_svg_parts = [f'''<svg width="{max_row_width}" height="{grid_height}" viewBox="0 0 {max_row_width} {grid_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&amp;display=swap');
    </style>
  </defs>''']
        
        current_y = 0
        for row_svgs, row_widths in rows:
            # Calculate starting x position for centering
            row_width = sum(row_widths) + badge_margin * (len(row_widths) - 1)
            start_x = (max_row_width - row_width) / 2
            
            current_x = start_x
            for svg, width in zip(row_svgs, row_widths):
                # Extract the inner content of the badge SVG
                content_start = svg.find('<rect')
                content_end = svg.rfind('</svg>')
                badge_content = svg[content_start:content_end]
                
                # Add the badge content with translation
                grid_svg_parts.append(f'  <g transform="translate({current_x}, {current_y})">')
                grid_svg_parts.append(f'    {badge_content}')
                grid_svg_parts.append('  </g>')
                
                current_x += width + badge_margin
            
            current_y += self.height + line_spacing
        
        grid_svg_parts.append('</svg>')
        
        return '\n'.join(grid_svg_parts)
    
    def generate_error_svg(self, message: str) -> str:
        """Generate an error SVG"""
        text_width = self.calculate_text_width(message)
        total_width = self.padding * 2 + text_width
        
        return f'''<svg width="{int(total_width)}" height="{self.height}" viewBox="0 0 {int(total_width)} {self.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&amp;display=swap');
    </style>
  </defs>

  <rect width="{int(total_width)}" height="{self.height}" rx="{self.border_radius}" fill="#ff4444"/>
  
  <text x="{total_width / 2}" y="{self.height / 2 + (self.font_size * 0.35)}" font-family="JetBrains Mono, monospace" font-size="{self.font_size}" font-weight="800" fill="#ffffff" text-anchor="middle">{message}</text>
</svg>'''

    def get_available_badges(self) -> List[str]:
        """Get list of available badge names"""
        return list(self.badge_map.keys())
    