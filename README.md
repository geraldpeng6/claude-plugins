# Claude Code Plugins

A collection of plugins for [Claude Code](https://claude.ai/code).

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [mitm-analyzer](./mitm-analyzer) | Capture traffic with mitmproxy and generate OpenAPI docs for reverse engineering APIs |

## Installation

```bash
# 1. Add marketplace (one-time setup)
/plugins marketplace add geraldpeng6/claude-plugins

# 2. Install plugins
/plugins install mitm-analyzer

# Or install directly without adding marketplace
/plugins install mitm-analyzer --from github:geraldpeng6/claude-plugins
```

### Local Development

```bash
claude --plugin-dir ./mitm-analyzer
```

## License

MIT License - See individual plugin directories for details.
