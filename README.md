# Simple Icons Skill Badges

Generate beautiful SVG skill badges using official brand colors and icons from [Simple Icons](https://simpleicons.org).

[![License](https://img.shields.io/github/license/lheintzmann1/skill-badges)](LICENSE)

## Features

- **3300+ Icons Available** - All Simple Icons with official brand colors
- **Skills Grid Generation** - Create organized grids of multiple skill badges
- **REST API** - Easy integration with any project
- **SVG Format** - Scalable vector graphics
- **Official Colors** - Authentic brand colors from Simple Icons
- **Fast Generation** - Optimized for performance
- **CORS Enabled** - Works from any domain

## API Endpoints

### Generate Badge

```http
GET /api/badge?icon={slug}&name={display_name}&color={hex_color}
```

**Parameters:**

- `icon` (required): Icon slug from Simple Icons
- `name` (optional): Display name for the badge
- `color` (optional): Custom hex color (without #)

**Examples:**

```http
/api/badge?icon=javascript&name=JavaScript
/api/badge?icon=react&name=React&color=ff6b6b
/api/badge?icon=python
```

### Generate Skills Grid

```http
GET /api/s?c={skills}&cols={columns}&gap={pixels}
```

**Parameters:**

- `c` (required): Comma-separated list of skill slugs
- `cols` (optional): Number of columns (default: 4)
- `gap` (optional): Gap between badges in pixels (default: 8)

**Examples:**

```http
/api/s?c=python,react,nodejs,docker
/api/s?c=javascript,typescript,vue,nuxt,tailwindcss,mongodb&cols=3
/api/s?c=python,django,postgresql,redis,docker,kubernetes&cols=2&gap=12
```

### List All Icons

```http
GET /api/list?limit={number}
```

**Parameters:**

- `limit` (optional): Maximum number of results

### Search Icons

```http
GET /api/search?q={query}
```

**Parameters:**

- `q` (required): Search term

## Local Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/skill-badges.git
cd skill-badges

# Install dependencies
npm install

# Generate all badges locally
npm run build

# Start development server
npm run dev
```

### Generate All Badges

```bash
# Generate all 3296+ badges
node generate-all.js
```

## Usage Examples

### Single Badges

#### HTML Example

```html
<img src="https://your-api-url/api/badge?icon=javascript&name=JavaScript" alt="JavaScript" />
<img src="https://your-api-url/api/badge?icon=react&color=61dafb" alt="React" />
```

#### Markdown Example

```markdown
![JavaScript](https://your-api-url/api/badge?icon=javascript&name=JavaScript)
![React](https://your-api-url/api/badge?icon=react&color=61dafb)
```

### Skills Grid

#### HTML Grid Example

```html
<img src="https://your-api-url/api/s?c=python,react,nodejs,docker" alt="Tech Stack" />
<img src="https://your-api-url/api/s?c=javascript,typescript,vue,nuxt&cols=2" alt="Frontend Skills" />
```

#### Markdown Grid Example

```markdown
![Tech Stack](https://your-api-url/api/s?c=python,react,nodejs,docker)
![Frontend Skills](https://your-api-url/api/s?c=javascript,typescript,vue,nuxt&cols=2)
```

#### For GitHub Profile README

```markdown
## 🚀 Tech Stack

![Skills](https://skill-badges.vercel.app/api/s?c=python,django,postgresql,redis,docker,kubernetes&cols=3)

## 💻 Frontend Technologies

![Frontend](https://skill-badges.vercel.app/api/s?c=react,nextjs,typescript,tailwindcss&cols=2)
```

### CSS

```css
.skill-badge {
  background-image: url('https://your-api-url/api/badge?icon=nodejs&name=Node.js');
}
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Simple Icons](https://simpleicons.org) for providing the amazing icon collection
- [JetBrains Mono](https://www.jetbrains.com/mono/) for the beautiful monospace font
- [Vercel](https://vercel.com) for the hosting platform

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
