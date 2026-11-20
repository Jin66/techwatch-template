#!/usr/bin/env bash
# Writes today's digest with Claude Code, commits and pushes it. Run by the systemd timer every
# morning, or by hand with `mise run veille`.
set -euo pipefail
cd "$(dirname "$0")/.."

digest="digests/$(date +%F).md"
if [[ -f "$digest" ]]; then
    echo "$digest already exists"
    exit 0
fi

# Permissions come from .claude/settings.json, so the run never waits for a prompt.
claude -p "/veille"

if [[ ! -f "$digest" ]]; then
    echo "Claude did not write $digest" >&2
    exit 1
fi

git add "$digest"
git commit -q -m "📰 docs(digest): add digest of $(date +%F)" -m "Co-Authored-By: Claude <noreply@anthropic.com>"
# Offline at boot: the push fails but the commit stays, and the next run pushes both.
git push -q
echo "$digest committed and pushed"
