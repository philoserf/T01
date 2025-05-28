#!/usr/bin/env python3
"""
Tidy Tags - A tool for processing tags in markdown file frontmatter.

This module provides functionality to process and transform tags in YAML frontmatter
of markdown files. It supports operations like replacing spaces with hyphens and
converting tags to lowercase.

Features:
- Safe YAML frontmatter detection
- Dry-run mode for previewing changes
- Verbose and quiet logging modes
- Large file size protection
- Comprehensive error handling

Example usage:
    python tidy_tags.py replace-spaces --dry-run
    python tidy_tags.py lowercase /path/to/notes --verbose
"""

import argparse
import os
import re
import sys
from enum import Enum
from pathlib import Path
from typing import Callable

__version__ = "1.0.0"
__author__ = "Mark Ayers"

# Constants
MAX_FILE_SIZE_MB = 10


class Operation(Enum):
    """Available tag operations."""

    REPLACE_SPACES = "replace-spaces"
    LOWERCASE = "lowercase"


# Public API
__all__ = [
    "Logger",
    "FileProcessor",
    "find_yaml_tags",
    "parse_tags",
    "validate_tag_structure",
    "transform_tags_in_content",
    "process_tags",
    "replace_spaces_in_tags",
    "convert_tags_to_lowercase",
]


class Logger:
    """Simple logger with verbosity controls."""

    def __init__(self, verbose: bool = False, quiet: bool = False):
        self.verbose = verbose
        self.quiet = quiet

    def info(self, message: str):
        """Log info level message."""
        if not self.quiet:
            print(message)

    def debug(self, message: str):
        """Log debug level message."""
        if self.verbose and not self.quiet:
            print(message)

    def error(self, message: str):
        """Log error message (always shown)."""
        print(message)


# ============================================================================
# YAML and Tag Parsing Utilities
# ============================================================================


def find_yaml_tags(content: str) -> tuple[str, int, int] | None:
    """
    Find tags array in YAML frontmatter only.

    Returns:
        Tuple of (matched_text, start_pos, end_pos) or None if not found
    """
    frontmatter_pattern = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL | re.MULTILINE)
    frontmatter_match = frontmatter_pattern.search(content)

    if frontmatter_match:
        yaml_content = frontmatter_match.group(1)
        tag_pattern = re.compile(r"^tags:\s*\[(.*?)\]", re.MULTILINE)
        tag_match = tag_pattern.search(yaml_content)
        if tag_match:
            yaml_start = frontmatter_match.start(1)
            start_pos = yaml_start + tag_match.start()
            end_pos = yaml_start + tag_match.end()
            return tag_match.group(0), start_pos, end_pos
    return None


def parse_tags(tags_str: str) -> list[str]:
    """Parse comma-separated tags while preserving quoted strings."""
    if not tags_str.strip():
        return []

    updated_tags = []
    in_quotes = False
    current_tag = ""

    for char in tags_str:
        if char == '"' and (len(current_tag) == 0 or current_tag[-1] != "\\"):
            in_quotes = not in_quotes
            current_tag += char
        elif char == "," and not in_quotes:
            tag = current_tag.strip()
            if tag:  # Don't add empty tags
                updated_tags.append(tag)
            current_tag = ""
        else:
            current_tag += char

    # Add final tag if exists
    if current_tag.strip():
        updated_tags.append(current_tag.strip())

    return updated_tags


def validate_tag_structure(tags: list[str]) -> bool:
    """Validate that parsed tags have proper structure."""
    for tag in tags:
        # Check for unmatched quotes
        if tag.count('"') % 2 != 0:
            return False
        # Check for empty quoted strings
        if tag == '""':
            return False
        # Check for malformed quoted tags
        if tag.startswith('"') and not tag.endswith('"'):
            return False
    return True


# ============================================================================
# File Processing
# ============================================================================


class FileProcessor:
    """Handles file discovery, reading, and writing operations."""

    def __init__(self, logger: Logger, max_file_size_mb: int = MAX_FILE_SIZE_MB):
        self.logger = logger
        self.max_file_size_mb = max_file_size_mb

    def should_skip_file(self, filepath: str) -> bool:
        """Check if file should be skipped due to size or other criteria."""
        try:
            file_path = Path(filepath)
            file_size = file_path.stat().st_size
            if file_size > self.max_file_size_mb * 1024 * 1024:
                self.logger.info(
                    f"Skipping large file: {filepath} ({file_size / 1024 / 1024:.1f}MB)"
                )
                return True
        except OSError:
            return True
        return False

    def read_file_content(self, filepath: str) -> str | None:
        """Read file content safely."""
        try:
            return Path(filepath).read_text(encoding="utf-8")
        except (IOError, UnicodeDecodeError) as e:
            self.logger.error(f"Error reading {filepath}: {e}")
            return None

    def write_file_content(self, filepath: str, content: str) -> bool:
        """Write file content safely."""
        try:
            Path(filepath).write_text(content, encoding="utf-8")
            return True
        except IOError as e:
            self.logger.error(f"Error writing {filepath}: {e}")
            return False

    def find_markdown_files(self, directory: str) -> list[str]:
        """Find all markdown files in directory."""
        directory_path = Path(directory)
        return [str(file_path) for file_path in directory_path.rglob("*.md")]


# ============================================================================
# Tag Processing Logic
# ============================================================================


