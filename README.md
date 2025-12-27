# Claude Code Plugins

A collection of plugins for [Claude Code](https://claude.ai/code).

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [mitm-analyzer](./mitm-analyzer) | Capture traffic with mitmproxy and generate OpenAPI docs for reverse engineering APIs |

## Installation

```bash
# Install from this marketplace
/plugins install <plugin-name> --from github:geraldpeng6/claude-plugins

# Or load locally for development
claude --plugin-dir ./mitm-analyzer
```

## License

MIT License - See individual plugin directories for details.
