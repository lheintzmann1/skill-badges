import { BadgeGenerator } from './badge-generator.js';

export default function handler(req, res) {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    if (req.method !== 'GET') {
        res.status(405).json({ error: 'Method not allowed' });
        return;
    }

    const { c: skills, cols = 4, gap = 8 } = req.query;

    if (!skills) {
        res.status(400).json({ 
            error: 'Skills parameter (c) is required',
            example: '/api/s?c=python,react,nodejs,docker',
            parameters: {
                c: 'Comma-separated list of skill slugs',
                cols: 'Number of columns (default: 4)',
                gap: 'Gap between badges in pixels (default: 8)'
            }
        });
        return;
    }

    // Parse skills from comma-separated string
    const skillsList = skills.split(',').map(skill => skill.trim()).filter(skill => skill);
    
    if (skillsList.length === 0) {
        res.status(400).json({ error: 'At least one skill is required' });
        return;
    }

    const generator = new BadgeGenerator();
    const gridGenerator = new GridGenerator();
    
    // Generate individual badges
    const badges = [];
    for (const skill of skillsList) {
        const icon = generator.getSimpleIcon(skill);
        const displayName = icon ? icon.title : skill;
        const svg = generator.generateBadgeSvg(skill, displayName);
        if (svg) {
            badges.push({
                skill,
                svg,
                width: generator.calculateBadgeWidth(displayName),
                height: generator.height
            });
        }
    }

    if (badges.length === 0) {
        res.status(404).json({ 
            error: 'No valid icons found for provided skills',
            available_icons_endpoint: '/api/list'
        });
        return;
    }

    // Generate grid SVG
    const gridSvg = gridGenerator.generateGrid(badges, parseInt(cols), parseInt(gap));

    // Set SVG content type
    res.setHeader('Content-Type', 'image/svg+xml');
    res.setHeader('Cache-Control', 'public, max-age=86400'); // Cache for 24 hours
    
    res.status(200).send(gridSvg);
}

class GridGenerator {
    generateGrid(badges, cols = 4, gap = 8) {
        if (!badges || badges.length === 0) {
            return null;
        }

        // Calculate grid dimensions
        const rows = Math.ceil(badges.length / cols);
        
        // Find the maximum badge dimensions for consistent spacing
        const maxWidth = Math.max(...badges.map(b => b.width));
        const maxHeight = Math.max(...badges.map(b => b.height));
        
        // Calculate total grid dimensions
        const totalWidth = (maxWidth * cols) + (gap * (cols - 1));
        const totalHeight = (maxHeight * rows) + (gap * (rows - 1));
        
        // Generate SVG
        let svg = `<svg width="${totalWidth}" height="${totalHeight}" viewBox="0 0 ${totalWidth} ${totalHeight}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&amp;display=swap');
    </style>
  </defs>`;

        // Position each badge in the grid
        badges.forEach((badge, index) => {
            const row = Math.floor(index / cols);
            const col = index % cols;
            
            const x = col * (maxWidth + gap);
            const y = row * (maxHeight + gap);
            
            // Center the badge within its allocated space if it's smaller than maxWidth
            const centeredX = x + (maxWidth - badge.width) / 2;
            
            // Extract the content of the badge SVG (everything inside the main <svg> tag)
            const badgeContent = this.extractSvgContent(badge.svg);
            
            svg += `\n  <g transform="translate(${centeredX}, ${y})">
    ${badgeContent}
  </g>`;
        });

        svg += '\n</svg>';
        
        return svg;
    }
    
    extractSvgContent(svgString) {
        // Remove the outer <svg> tag and extract the inner content
        const match = svgString.match(/<svg[^>]*>(.*)<\/svg>/s);
        if (match) {
            return match[1].trim();
        }
        return svgString;
    }
}
