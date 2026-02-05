---
title: AGENTS
date: 2025-10-26
updated: 2026-02-05
---

## Project Overview

T01 is an Obsidian vault for Toastmasters club transformation, published via Flowershow.

## Architecture

Obsidian vault → Linter (on save) → git push → GitHub → Flowershow cloud

## Content Structure

- All markdown content lives flat in the root directory
- Images go in `assets/`

## Commands

```bash
bunx prettier --write <file>   # format markdown
```

## Frontmatter Requirements

Frontmatter is auto-managed by Obsidian Linter on save.

## Editing Guidelines

1. Preserve frontmatter structure
2. Let Linter handle formatting on save
3. Use wikilinks for internal references: `[[Page Name]]`
4. Start content headings at H2 (H1 reserved for title)
5. Maintain Title Case for headings
6. Keep URLs in markdown link format: `[text](url)`

## Linter Formatting (Auto-Applied)

- Emphasis: `_underscores_`
- Strong: `**asterisks**`
- Arrays sorted alphabetically
- Smart quotes enabled
- Proper ellipsis: `…` (not `…`)
- Single space after list markers
- Blank lines before/after headings, code blocks, tables

## Key Configuration

- `config.json` — Flowershow site config (nav, sidebar, edit link)

## Publishing

Content auto-publishes when pushed to GitHub → Flowershow cloud.
