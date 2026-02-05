---
title: AGENTS
date: 2025-10-26
updated: 2026-02-05
---

# CLAUDE.md

This file is the entry point for Claude Code when working in this repository.

## Project Overview

T01 is an Obsidian vault for Toastmasters club transformation, published via Flowershow.

## Architecture

Obsidian vault → Linter (on save) → Flowershow plugin → GitHub → Flowershow cloud

## Content Structure

- All markdown content lives flat in the root directory
- Images go in `assets/`

## Commands

```bash
bunx prettier --write <file>   # format markdown
bunx markdownlint <file>       # lint markdown
```

## Frontmatter Requirements

All markdown files MUST include:

```yaml
---
title: Page Title
date: YYYY-MM-DD
updated: YYYY-MM-DD
created: YYYY-MM-DD
tags: [tag1, tag2]
category: Category Name
description: Brief description
---
```

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
- `.markdownlintrc` — lint overrides: MD013 off (line length), MD025 off (multiple H1), MD036 off (emphasis as heading)

## Publishing

Content auto-publishes via Obsidian Flowershow plugin → GitHub → Flowershow cloud.

**Sensitive files — never commit or share:**

- `.obsidian/plugins/flowershow/data.json` (contains GitHub token)
- `exmemo-tools/data.json` (contains API keys)