def transform_tags_in_content(
    content: str, tag_transformer: Callable[[str], str], logger: Logger
) -> tuple[str, bool]:
    """
    Transform tags in file content.

    Returns:
        Tuple of (updated_content, was_changed)
    """
    tag_match_result = find_yaml_tags(content)
    if not tag_match_result:
        return content, False

    matched_text, start_pos, end_pos = tag_match_result
    tag_pattern = re.compile(r"tags:\s*\[(.*?)\]", re.DOTALL)
    inner_match = tag_pattern.search(matched_text)

    if not inner_match:
        return content, False

    tags_str = inner_match.group(1)
    updated_tags = parse_tags(tags_str)

    # Validate tag structure
    if not validate_tag_structure(updated_tags):
        logger.debug("Invalid tag structure found")
        return content, False

    original_tags = updated_tags.copy()

    # Apply transformation
    for i, tag in enumerate(updated_tags):
        if tag.startswith('"') and tag.endswith('"'):
            tag_content = tag[1:-1]
            transformed_content = tag_transformer(tag_content)
            updated_tags[i] = f'"{transformed_content}"'
        else:
            updated_tags[i] = tag_transformer(tag)

    # Check if any changes were made
    if updated_tags == original_tags:
        return content, False

    updated_tags_str = ", ".join(updated_tags)
    updated_content = (
        content[:start_pos] + f"tags: [{updated_tags_str}]" + content[end_pos:]
    )

    return updated_content, True


def process_tags(
    directory: str,
    tag_transformer: Callable[[str], str],
    operation_name: str,
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
    max_file_size_mb: int = MAX_FILE_SIZE_MB,
) -> dict:
    """
    Process tags in markdown files with a custom transformation.

    Args:
        directory: Directory to search for markdown files
        tag_transformer: Function to transform individual tags
        operation_name: Name of the operation for logging
        dry_run: If True, only show what would be changed without modifying files
        verbose: Enable verbose output
        quiet: Suppress non-error output
        max_file_size_mb: Maximum file size in MB to process

    Returns:
        Dictionary with processing results
    """
    logger = Logger(verbose, quiet)
    file_processor = FileProcessor(logger, max_file_size_mb)

    # Find all markdown files
    markdown_files = file_processor.find_markdown_files(directory)

    updated_files = 0
    changes_found = 0

    for filepath in markdown_files:
        if file_processor.should_skip_file(filepath):
            continue

        content = file_processor.read_file_content(filepath)
        if content is None:
            continue

        updated_content, was_changed = transform_tags_in_content(
            content, tag_transformer, logger
        )

        if was_changed:
            changes_found += 1

            if dry_run:
                logger.info(f"Would update {filepath}")
                logger.debug("  Tag transformation would be applied")
            else:
                if file_processor.write_file_content(filepath, updated_content):
                    updated_files += 1
                    logger.info(f"Updated tags in {filepath}")

    # Final summary
    if dry_run:
        logger.info(
            f"Dry run complete! Found {changes_found} files that would be updated."
        )
    else:
        logger.info(f"Finished {operation_name}! Updated {updated_files} files.")

    return {
        "files_processed": len(markdown_files),
        "files_updated": updated_files,
        "changes_found": changes_found,
        "operation": operation_name,
        "dry_run": dry_run,
    }


# ============================================================================
# Operation-Specific Functions
# ============================================================================


def replace_spaces_in_tags(
    directory: str,
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
    max_file_size_mb: int = MAX_FILE_SIZE_MB,
) -> dict:
    """Replace spaces with hyphens in tags."""

    def space_replacer(tag: str) -> str:
        return tag.replace(" ", "-")

    return process_tags(
        directory,
        space_replacer,
        "space replacement",
        dry_run,
        verbose,
        quiet,
        max_file_size_mb,
    )


def convert_tags_to_lowercase(
    directory: str,
    dry_run: bool = False,
    verbose: bool = False,
    quiet: bool = False,
    max_file_size_mb: int = MAX_FILE_SIZE_MB,
) -> dict:
    """Convert tags to lowercase."""
    return process_tags(
        directory,
        str.lower,
        "lowercase conversion",
        dry_run,
        verbose,
        quiet,
        max_file_size_mb,
    )


# ============================================================================
# Main Entry Point
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Process tags in markdown files frontmatter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s replace-spaces                    # Replace spaces in current directory
  %(prog)s lowercase /path/to/notes          # Convert to lowercase in specific directory
  %(prog)s replace-spaces --dry-run          # Preview changes without applying them
  %(prog)s lowercase ~/notes --dry-run       # Preview lowercase conversion
        """,
    )

    parser.add_argument(
        "operation",
        choices=[op.value for op in Operation],
        help="Operation to perform on tags",
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=os.getcwd(),
        help="Directory to search for markdown files (default: current directory)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress non-error output"
    )

    parser.add_argument(
        "--max-file-size",
        type=int,
        default=MAX_FILE_SIZE_MB,
        help=f"Maximum file size in MB to process (default: {MAX_FILE_SIZE_MB}MB)",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.verbose and args.quiet:
        print("Error: Cannot specify both --verbose and --quiet options.")
        sys.exit(1)

    # Validate directory exists
    directory_path = Path(args.directory).expanduser()
    if not directory_path.is_dir():
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)

    directory = str(directory_path)

    if not args.quiet:
        print(f"Processing markdown files in: {directory}")
        if args.dry_run:
            print("DRY RUN MODE - No files will be modified")
        print()

    result = None
    if args.operation == Operation.REPLACE_SPACES.value:
        result = replace_spaces_in_tags(
            directory, args.dry_run, args.verbose, args.quiet, args.max_file_size
        )
    elif args.operation == Operation.LOWERCASE.value:
        result = convert_tags_to_lowercase(
            directory, args.dry_run, args.verbose, args.quiet, args.max_file_size
        )

    if args.verbose and not args.quiet and result:
        print(f"\nSummary: {result}")


if __name__ == "__main__":
    main()
