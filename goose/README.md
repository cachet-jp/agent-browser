# agent-browser for goose

This fork packages agent-browser as a [goose](https://github.com/block/goose)
extension. goose talks to agent-browser's built-in stdio MCP server
(`agent-browser mcp`), so it gets typed tools like `agent_browser_open`,
`agent_browser_snapshot`, `agent_browser_click`, `agent_browser_fill` and
`agent_browser_screenshot`.

## Install

Requires Rust (`cargo`) and Chrome (or run `agent-browser install`).

```sh
goose/install.sh
```

This script:

1. builds `cli/` in release mode,
2. installs the binary and launcher to `~/.local/share/agent-browser-goose/`,
3. adds an enabled `agent-browser` stdio extension to
   `~/.config/goose/config.yaml` (after writing a backup).

Restart goose to load the extension.

## Files

| File | Purpose |
|------|---------|
| `agent-browser-goose` | Launcher that goose spawns. It runs `agent-browser mcp --tools core,tabs`. |
| `install.sh` | Builds, installs and registers the extension. |
| `register.py` | Adds or refreshes the extension entry in goose's `config.yaml`. |

## Configuration

Set these in the extension's environment variables in goose:

| Variable | Default | Meaning |
|----------|---------|---------|
| `AGENT_BROWSER_GOOSE_TOOLS` | `core,tabs` | MCP tool profiles (`core`, `tabs`, `network`, `state`, `debug`, `react`, `mobile`, `all`) |
| `AGENT_BROWSER_SESSION` | `goose` | Browser session name, kept separate from interactive CLI use |
| `AGENT_BROWSER_HEADED` | unset | Set to `1` to show the browser window |
| `AGENT_BROWSER_GOOSE_BIN` | `~/.local/share/agent-browser-goose/agent-browser` | Binary that the launcher runs |

## Syncing with upstream

```sh
git fetch upstream && git merge upstream/main && goose/install.sh
```
