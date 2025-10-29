#!/usr/bin/env python3

# This is supposed to separate logical compounds of python code with empty lines above and below
# But it's not working correctly yet since it inserts at wrong places

import sys
import tokenize
import io
import re
from pathlib import Path


class CompoundGroupFormatter:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            self.content = f.read()
        self.lines = self.content.split("\n")

    def is_compound_chain_keyword(self, line: str) -> bool:
        """Check if line starts with else, elif, except, finally."""
        stripped = line.strip()
        return any(
            stripped.startswith(kw)
            for kw in ("else:", "elif ", "except:", "except ", "finally:")
        )

    def is_closing_bracket_only(self, line: str) -> bool:
        """Check if line is only closing brackets."""
        stripped = line.strip()
        return stripped and all(c in ")}],:;" for c in stripped)

    def is_comment_only(self, line: str) -> bool:
        """Check if line is only a comment."""
        stripped = line.strip()
        return stripped.startswith("#")

    def is_compound_header_line(self, line: str) -> bool:
        """True if line starts a new block (if/for/while/try/with/def/class/except/else/elif/finally)."""
        stripped = line.strip()
        if not stripped.endswith(":"):
            return False
        # Quick keyword check to avoid false positives
        starters = (
            "if ",
            "for ",
            "while ",
            "try:",
            "with ",
            "def ",
            "class ",
            "else:",
            "elif ",
            "except",
            "finally:",
        )
        return any(stripped.startswith(s) for s in starters)

    def starts_header_prefix(self, line: str) -> bool:
        """True if line begins a header keyword sequence even if not ending with ':' yet.
        This helps detect multi-line headers like a long def signature or if condition spanning lines.
        """
        stripped = line.lstrip()
        prefixes = ("if ", "for ", "while ", "try", "with ", "def ", "class ", "elif ", "except", "else")
        return any(stripped.startswith(p) for p in prefixes)

    def is_decorator_line(self, line: str) -> bool:
        """True if the line is a decorator like @dataclass or @something."""
        return line.lstrip().startswith("@")

    def indent_of(self, line: str) -> int:
        return len(line) - len(line.lstrip())

    def assigned_name(self, line: str) -> str | None:
        """Return the variable name if line is a simple assignment like `name = ...`. Avoids walrus/equals comparisons."""
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*", line)
        if not m:
            return None
        # Exclude `==` or `:=` cases, already handled by regex but keep safe-guard
        if "==" in line or ":=" in line:
            return None
        return m.group(1)

    def header_uses_name(self, header_line: str, name: str) -> bool:
        """True if the header condition (text before colon) references the given name as a whole word."""
        stripped = header_line.strip()
        if not stripped.endswith(":"):
            return False
        cond = stripped[:-1]  # drop trailing colon
        return re.search(rf"\b{name}\b", cond) is not None

    def detect_multiline_bracket_groups(self, tokens: list[tokenize.TokenInfo]) -> list[tuple[int, int]]:
        """
        Return (start_line, end_line) for expressions that span multiple physical lines due to
        parentheses/brackets/braces. We only consider groups that start at base depth and
        close back to base depth on a later line.
        """
        groups: list[tuple[int, int]] = []
        depth = 0
        group_start_line: int | None = None

        for tok in tokens:
            tok_type, tok_string, start, end, _ = tok

            # Only consider operator tokens for brackets; strings/comments are ignored by tokenize here
            if tok_type != tokenize.OP:
                continue

            if tok_string in "([{":
                if depth == 0:
                    group_start_line = start[0]
                depth += 1
                continue

            if tok_string in ")]}":
                if depth > 0:
                    depth -= 1
                    if depth == 0 and group_start_line is not None:
                        end_line = end[0]
                        # Only treat as a group if it actually spans lines
                        if end_line > group_start_line:
                            groups.append((group_start_line, end_line))
                        group_start_line = None

        return groups

    def format(self) -> None:
        """Add blank lines between logical groups separated by compound statements."""
        new_lines = []

        try:
            tokens = list(tokenize.generate_tokens(io.StringIO(self.content).readline))
        except tokenize.TokenError:
            print(f"⚠ Skipping {self.file_path} (tokenization error)")
            return

        line_needs_blank_after = set()

        # Pass 0: detect multi-line bracketed expressions (e.g., function calls split across lines)
        # and ensure a single blank line before and after the group when surrounded by sibling code.
        groups = self.detect_multiline_bracket_groups(tokens)
        for start_line, end_line in groups:
            # Insert BEFORE the group (i.e., after the previous line), if previous line exists and is code
            if start_line > 1:
                prev_line = self.lines[start_line - 2]
                curr_start = self.lines[start_line - 1]

                if (
                    prev_line.strip()
                    and not self.is_comment_only(prev_line)
                    and not self.is_decorator_line(prev_line)
                    and not self.is_closing_bracket_only(prev_line)
                    and self.indent_of(prev_line) == self.indent_of(curr_start)
                ):
                    line_needs_blank_after.add(start_line - 1)

            # Insert AFTER the group, if next line exists and is code, but avoid separating
            # a multi-line header (def/if/etc) from its body. We can detect that either
            # the group starts with a header prefix or the following line is more indented than the group's start.
            if end_line < len(self.lines):
                next_line = self.lines[end_line]

                group_first_line = self.lines[start_line - 1]
                start_indent = self.indent_of(group_first_line)

                # If this looks like a multi-line header, don't add a blank after it
                looks_like_header = self.starts_header_prefix(group_first_line)

                # If next line is more indented, it's likely the body of the header; don't separate
                next_indent = self.indent_of(next_line)

                if (
                    next_line.strip()
                    and not self.is_comment_only(next_line)
                    and not self.is_compound_header_line(next_line)
                    and not looks_like_header
                    and not (next_indent > start_indent)
                ):
                    line_needs_blank_after.add(end_line)

        for i, token in enumerate(tokens):
            tok_type, tok_string, start, end, line = token

            # Detect dedenting (going back to lower indentation)
            if tok_type == tokenize.DEDENT:
                dedent_line = start[0] - 1

                # Look back to find the line before dedent
                if dedent_line > 0:
                    # Check if next line (at dedent position) is a compound chain keyword
                    if dedent_line < len(self.lines):
                        next_line = self.lines[dedent_line]
                        # Skip if next line is else/elif/except/finally, closing bracket, or comment
                        # Also skip if the previous line is a comment (don't add blanks between comments)
                        if dedent_line > 0:
                            prev_line = self.lines[dedent_line - 1]
                            if self.is_comment_only(prev_line):
                                continue

                        # We want a blank line unless the next line is a chain keyword or a closing bracket-only line.
                        # If the next line is a comment, we still want a separating blank line before that comment.
                        if not (
                            self.is_compound_chain_keyword(next_line)
                            or self.is_closing_bracket_only(next_line)
                        ):
                            line_needs_blank_after.add(dedent_line - 1)

        # Second pass: insert a blank line before a section-starting comment inside the same block.
        # If a code line is immediately followed by a comment line (and there's no blank line already),
        # and that comment is followed by code (i.e., it's a section header comment), add a blank line.
        for idx in range(1, len(self.lines)):
            prev_line = self.lines[idx - 1]
            curr_line = self.lines[idx]

            # Only consider transitions from code -> comment with no blank line already
            if (
                prev_line.strip()
                and not self.is_comment_only(prev_line)
                and not self.is_closing_bracket_only(prev_line)
                and not self.is_compound_header_line(prev_line)  # don't add after headers like `if:`
            ):
                if curr_line.strip() and self.is_comment_only(curr_line):
                    # Ensure there isn't already a blank line (we checked curr_line is non-empty)
                    # Peek ahead to see if the comment is followed by code (skip consecutive comments)
                    j = idx + 1
                    while j < len(self.lines) and self.is_comment_only(self.lines[j]):
                        j += 1
                    if j < len(self.lines) and self.lines[j].strip():
                        # Mark to insert a blank line after prev_line
                        line_needs_blank_after.add(idx)

        # Third pass: ensure a blank line BEFORE a new compound header (e.g., `if:`)
        # when the previous line is a non-comment, non-empty code line.
        for idx in range(1, len(self.lines)):
            curr_line = self.lines[idx]
            prev_line = self.lines[idx - 1]

            if not self.is_compound_header_line(curr_line):
                continue

            # Do not separate chained headers like else/elif/except/finally
            if self.is_compound_chain_keyword(curr_line):
                continue

            # If previous line is empty, there is already a separation
            if not prev_line.strip():
                continue

            # Do not insert between a documentation comment and its header
            if self.is_comment_only(prev_line):
                continue

            # Do not insert after closing bracket-only lines
            if self.is_closing_bracket_only(prev_line):
                continue

            # Do not separate decorators from their header
            if self.is_decorator_line(prev_line):
                continue

            # Only separate sibling groups (same indentation level)
            if self.indent_of(prev_line) != self.indent_of(curr_line):
                continue

            # Heuristic: if previous line assigns a variable and this header immediately tests it,
            # treat them as a tight pair (no separation).
            prev_assigned = self.assigned_name(prev_line)
            if prev_assigned and self.header_uses_name(curr_line, prev_assigned):
                continue

            # Insert a blank line BEFORE the header by marking an insertion AFTER the previous line
            line_needs_blank_after.add(idx)

        # Rebuild lines with added blank lines
        for line_num, line in enumerate(self.lines, start=1):
            new_lines.append(line)

            # Add blank line if needed and not already present
            if line_num in line_needs_blank_after:
                # Check if next line is empty
                if line_num < len(self.lines):
                    next_line = self.lines[line_num].strip()
                    # Only add if next line is not empty
                    if next_line:
                        new_lines.append("")

        result = "\n".join(new_lines)
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✓ Formatted {self.file_path}")


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {Path(__file__).name} <python_file_or_directory>")
        sys.exit(1)

    for path_str in sys.argv[1:]:
        path = Path(path_str)

        if path.is_file() and path.suffix == ".py":
            CompoundGroupFormatter(str(path)).format()
        elif path.is_dir():
            for py_file in path.rglob("*.py"):
                CompoundGroupFormatter(str(py_file)).format()
        else:
            print(f"⚠ Skipping {path} (not a Python file)")


if __name__ == "__main__":
    main()
