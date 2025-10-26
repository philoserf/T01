# CLAUDE.md

This file provides guidance to Claude Code (<https://claude.ai/code>) when working with code in this repository.

## Project Overview

T01 is an Obsidian vault documenting a strategic plan for transforming a Toastmasters club. The content is published as a website using Flowershow (<https://flowershow.app/@philoserf/T01>).

The repository focuses on:

- Strategic planning for Toastmasters club transformation
- Legal compliance within Toastmasters International framework
- Meeting structures and demonstration series
- Member management and club operations

## Content Management

### Obsidian-Specific

This is an Obsidian vault with specific plugins and configurations:

- **Linter Plugin**: Automatically formats markdown on save according to `.obsidian/plugins/obsidian-linter/data.json`
- **Flowershow Plugin**: Publishes content to the web (repo: philoserf/T01)
- **Navigation**: Uses Obsidian wikilinks (`[[Page Name]]`) for internal navigation

### Frontmatter Requirements

All markdown files MUST include YAML frontmatter with these fields:

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

**Important frontmatter rules:**

- `title`: Auto-generated from first H1 or filename (via Linter)
- `date`: Creation date, auto-managed by Linter
- `updated`: Modification timestamp, auto-managed by Linter
- Tags and arrays use single-line format: `[item1, item2]`
- Arrays are sorted alphabetically by Linter
- YAML keys are sorted with priority keys first

### Linter Formatting Rules

The Obsidian Linter plugin enforces strict formatting. Key rules:

**YAML/Frontmatter:**

- Blank line after YAML frontmatter
- Compact YAML formatting
- Tags formatted as arrays
- Timestamps auto-updated
- Arrays sorted alphabetically

**Headings:**

- Title Case capitalization
- Start at H2 (H1 reserved for title)
- No trailing punctuation
- Blank lines before and after

**Lists:**

- Unordered lists use `-` marker
- Ordered lists use ascending numbers with `.`
- Single space after list markers

**Formatting:**

- Emphasis with `_underscores_`
- Strong with `**asterisks**`
- No bare URLs (must be in markdown link format)
- Proper ellipsis (`…` not `...`)
- Smart quotes enabled
- Trailing spaces removed
- Line break at document end

**Whitespace:**

- Consecutive blank lines collapsed
- Empty line around blockquotes, code fences, tables, math blocks
- No multiple spaces

### Git Workflow

The repository uses a simple git workflow:

- Main branch: `main`
- Content updates committed with descriptive messages
- Recent pattern: "Update: [Date]" or "Update content [filename]"
- Flowershow plugin auto-publishes to GitHub (philoserf/T01)

**Note:** The Flowershow plugin data contains a GitHub token - this file should never be committed or shared.

## Content Structure

### Core Documents

- `README.md`: Index page with links to all main documents
- `About.md`: Technical background and colophon
- `Links.md`: External Toastmasters resources
- `Strategic Plan for Transformation.md`: Main strategic document
- `Demonstration Meeting Series.md`: Club building process
- `Member States (discipline).md`: Member management
- `Exact Requirements of the Club Constitution.md`: Legal requirements
- `Essential Operational Elements and Requirements.md`: Operations guide
- `Required Documents and Information for a Toastmasters Club.md`: Documentation requirements

### Website Configuration

`config.json` defines Flowershow website settings:

- Navigation structure
- Social media links
- Logo and branding
- Edit link visibility

## Editing Guidelines

When editing markdown files:

1. Preserve existing frontmatter structure
2. Let Linter handle formatting (it runs on save in Obsidian)
3. Use wikilinks for internal references: `[[Page Name]]`
4. Maintain Title Case for headings
5. Keep URLs in proper markdown link format
6. Ensure blank line after frontmatter
7. Start content headings at H2 level

## Publishing

Content is automatically published via:

1. Obsidian Flowershow plugin pushes to GitHub repo
2. Flowershow cloud service builds and deploys website
3. Live site: <https://flowershow.app/@philoserf/T01>

Changes pushed to the GitHub repository trigger automatic rebuilds on Flowershow.
