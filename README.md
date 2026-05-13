# Agent README Generator MCP

[![Smithery](https://img.shields.io/badge/Smithery-Deployed-3B82F6)](https://smithery.ai/server/@Rumblingb/agent-readme-generator-mcp)
[![npm](https://img.shields.io/npm/v/agentpay-readme-generator-mcp)](https://www.npmjs.com/package/agentpay-readme-generator-mcp)
[![GitHub Stars](https://img.shields.io/github/stars/Rumblingb/agent-readme-generator-mcp?style=social)](https://github.com/Rumblingb/agent-readme-generator-mcp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)](https://rumblingb.github.io/agent-readme-generator-mcp)

An MCP (Model Context Protocol) server that generates professional README files for GitHub repositories. Built for MCP-compatible clients like Claude Desktop, Cursor, and VS Code.

## Features

- **readme_generate** — Generate a complete, formatted README from a repo name, description, features, and tools list
- **readme_add_badge** — Generate markdown for badges (Smithery, npm, GitHub stars, Python, License)
- **readme_validate** — Check a README against best practices (title, description, installation, usage, license, badges, TOC)
- **readme_templates** — List available README templates (Python MCP, REST API, HTML Tool, CLI App, npm Package)

## Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | 5 READMEs per session |
| **Pro** | **$9/mo** | Unlimited READMEs, custom branding, all templates, priority support |

[**Subscribe to Pro →**](https://rumblingb.github.io/agent-readme-generator-mcp)

## Installation

### Option 1: npm (recommended for MCP clients)

```bash
npm install -g agentpay-readme-generator-mcp
```

### Option 2: Smithery

[Install from Smithery](https://smithery.ai/server/@Rumblingb/agent-readme-generator-mcp)

### Option 3: Manual

```bash
git clone https://github.com/Rumblingb/agent-readme-generator-mcp.git
cd agent-readme-generator-mcp
pip install -r requirements.txt
python server.py
```

## MCP Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "readme-generator": {
      "command": "python",
      "args": ["-m", "server"],
      "env": {
        "PYTHONPATH": "/path/to/agent-readme-generator-mcp"
      }
    }
  }
}
```

### Cursor

Add to Cursor's MCP configuration.

### VS Code

Add to VS Code's settings for GitHub Copilot.

## Tools

### `readme_generate`

Generate a complete README file.

**Parameters:**
- `name` (string): Repository name
- `description` (string): Project description
- `features` (string[]): List of features
- `tools` (string[]): List of tools/commands
- `template` (string): Template type (`python-mcp`, `rest-api`, `html-tool`, `cli-app`, `npm-package`)
- `session_id` (string, optional): Session identifier for rate limiting

### `readme_add_badge`

Generate markdown for a badge.

**Parameters:**
- `type` (string): Badge type (`smithery`, `npm`, `github-stars`, `python`, `license`)
- `repo` (string): GitHub repo (owner/repo format)
- `package` (string): npm package name

### `readme_validate`

Validate a README against best practices checklist.

**Parameters:**
- `content` (string): Full README text to validate

### `readme_templates`

List available README templates with their section layouts.

## Development

```bash
git clone https://github.com/Rumblingb/agent-readme-generator-mcp.git
cd agent-readme-generator-mcp
pip install -r requirements.txt
python server.py
```

## Testing

```bash
# Test the server starts and responds to tools/list
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python server.py
```

## Deployment

The site is deployed via GitHub Pages at [rumblingb.github.io/agent-readme-generator-mcp](https://rumblingb.github.io/agent-readme-generator-mcp).

## License

MIT
