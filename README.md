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

## Usage Examples

### Single Badges

#### HTML Example

```html
<img src="https://skill-badges.vercel.app/api/badge?icon=javascript&name=JavaScript" alt="JavaScript" />
<img src="https://skill-badges.vercel.app/api/badge?icon=react&name=React" alt="React" />
```

<img src="https://skill-badges.vercel.app/api/badge?icon=javascript&name=JavaScript" alt="JavaScript" />
<img src="https://skill-badges.vercel.app/api/badge?icon=react&name=React" alt="React" />

#### Markdown Example

```markdown
![JavaScript](https://skill-badges.vercel.app/api/badge?icon=javascript&name=JavaScript)
![React](https://skill-badges.vercel.app/api/badge?icon=react&name=React)
```

![JavaScript](https://skill-badges.vercel.app/api/badge?icon=javascript&name=JavaScript)
![React](https://skill-badges.vercel.app/api/badge?icon=react&name=React)

### Badges Grid

#### HTML Example
```html
<img src="https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker" alt="Tech Stack" />
<img src="https://skill-badges.vercel.app/api/s?c=javascript,typescript,vue,nuxt&cols=2" alt="Frontend Skills" />
```

<img src="https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker" alt="Tech Stack" />
<img src="https://skill-badges.vercel.app/api/s?c=javascript,typescript,vue,nuxt&cols=2" alt="Frontend Skills" />

#### Markdown Example

```markdown
![Tech Stack](https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker)
![Frontend Skills](https://skill-badges.vercel.app/api/s?c=javascript,typescript,vue,nuxt&cols=2)
```

![Tech Stack](https://skill-badges.vercel.app/api/s?c=python,react,nodejs,docker)
![Frontend Skills](https://skill-badges.vercel.app/api/s?c=javascript,typescript,vue,nuxt&cols=2)

## Local Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/lheintzmann1/skill-badges.git
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
# Generate all 3300+ badges
node generate-all.js
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Simple Icons](https://simpleicons.org) for providing the amazing icon collection
- [JetBrains Mono](https://www.jetbrains.com/mono/) for the beautiful monospace font

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
