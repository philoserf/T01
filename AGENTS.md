---
title: AGENTS
date: 2025-10-26
updated: 2025-12-05
---

## Project Overview

T01 is an Obsidian vault for Toastmasters club transformation, published via Flowershow.

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

## Publishing

Content auto-publishes via Obsidian Flowershow plugin → GitHub → Flowershow cloud

**Note:** Flowershow plugin data contains GitHub token—never commit or share.
