# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A [Flowershow](https://flowershow.app) digital garden, hosted at <https://crbgc-philoserf.flowershow.me>. Content-only — Flowershow renders the markdown from its hosted side; pushing to `main` is the "deploy."

## Commands

```bash
task fmt    # prettier --write across all markdown (uses .ignore for excludes)
task check  # alias for fmt; placeholder for future checks
```

Prettier is the only toolchain — installed globally via Homebrew on this machine. `.ignore` excludes `.obsidian/` (per-machine editor state) and `.task/` (Taskfile cache).

The directory is also an Obsidian vault (`.obsidian/`), so markdown is typically authored in Obsidian and committed from the same working tree. Don't touch `.obsidian/` files unless the user asks — they're per-machine editor state.

## Content model

- Markdown files use YAML frontmatter. Current keys in use: `title`, `date` (`YYYY-MM-DD`), `showHero` (bool). Match the existing shape when adding new pages.
- Two licenses by design, and the split is load-bearing: `LICENSE` (MIT) covers code/config/templates; `CONTENT-LICENSE.md` (CC BY-NC-SA 4.0) covers prose and media. Don't merge them or apply one license to the other domain.

## Backlog

The next concrete step for this repo lives in `../NEXT.md` at the workspace root (one row per repo). Read the T01 row when starting work; update it when that step ships. If no T01 row exists yet, add one.
