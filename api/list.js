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

    const { search, limit } = req.query;
    const generator = new BadgeGenerator();
    
    let icons;
    if (search) {
        icons = generator.searchIcons(search);
    } else {
        icons = generator.getAllAvailableIcons();
    }

    // Apply limit if specified
    if (limit) {
        const limitNum = parseInt(limit);
        if (!isNaN(limitNum) && limitNum > 0) {
            icons = icons.slice(0, limitNum);
        }
    }

    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Cache-Control', 'public, max-age=3600'); // Cache for 1 hour
    
    res.status(200).json({
        total: icons.length,
        icons: icons
    });
}
