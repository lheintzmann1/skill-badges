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

    const { q } = req.query;

    if (!q) {
        res.status(400).json({ error: 'Query parameter "q" is required' });
        return;
    }

    const generator = new BadgeGenerator();
    const results = generator.searchIcons(q);

    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Cache-Control', 'public, max-age=3600'); // Cache for 1 hour
    
    res.status(200).json({
        query: q,
        total: results.length,
        icons: results
    });
}
