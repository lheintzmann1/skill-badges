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

    const { icon, name, color } = req.query;

    if (!icon) {
        res.status(400).json({ error: 'Icon parameter is required' });
        return;
    }

    const generator = new BadgeGenerator();
    const displayName = name || icon;
    const svg = generator.generateBadgeSvg(icon, displayName, color);

    if (!svg) {
        res.status(404).json({ 
            error: 'Icon not found',
            available_icons_endpoint: '/api/list'
        });
        return;
    }

    // Set SVG content type
    res.setHeader('Content-Type', 'image/svg+xml');
    res.setHeader('Cache-Control', 'public, max-age=86400'); // Cache for 24 hours
    
    res.status(200).send(svg);
}
