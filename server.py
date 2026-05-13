#!/usr/bin/env python3
"""Agent README Generator MCP Server - Generate professional README files."""
import asyncio
import json
import sys
import time
from typing import Any

FREE_LIMIT = 5
PRO_KEYS = {}

def check_rate_limit(session_id: str) -> bool:
    if session_id in PRO_KEYS:
        return True
    key = f"count:{session_id}"
    now = int(time.time())
    if key not in check_rate_limit._cache:
        check_rate_limit._cache[key] = (now, 1)
        return True
    ts, cnt = check_rate_limit._cache[key]
    if now - ts > 3600:
        check_rate_limit._cache[key] = (now, 1)
        return True
    if cnt >= FREE_LIMIT:
        return False
    check_rate_limit._cache[key] = (ts, cnt + 1)
    return True
check_rate_limit._cache = {}

TEMPLATES = {
    "python-mcp": {
        "name": "Python MCP Server",
        "sections": ["Overview", "Features", "Installation", "Usage", "Tools", "Development", "License"],
    },
    "rest-api": {
        "name": "REST API Service",
        "sections": ["Overview", "Endpoints", "Authentication", "Examples", "Rate Limits", "License"],
    },
    "html-tool": {
        "name": "HTML/CSS Tool",
        "sections": ["Overview", "Demo", "Setup", "Usage", "Customization", "Browser Support", "License"],
    },
    "cli-app": {
        "name": "CLI Application",
        "sections": ["Overview", "Installation", "Commands", "Examples", "Configuration", "License"],
    },
    "npm-package": {
        "name": "npm Package",
        "sections": ["Overview", "Installation", "API", "Examples", "Contributing", "License"],
    },
}

BADGE_TEMPLATES = {
    "smithery": ("https://img.shields.io/badge/Smithery-Deployed-3B82F6?logo=data:image/svg+xml;base64,...",
                 "https://smithery.ai/server/{repo}"),
    "npm": ("https://img.shields.io/npm/v/{package}.svg",
            "https://www.npmjs.com/package/{package}"),
    "github-stars": ("https://img.shields.io/github/stars/{repo}.svg?style=social",
                     "https://github.com/{repo}"),
    "python": ("https://img.shields.io/badge/python-3.10+-blue.svg", ""),
    "license": ("https://img.shields.io/badge/license-MIT-green.svg", ""),
}

