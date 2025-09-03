import * as simpleIcons from 'simple-icons';

export class BadgeGenerator {
    constructor() {
        // Badge configuration
        this.height = 30;
        this.padding = 16;
        this.iconSize = 20;
        this.textPadding = 12;
        this.borderRadius = 15;
        this.fontSize = 14;
    }

    calculateTextWidth(text) {
        // JetBrains Mono bold 14px - fixed width characters
        const charWidth = 8.4;
        return text.length * charWidth;
    }

    getTextColor(bgColor) {
        // Convert hex to RGB
        const hexColor = bgColor.replace('#', '');
        if (hexColor.length !== 6) {
            return '#ffffff';
        }

        try {
            const r = parseInt(hexColor.substring(0, 2), 16);
            const g = parseInt(hexColor.substring(2, 4), 16);
            const b = parseInt(hexColor.substring(4, 6), 16);

            // Calculate relative luminance
            const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

            // Return white for dark backgrounds, black for light backgrounds
            return luminance > 0.8 ? '#000000' : '#ffffff';
        } catch (error) {
            return '#ffffff';
        }
    }

    getSimpleIcon(iconSlug) {
        // Try direct match first
        let iconName = 'si' + iconSlug;
        let icon = simpleIcons[iconName];
        
        if (!icon) {
            // Try with first letter capitalized
            iconName = 'si' + iconSlug.charAt(0).toUpperCase() + iconSlug.slice(1);
            icon = simpleIcons[iconName];
        }
        
        if (!icon) {
            // Search by slug in all icons
            for (const [key, iconData] of Object.entries(simpleIcons)) {
                if (key.startsWith('si') && typeof iconData === 'object' && iconData.slug) {
                    if (iconData.slug === iconSlug) {
                        icon = iconData;
                        break;
                    }
                }
            }
        }
        
        return icon || null;
    }

    calculateBadgeWidth(displayName) {
        const textWidth = this.calculateTextWidth(displayName);
        return this.padding * 2 + this.iconSize + this.textPadding + textWidth;
    }

    generateBadgeSvg(iconSlug, displayName, customColor = null) {
        // Get icon from simple-icons
        const icon = this.getSimpleIcon(iconSlug);
        if (!icon) {
            return null;
        }

        // Use custom color or Simple Icons default color
        const badgeColor = customColor || `#${icon.hex}`;
        
        // Calculate dimensions
        const textWidth = this.calculateTextWidth(displayName);
        const totalWidth = this.calculateBadgeWidth(displayName);
        
        // Text color based on background
        const textColor = this.getTextColor(badgeColor);
        
        // Text position
        const textX = this.padding + this.iconSize + this.textPadding + (textWidth / 2);
        const textY = this.height / 2 + (this.fontSize * 0.35);
        
        // SVG template
        return `<svg width="${Math.round(totalWidth)}" height="${this.height}" viewBox="0 0 ${Math.round(totalWidth)} ${this.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&amp;display=swap');
    </style>
  </defs>
  <rect width="${Math.round(totalWidth)}" height="${this.height}" rx="${this.borderRadius}" fill="${badgeColor}"/>
  <g transform="translate(${this.padding}, ${(this.height - this.iconSize) / 2}) scale(${this.iconSize / 24})" fill="${textColor}">
    <path d="${icon.path}"/>
  </g>
  <text x="${textX}" y="${textY}" font-family="JetBrains Mono, monospace" font-size="${this.fontSize}" font-weight="800" fill="${textColor}" text-anchor="middle">${displayName}</text>
</svg>`;
    }

    getAllAvailableIcons() {
        const icons = [];
        for (const [key, icon] of Object.entries(simpleIcons)) {
            if (key.startsWith('si') && typeof icon === 'object' && icon.slug && icon.title && icon.hex) {
                icons.push({
                    slug: icon.slug,
                    title: icon.title,
                    color: `#${icon.hex}`
                });
            }
        }
        return icons.sort((a, b) => a.slug.localeCompare(b.slug));
    }

    searchIcons(query) {
        const allIcons = this.getAllAvailableIcons();
        const searchTerm = query.toLowerCase();
        
        return allIcons.filter(icon => 
            icon.slug.toLowerCase().includes(searchTerm) ||
            icon.title.toLowerCase().includes(searchTerm)
        );
    }
}
