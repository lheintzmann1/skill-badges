#!/usr/bin/env node

import fs from 'fs/promises';
import { BadgeGenerator } from './api/badge-generator.js';

async function generateBadges(limit = null) {
    console.log('🚀 Generating Simple Icons badges...');
    
    const generator = new BadgeGenerator();
    const allIcons = generator.getAllAvailableIcons();
    
    const iconsToGenerate = limit ? allIcons.slice(0, limit) : allIcons;
    console.log(`📋 Generating ${iconsToGenerate.length} badges${limit ? ` (limited to ${limit})` : ''}`);
    
    // Create public directory structure
    await fs.mkdir('public', { recursive: true });
    await fs.mkdir('public/badges', { recursive: true });
    
    // Batch processing
    const batchSize = 100;
    let generated = 0;
    
    for (let i = 0; i < iconsToGenerate.length; i += batchSize) {
        const batch = iconsToGenerate.slice(i, i + batchSize);
        
        await Promise.all(batch.map(async (icon) => {
            try {
                const svg = generator.generateBadgeSvg(icon.slug, icon.title);
                if (svg) {
                    const filename = `${icon.slug}_badge.svg`;
                    // Write to public/badges/
                    await fs.writeFile(`public/badges/${filename}`, svg);
                    generated++;
                } else {
                    console.error(`❌ Error generating badge for ${icon.slug}: Icon not found`);
                }
            } catch (error) {
                console.error(`❌ Error generating badge for ${icon.slug}:`, error.message);
            }
        }));
        
        console.log(`📝 Generated ${Math.min(generated, iconsToGenerate.length)}/${iconsToGenerate.length} badges...`);
    }
    
    // Copy index.html to public directory
    try {
        await fs.copyFile('index.html', 'public/index.html');
        console.log('📄 Copied index.html to public directory');
    } catch (error) {
        console.log('ℹ️  index.html not found, skipping copy');
    }
    
    console.log(`✅ Successfully generated ${generated} badges!`);
}

// Parse command line arguments
const args = process.argv.slice(2);
const limitArg = args.find(arg => arg.startsWith('--limit='));
const limit = limitArg ? parseInt(limitArg.split('=')[1]) : null;

generateBadges(limit).catch(console.error);
