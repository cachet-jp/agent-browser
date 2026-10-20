#!/bin/sh
# Build agent-browser from this fork and register it as a goose extension.
#
#   goose/install.sh            build, install, register (enabled)
#   goose/install.sh --no-build install an existing cli/target/release build
#
# The goose config change takes effect the next time goose starts.
set -eu

REPO="$(cd "$(dirname "$0")/.." && pwd)"
PREFIX="${AGENT_BROWSER_GOOSE_PREFIX:-$HOME/.local/share/agent-browser-goose}"
GOOSE_CONFIG="${GOOSE_CONFIG:-$HOME/.config/goose/config.yaml}"

if [ "${1:-}" != "--no-build" ]; then
  cargo build --release --manifest-path "$REPO/cli/Cargo.toml"
fi

mkdir -p "$PREFIX"
install -m 0755 "$REPO/cli/target/release/agent-browser" "$PREFIX/agent-browser"
install -m 0755 "$REPO/goose/agent-browser-goose" "$PREFIX/agent-browser-goose"
echo "installed: $PREFIX/agent-browser ($("$PREFIX/agent-browser" --version))"

python3 "$REPO/goose/register.py" "$GOOSE_CONFIG" "$PREFIX/agent-browser-goose"
