#!/usr/bin/env node

import fs from 'fs/promises';
import { BadgeGenerator } from './api/badge-generator.js';

async function generateBadges(limit = null) {
    console.log('🚀 Generating Simple Icons badges...');
    
    const generator = new BadgeGenerator();
    const allIcons = generator.getAllAvailableIcons();
    
    const iconsToGenerate = limit ? allIcons.slice(0, limit) : allIcons;
    console.log(`📋 Generating ${iconsToGenerate.length} badges${limit ? ` (limited to ${limit})` : ''}`);
    
    // Create badges directory
    await fs.mkdir('badges', { recursive: true });
    
    // Batch processing
    const batchSize = 100;
    let generated = 0;
    
    for (let i = 0; i < iconsToGenerate.length; i += batchSize) {
        const batch = iconsToGenerate.slice(i, i + batchSize);
        
        await Promise.all(batch.map(async (icon) => {
            try {
                const svg = generator.generateBadgeSvg(icon.slug);
                await fs.writeFile(`badges/${icon.slug}_badge.svg`, svg);
                generated++;
            } catch (error) {
                console.error(`❌ Error generating badge for ${icon.slug}:`, error.message);
            }
        }));
        
        console.log(`📝 Generated ${Math.min(generated, iconsToGenerate.length)}/${iconsToGenerate.length} badges...`);
    }
    
    console.log(`✅ Successfully generated ${generated} badges!`);
}

// Parse command line arguments
const args = process.argv.slice(2);
const limitArg = args.find(arg => arg.startsWith('--limit='));
const limit = limitArg ? parseInt(limitArg.split('=')[1]) : null;

generateBadges(limit).catch(console.error);