async def handle_request(request: dict) -> dict:
    method = request.get("method", "")
    params = request.get("params", {})
    req_id = request.get("id", None)
    session_id = params.get("session_id", "anonymous")
    
    if not check_rate_limit(session_id):
        return {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Free limit reached. Upgrade at https://rumblingb.github.io/agent-readme-generator-mcp"}, "id": req_id}
    
    if method == "tools/call":
        tool = params.get("name", "")
        args = params.get("arguments", {})
        
        if tool == "readme_generate":
            name = args.get("name", "my-project")
            desc = args.get("description", "A great project")
            features = args.get("features", [])
            tools_list = args.get("tools", [])
            template = args.get("template", "python-mcp")
            
            features_bullets = "\n".join(f"- {f}" for f in features)
            tools_bullets = "\n".join(f"- `{t}`" for t in tools_list)
            
            readme = f"""# {name}

{desc}

## Features

{features_bullets if features_bullets else "- Core functionality"}

## Tools

{tools_bullets if tools_bullets else "- Primary tool"}

## Installation

```bash
pip install agentpay-readme-generator-mcp
```

## Usage

Add to your MCP configuration:

```json
{{
  "mcpServers": {{
    "{name}": {{
      "command": "python",
      "args": ["-m", "{name.lower().replace('-', '_')}"]
    }}
  }}
}}
```

## Development

```bash
git clone https://github.com/Rumblingb/{name}.git
cd {name}
pip install -e .
```

## License

MIT
"""
            return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": readme}]}, "id": req_id}
        
        elif tool == "readme_add_badge":
            badge_type = args.get("type", "smithery")
            repo = args.get("repo", "Rumblingb/agent-readme-generator-mcp")
            package = args.get("package", "agentpay-readme-generator-mcp")
            
            if badge_type not in BADGE_TEMPLATES:
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": f"Unknown badge type: {badge_type}. Options: {', '.join(BADGE_TEMPLATES.keys())}"}]}, "id": req_id}
            
            img_url, link_url = BADGE_TEMPLATES[badge_type]
            img_url = img_url.replace("{repo}", repo).replace("{package}", package)
            link_url = link_url.replace("{repo}", repo).replace("{package}", package)
            
            badge = f"[![{badge_type}]({img_url})]({link_url})" if link_url else f"![{badge_type}]({img_url})"
            return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": badge}]}, "id": req_id}
        
        elif tool == "readme_validate":
            readme_content = args.get("content", "")
            checks = {
                "has_title": "# " in readme_content[:200],
                "has_description": len(readme_content) > 100,
                "has_installation": "## Installation" in readme_content or "## Setup" in readme_content,
                "has_usage": "## Usage" in readme_content,
                "has_license": "## License" in readme_content or "license" in readme_content.lower(),
                "has_badges": "[!" in readme_content,
                "has_toc": any(m in readme_content for m in ["## Table of Contents", "- [Installation]", "- [Usage]"]),
            }
            score = sum(1 for v in checks.values() if v)
            total = len(checks)
            passed = [k for k, v in checks.items() if v]
            failed = [k for k, v in checks.items() if not v]
            
            result = f"""## README Validation Report

**Score: {score}/{total}** ({(score/total)*100:.0f}%)

### Passed Checks:
{chr(10).join(f'- ✅ {k.replace("_", " ").title()}' for k in passed)}

### Failed Checks:
{chr(10).join(f'- ❌ {k.replace("_", " ").title()}' for k in failed) if failed else '- None!'}

### Recommendations:
{chr(10).join(f'- Add section: {k.replace("_", " ").title()}' for k in failed[:3]) if failed else '- Your README looks great!'}
"""
            return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": result}]}, "id": req_id}
        
        elif tool == "readme_templates":
            template_list = "\n\n".join(
                f"### {t['name']}\nSections: " + ", ".join(f"`{s}`" for s in t["sections"])
                for t in TEMPLATES.values()
            )
            return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": f"# Available README Templates\n\n{template_list}"]}, "id": req_id}
        
        return {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Unknown tool: {tool}"}, "id": req_id}
    
    if method == "tools/list":
        tools_spec = [
            {
                "name": "readme_generate",
                "description": "Generate a professional README for a GitHub repo",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Repository name"},
                        "description": {"type": "string", "description": "Project description"},
                        "features": {"type": "array", "items": {"type": "string"}, "description": "List of features"},
                        "tools": {"type": "array", "items": {"type": "string"}, "description": "List of tools/commands"},
                        "template": {"type": "string", "description": "Template type", "enum": list(TEMPLATES.keys())},
                        "session_id": {"type": "string", "description": "Session ID for rate limiting"},
                    },
                },
            },
            {
                "name": "readme_add_badge",
                "description": "Generate markdown for a badge",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "description": "Badge type", "enum": list(BADGE_TEMPLATES.keys())},
                        "repo": {"type": "string", "description": "GitHub repo (owner/repo)"},
                        "package": {"type": "string", "description": "npm package name"},
                        "session_id": {"type": "string", "description": "Session ID for rate limiting"},
                    },
                },
            },
            {
                "name": "readme_validate",
                "description": "Validate a README against best practices",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Full README content to validate"},
                        "session_id": {"type": "string", "description": "Session ID for rate limiting"},
                    },
                },
            },
            {
                "name": "readme_templates",
                "description": "List available README templates",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Session ID for rate limiting"},
                    },
                },
            },
        ]
        return {"jsonrpc": "2.0", "result": {"tools": tools_spec}, "id": req_id}
    
    return {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Unknown method: {method}"}, "id": req_id}

async def main():
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer
    buffer = b""
    
    while True:
        chunk = await asyncio.get_event_loop().run_in_executor(None, stdin.read1, 4096)
        if not chunk:
            break
        buffer += chunk
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            line = line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
                response = await handle_request(request)
                resp_line = json.dumps(response) + "\n"
                stdout.write(resp_line.encode())
                await asyncio.get_event_loop().run_in_executor(None, stdout.flush)
            except json.JSONDecodeError:
                error_resp = json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None}) + "\n"
                stdout.write(error_resp.encode())
                await asyncio.get_event_loop().run_in_executor(None, stdout.flush)

if __name__ == "__main__":
    asyncio.run(main())
