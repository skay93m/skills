---
name: worker-pool
description: 2-AI Stack worker pool orchestration guidelines for Antigravity (AGY) and Codex.
---

# 2-AI Stack Headless Worker Pool

1. **Tier 1: `flash_lite` Subagents**: Default local file, shell, and Basic Memory MCP worker for fast, low-cost parallel orchestration.
2. **Tier 2: `codex exec --ephemeral "<prompt>"`**: Stateless 1-shot OpenAI/Codex subscription worker for batch refactoring, code generation, or reviews without multi-turn $O(N^2)$ session bloat.
3. **Retired**: Claude Pro and GitHub Copilot are retired in favor of the standardized 2-AI Stack (AGY + ChatGPT/Codex).
