#!/usr/bin/env python3
"""
Badge Generator - Generates SVG badges from JSON configuration file
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
import argparse


class BadgeGenerator:
    """SVG badge generator"""
    
    def __init__(self, config_file: str = "badges_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        
        # Badge configuration
        self.height = 30
        self.padding = 16
        self.icon_size = 20
        self.text_padding = 12
        self.border_radius = 15
        self.font_size = 14
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] Configuration file '{self.config_file}' not found")
            return {"badges": []}
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parsing error: {e}")
            return {"badges": []}
    
    def calculate_text_width(self, text: str) -> float:
        """Calculate text width for monospace font"""
        # JetBrains Mono bold 14px - tous les caractères font la même largeur
        char_width = 8.4  # Largeur fixe pour JetBrains Mono 14px bold
        return len(text) * char_width
    
    def get_text_color(self, bg_color: str) -> str:
        """Determine text color based on background brightness"""
        # Convert hex to RGB
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
        icon_path = Path("icons") / f"{filename}.svg"
        if not icon_path.exists():
            print(f"[WARNING] Missing icon: {icon_path}")
            return ""
        
        try:
            with open(icon_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract content between <svg> tags
            start_tag = content.find('<svg')
            if start_tag == -1:
                return ""
            
            # Find end of opening svg tag
            tag_end = content.find('>', start_tag)
            if tag_end == -1:
                return ""
            
            # Find closing svg tag
            end_tag = content.rfind('</svg>')
            if end_tag == -1:
                return ""
            
            # Extract content between tags
            svg_content = content[tag_end + 1:end_tag].strip()
            
            return svg_content
            
        except Exception as e:
            print(f"[ERROR] Error loading icon {filename}: {e}")
            return ""
    
    def generate_badge_svg(self, badge_config: Dict[str, str]) -> str:
        """Generate SVG for a badge"""
        filename = badge_config["filename"]
        display_name = badge_config["displayName"]
        color = badge_config["color"]
        
        # Calculate dimensions
        text_width = self.calculate_text_width(display_name)
        total_width = self.padding * 2 + self.icon_size + self.text_padding + text_width
        
        # Text color (same color for icon and text)
        text_color = self.get_text_color(color)
        
        # Text position (properly spaced from icon)
        text_x = self.padding + self.icon_size + self.text_padding + (text_width / 2)
        text_y = self.height / 2 + (self.font_size * 0.35)  # Vertical adjustment
        
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
    
    def generate_all_badges(self, output_dir: str = "badges") -> Dict[str, Any]:
        """Generate all badges"""
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Statistics
        stats = {
            "success": 0,
            "errors": 0,
            "total": len(self.config.get("badges", [])),
            "missing_icons": []
        }
        
        print(f"[INFO] Generating {stats['total']} badges...")
        
        for badge_config in self.config.get("badges", []):
            try:
                filename = badge_config["filename"]
                
                # Check if icon exists
                icon_path = Path("icons") / f"{filename}.svg"
                if not icon_path.exists():
                    stats["missing_icons"].append(filename)
                    stats["errors"] += 1
                    continue
                
                # Generate SVG
                svg_content = self.generate_badge_svg(badge_config)
                
                # Save file
                output_file = output_path / f"{filename}_badge.svg"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                
                stats["success"] += 1
                
                # Progress display
                if stats["success"] % 50 == 0:
                    print(f"[INFO] {stats['success']}/{stats['total']} badges generated...")
                    
            except Exception as e:
                print(f"[ERROR] Error generating badge {badge_config.get('filename', 'unknown')}: {e}")
                stats["errors"] += 1
        
        return stats
    
    def save_report(self, stats: Dict[str, Any], output_file: str = "badges/generation_report.json"):
        """Save generation report"""
        report = {
            "timestamp": Path.cwd().as_posix(),
            "results": {
                "success": stats["success"],
                "errors": stats["errors"],
                "total": stats["total"]
            },
            "configuration": {
                "height": self.height,
                "padding": self.padding,
                "icon_size": self.icon_size,
                "text_padding": self.text_padding,
                "border_radius": self.border_radius
            },
            "missing_icons": stats.get("missing_icons", [])
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="SVG Badge Generator")
    parser.add_argument("--config", default="badges_config.json", help="JSON configuration file")
    parser.add_argument("--output", default="badges", help="Output directory")
    parser.add_argument("--quiet", action="store_true", help="Quiet mode")
    
    args = parser.parse_args()
    
    if not args.quiet:
        print("[INFO] Badge Generator")
        print("=" * 50)
    
    # Initialize generator
    generator = BadgeGenerator(args.config)
    
    if not generator.config.get("badges"):
        print("[ERROR] No badges found in configuration")
        return 1
    
    # Generate all badges
    stats = generator.generate_all_badges(args.output)
    
    # Save report
    generator.save_report(stats, f"{args.output}/generation_report.json")
    
    # Display results
    if not args.quiet:
        print("\nResults:")
        print(f"  Success: {stats['success']}")
        print(f"  Errors: {stats['errors']}")
        print(f"  Total: {stats['total']}")

        if stats["missing_icons"]:
            print(f"\n[WARNING] Missing icons ({len(stats['missing_icons'])}):")
            for icon in stats["missing_icons"][:10]:  # Show first 10
                print(f"    - {icon}.svg")
            if len(stats["missing_icons"]) > 10:
                print(f"    ... and {len(stats['missing_icons']) - 10} more")
        
        print(f"\n[INFO] Badges generated in '{args.output}/' directory")
    
    return 0 if stats["errors"] == 0 else 1


if __name__ == "__main__":
    exit(main())
