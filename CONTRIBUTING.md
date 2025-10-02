# Contributing to MCP Server Collection

Thank you for your interest in contributing to the MCP Server Collection! This document provides guidelines and information for contributors.

## What is MCP?

Model Context Protocol (MCP) is a protocol that enables AI assistants to securely connect to data sources and tools. MCP servers provide standardized interfaces for AI systems to interact with various services and data sources.

## How to Contribute

### 1. Fork and Clone

1. Fork this repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp-server-collection.git
   cd mcp-server-collection
   ```

### 2. Create a Branch

Create a new branch for your contribution:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Development Guidelines

#### MCP Server Structure
When adding a new MCP server, please follow this structure:

```
servers/
├── your-server-name/
│   ├── README.md          # Documentation for your server
│   ├── server.py          # Main server implementation
│   ├── requirements.txt   # Python dependencies
│   ├── config.json        # Configuration file (if needed)
│   └── examples/          # Usage examples
│       └── example.py
```

#### Code Standards
- Use Python 3.8+ for Python-based servers
- Follow PEP 8 style guidelines
- Include comprehensive docstrings
- Add type hints where appropriate
- Write clear, descriptive commit messages

#### Documentation Requirements
Each MCP server must include:
- A detailed README.md explaining:
  - What the server does
  - Installation instructions
  - Configuration options
  - Usage examples
  - Available tools/functions
- Inline code documentation
- Example usage files

### 4. Testing

Before submitting your contribution:
- Test your MCP server thoroughly
- Ensure it follows MCP protocol standards
- Verify all tools/functions work as expected
- Test with different AI clients if possible

### 5. Submitting Changes

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub

## Pull Request Guidelines

### Before Submitting
- [ ] Your code follows the project's coding standards
- [ ] You have added appropriate documentation
- [ ] You have tested your changes
- [ ] Your commit messages are clear and descriptive
- [ ] You have updated the main README.md if adding a new server

### PR Description Template
When creating a pull request, please include:
- A clear description of what your changes do
- Any new dependencies or requirements
- Screenshots or examples if applicable
- Reference any related issues

### Review Process
- All PRs require review before merging
- Maintainers will review code quality, documentation, and functionality
- Be responsive to feedback and requested changes
- Keep PRs focused and reasonably sized

## Types of Contributions

### New MCP Servers
We welcome new MCP server implementations! Some ideas:
- Database connectors (PostgreSQL, MongoDB, etc.)
- API integrations (REST, GraphQL)
- File system operations
- Cloud service integrations
- Development tools
- Data processing utilities

### Improvements to Existing Servers
- Bug fixes
- Performance improvements
- New features
- Better documentation
- Additional examples

### Documentation
- Improving existing documentation
- Adding tutorials
- Creating examples
- Fixing typos or unclear explanations

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior
- Harassment, trolling, or discriminatory language
- Personal attacks or political discussions
- Spam or off-topic discussions
- Any other conduct that could be considered inappropriate

## Getting Help

If you need help or have questions:
- Open an issue on GitHub
- Check existing issues and discussions
- Review the MCP documentation: https://modelcontextprotocol.io/

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Recognition

Contributors will be recognized in:
- The project's README.md
- Release notes for significant contributions
- GitHub's contributor graph

Thank you for contributing to the MCP Server Collection! 🚀