# Skill Badges API

A REST API service for generating high-quality SVG skill badges with icons. Generate beautiful, consistent badge grids for programming languages, frameworks, tools, and technologies on-demand via API endpoints.

![Example Badge Grid](https://skill-badges.vercel.app/api/s?c=python,javascript,react,nodejs,docker&perline=5)

## Live API

**Base URL**: `https://skill-badges.vercel.app`

Try it now: [https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker](https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker)

## API Endpoints

### Static Badge Grids (`/api/s`)

Generate static badge grids with consistent caching.

**Endpoint**: `GET /api/s`

**Parameters**:

- `c` (required): Comma-separated list of badge names
- `perline` (optional): Number of badges per line (default: 4, max: 20)

**Examples**:

```url
# Single line with 5 badges
/api/s?c=python,javascript,react,nodejs,docker&perline=5

# Multi-line grid (4 badges per line)
/api/s?c=python,javascript,react,nodejs,docker,aws,git,linux

# Custom layout (3 per line)
/api/s?c=python,react,nodejs,docker,aws,kubernetes&perline=3
```

### Dynamic Badge Grids (`/api/d`)

Future-enhanced badges with shorter cache times for real-time data.

**Endpoint**: `GET /api/d`

**Parameters**: Same as `/api/s`

**Future Features**:

- Real-time GitHub stats
- npm download counts
- Custom themes
- User-specific collections

## Usage Examples

### Markdown Integration

```markdown
![My Skills](https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker&perline=4)
```

![My Skills](https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker&perline=4)

### HTML Integration

```html
<img src="https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker&perline=4" 
     alt="My Skills">
```

<img src="https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker&perline=4" alt="My Skills">

## Available Badges

This project includes badges for 300+ technologies including:

Complete list available at: <https://skill-badges.vercel.app/api/list>

## Credits

- **[m3-Markdown-Badges](https://github.com/ziadOUA/m3-Markdown-Badges)** (GPL v3) - Original concept and design inspiration
- **[Devicon](https://github.com/devicons/devicon)** (MIT License) - High-quality icons
- **[JetBrains Mono](https://github.com/JetBrains/JetBrainsMono)** (OFL 1.1) - Beautiful monospace font

## Roadmap

- [x] ~~REST API for on-demand badge creation~~
- [ ] Licenses badges
- [ ] Dynamic badges (stars, forks, issues, downloads, and so on...)

## Contributing

Contributions are welcome! Please open an issue or pull request for suggestions and improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
