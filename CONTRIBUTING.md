# Contributing to Boltflow

Thank you for your interest in contributing to Boltflow! Contributions, feedback, and suggestions are welcome.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)

## 📜 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards others

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title** - Descriptive summary of the issue
- **Steps to reproduce** - Detailed steps to reproduce the behavior
- **Expected behavior** - What you expected to happen
- **Actual behavior** - What actually happened
- **Environment** - OS, Node version, browser, etc.
- **Screenshots** - If applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title** - Descriptive summary
- **Detailed description** - Explain the enhancement
- **Use cases** - Why would this be useful?
- **Examples** - Mockups or code examples if applicable

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch** - `git checkout -b feature/amazing-feature`
3. **Make your changes** - Follow coding standards
4. **Test your changes** - Ensure everything works
5. **Commit your changes** - Follow commit guidelines
6. **Push to your fork** - `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## 🛠️ Development Setup

### Prerequisites

- Node.js 20+
- Python 3.11+
- Redis (via Docker)
- OpenAI API key

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/boltflow-modern.git
cd boltflow-modern

# Add upstream remote
git remote add upstream https://github.com/krhebbar/boltflow-modern.git

# Install dependencies
./scripts/setup.sh

# Add your API keys
cp .env.example .env
# Edit .env with your keys

# Start development
./scripts/dev.sh
```

### Project Structure

```
boltflow-modern/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # FastAPI backend
├── packages/         # Shared packages
├── docker/           # Docker configs
├── docs/             # Documentation
└── scripts/          # Helper scripts
```

## 🔄 Pull Request Process

1. **Update documentation** - If you change APIs or functionality
2. **Add tests** - For new features or bug fixes
3. **Follow coding standards** - See below
4. **Update CHANGELOG** - Add your changes
5. **Ensure CI passes** - All tests must pass
6. **Request review** - Tag maintainers for review

### PR Title Format

```
type(scope): short description

Examples:
feat(scraper): add support for dynamic content
fix(api): resolve CORS issue in WebSocket
docs(readme): update installation instructions
refactor(generator): improve code generation logic
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
```

## 💻 Coding Standards

### TypeScript/JavaScript

```typescript
// Use descriptive variable names
const scrapedPages = await scraper.scrape(url)

// Add JSDoc comments for functions
/**
 * Analyzes a scraped page and extracts components
 * @param html - The HTML content to analyze
 * @returns Component analysis results
 */
async function analyzePage(html: string): Promise<Analysis> {
  // Implementation
}

// Use async/await over promises
const data = await fetchData() // Good
fetchData().then(data => {})   // Avoid

// Destructure when possible
const { url, maxPages } = request.body

// Use meaningful constants
const MAX_RETRY_ATTEMPTS = 3
const DEFAULT_TIMEOUT_MS = 5000
```

### Python

```python
# Follow PEP 8 style guide
from typing import Dict, List

# Use type hints
async def analyze_page(html: str, css: str = None) -> Dict:
    """
    Analyzes a page using AI.

    Args:
        html: The HTML content
        css: Optional CSS content

    Returns:
        Analysis results dictionary
    """
    pass

# Use descriptive names
scraped_pages = []  # Good
sp = []            # Avoid

# Use f-strings for formatting
message = f"Scraped {page_count} pages"
```

### React Components

```tsx
// Use functional components with TypeScript
interface ButtonProps {
  variant: "primary" | "secondary"
  onClick: () => void
  children: React.ReactNode
}

export function Button({ variant, onClick, children }: ButtonProps) {
  return (
    <button
      className={cn("base-styles", variant === "primary" && "primary-styles")}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

// Export at bottom for better readability
```

### File Naming

- **Components**: PascalCase - `ProjectCard.tsx`
- **Utilities**: camelCase - `formatDate.ts`
- **Hooks**: camelCase with "use" prefix - `useWebSocket.ts`
- **Types**: PascalCase - `Project.ts` or `types.ts`
- **API routes**: kebab-case - `scraper-status.ts`

## 📝 Commit Guidelines

### Format

```
type(scope): subject

body (optional)

footer (optional)
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting)
- **refactor**: Code refactoring
- **test**: Test additions or changes
- **chore**: Build process or tooling changes

### Examples

```bash
feat(api): add WebSocket support for real-time updates

Implemented WebSocket manager to broadcast progress updates
to connected clients during scraping and analysis.

Closes #42

---

fix(scraper): handle timeout errors gracefully

Added retry logic and better error messages for timeout scenarios.

---

docs(readme): update installation instructions

Added Docker setup instructions and troubleshooting section.
```

## 🧪 Testing

### Running Tests

```bash
# Frontend tests
npm run test --filter=web

# Backend tests
cd apps/api
pytest

# E2E tests
npm run test:e2e
```

### Writing Tests

```typescript
// Component tests
describe('ProjectCard', () => {
  it('should render project details', () => {
    render(<ProjectCard project={mockProject} />)
    expect(screen.getByText(mockProject.name)).toBeInTheDocument()
  })
})

// API tests
describe('POST /api/scraper/start', () => {
  it('should start scraping job', async () => {
    const response = await request(app)
      .post('/api/scraper/start')
      .send({ url: 'https://example.com' })

    expect(response.status).toBe(200)
    expect(response.body).toHaveProperty('job_id')
  })
})
```

## 📚 Documentation

When adding features:

1. Update relevant documentation in `/docs`
2. Add JSDoc/docstrings to functions
3. Update README if needed
4. Add examples if applicable

## 🎯 Areas for Contribution

Looking for ways to contribute? Here are some ideas:

- 🐛 **Bug Fixes** - Check the issues tab
- 📝 **Documentation** - Improve existing docs
- ✨ **Features** - Implement items from the roadmap
- 🧪 **Tests** - Increase test coverage
- 🎨 **UI/UX** - Enhance dashboard design
- ⚡ **Performance** - Optimize code
- 🌐 **Internationalization** - Add translations

## ❓ Questions?

- Open a discussion on GitHub
- Check existing issues and discussions
- Review the documentation in `/docs`

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Boltflow! 🚀
