from __future__ import annotations

# Standard
import re
from typing import Any, ClassVar
from dataclasses import dataclass

# Modules
from .args import args
from .config import config
from .output import Output
from .utils import utils
from .widgets import widgets


@dataclass
class SnippetMatch:
    start_line: str
    end_line: str
    language: str
    line_num: int


@dataclass
class MatchItem:
    def __init__(self, line: int, items: list[re.Match[Any]]) -> None:
        self.line = line
        self.items = items


@dataclass
class IndexItem:
    def __init__(self, start: str, end: str, content: str) -> None:
        self.start = start
        self.end = end
        self.content = content


class Markdown:
    separator = "───────────────────"
    marker_indent_ordered = "\u200b\u200c\u200b"
    marker_indent_unordered = "\u200c\u200b\u200c"
    urls: ClassVar[dict[str, str]] = {}

    pattern_snippets: str
    pattern_bold_aster: str
    pattern_bold_under: str
    pattern_italic_aster: str
    pattern_italic_under: str
    pattern_highlight: str
    pattern_uselink: str
    pattern_quote: str
    pattern_url: str
    pattern_link: str
    pattern_path: str
    pattern_header_1: str
    pattern_header_2: str
    pattern_header_3: str
    pattern_separator: str
    pattern_list_ordered: str
    pattern_list_unordered: str

    @staticmethod
    def build_patterns() -> None:
        protocols_list = ["https://", "http://", "www.", "ftp://", "sftp://", "ssh://"]
        protocols_string = Markdown.escape_chars(protocols_list, "|")
        protocols = rf"({protocols_string})"

        tick = utils.escape_regex("`")
        hash_ = utils.escape_regex("#")
        uselink = utils.escape_regex("%@")

        def get_u(c: str, n: int) -> str:
            return f"{c}{{{n}}}"

        def get_t(c: str, n: int) -> str:
            u = get_u(c, n)
            return rf"(?:(?!{u}|\s).)"

        def get_t2(c: str, n: int) -> str:
            u = get_u(c, n)
            return rf"(?:(?!{u}).)"

        # *this thing* but not *this thing * and not math operations like 2*3
        # No spaces between the chars
        def char_regex_1(char: str, n: int = 1) -> str:
            c = utils.escape_regex(char)
            u = get_u(c, n)
            t = get_t(c, n)
            t2 = get_t2(c, n)

            if char == "*":
                # Special case for asterisk to avoid matching math operations
                return rf"(?P<all>(?<!\d){u}(?P<content>{t}{t2}*{t}|{t}){u}(?!\d))"

            # Original pattern for other characters
            return rf"(?P<all>{u}(?P<content>{t}{t2}*{t}|{t}){u})"

        # _this thing_ but not_this_thing
        # Chars have to be at the edges
        def char_regex_2(char: str, n: int = 1) -> str:
            c = utils.escape_regex(char)
            u = get_u(c, n)
            t = get_t(c, n)
            return rf"(?:^|\s)(?P<all>{u}(?P<content>{t}.*?{t}|{t}){u})(?:$|\s)"

        # `this thing` or ` this thing `
        # There can be spaces between the chars
        def char_regex_3(char: str, n: int = 1) -> str:
            c = utils.escape_regex(char)
            u = get_u(c, n)
            t2 = get_t2(c, n)
            return rf"(?P<all>{u}(?P<content>{t2}+){u})"

        # Italic with one asterisk
        Markdown.pattern_italic_aster = char_regex_1("*")

        # Bold with two asterisks
        Markdown.pattern_bold_aster = char_regex_1("*", 2)

        # Italic with one underscore
        Markdown.pattern_italic_under = char_regex_2("_")

        # Bold with two underscores
        Markdown.pattern_bold_under = char_regex_2("_", 2)

        # Highlight with one backtick
        Markdown.pattern_highlight = char_regex_3("`")

        # Highlight with one double-quote
        Markdown.pattern_quote = char_regex_1('"')

        # Code snippets / fences
        # Capture stuff that could repeat BUT that has the slim
        # possibility of catastrophically backtracking in case
        # the stuff AFTER it fails to match (such as the closing
        # 3x backticks).
        Markdown.pattern_snippets = rf"^{tick}{{3}}([-\w.# ]*)(?:\n|{tick}{{3}})(?=((?:[^{tick}]+|(?!^{tick}{{3}}){tick}{{1,2}}|(?!{tick}{{3}}[^{tick}]){tick}{{3}})*))\2(?:{tick}{{3}}|$)\s*$"

        # Uselink with the special chars
        Markdown.pattern_uselink = char_regex_1(uselink)

        # URLs with http:// | https:// | ftp:// | www.
        Markdown.pattern_url = (
            rf"(?:(?<=\s)|^)(?P<all>(?P<content>({protocols})([^\s]+?)))(?=\s|$)"
        )

        # Unix paths like /home/user/file.txt
        Markdown.pattern_path = r"(?:(?<=\s)|^)(?P<all>(?P<content>(\/|~\/)[^\s\/]+\/[^\s\/]+[^\s]*))(?=\s|$)"

        # Header with one hash
        Markdown.pattern_header_1 = rf"^(?P<all>{hash_}{{1}}\s+(?P<content>.*))$"

        # Header with two hashes
        Markdown.pattern_header_2 = rf"^(?P<all>{hash_}{{2}}\s+(?P<content>.*))$"

        # Header with three hashes
        Markdown.pattern_header_3 = rf"^(?P<all>{hash_}{{3}}\s+(?P<content>.*))$"

        # Separator line
        Markdown.pattern_separator = r"^-{3,}$"

        # Bullet list (ordered)
        Markdown.pattern_list_ordered = (
            r"(^|(?<=\n\n)) *\d+[.)] [^\n]+(?:\n{1,2}[ \t]*\d+[.)] [^\n]+)*"
        )

        # Bullet list (unordered)
        Markdown.pattern_list_unordered = (
            r"(^|(?<=\n\n)) *[*-] [^\n]+(?:\n{1,2}[ \t]*[*-] [^\n]+)*"
        )

        # Word URL like [Click here](https://example.com)
        Markdown.pattern_link = (
            r"(?:^|\s)(?P<all>\[(?P<content>[^\]]+)\]\((?P<url>[^\)]+)\))(?:$|\s)"
        )

    @staticmethod
    def escape_chars(chars: list[str], separator: str = "") -> str:
        clean = [utils.escape_regex(c) for c in chars]
        return separator.join(clean)

    @staticmethod
    def get_url_id(url: str) -> str | None:
        for id_, value in Markdown.urls.items():
            if value == url:
                return id_

        return None

    @staticmethod
    def get_url(url_id: str) -> str | None:
        url_id = url_id.replace("link_", "")
        return Markdown.urls.get(url_id)

    def __init__(self, widget: Output) -> None:
        self.widget = widget

        self.not_nobody = [
            "clean",
            "join",
            "ordered",
            "unordered",
        ]

    def format_all(self) -> None:
        start_ln = 1
        end_ln = self.last_line()
        self.format_section("nobody", start_ln, end_ln)
        self.indent_lines()

    def format_last(self) -> None:
        start_ln = int(self.widget.index("end - 1l").split(".")[0])
        end_ln = self.last_line()
        self.format_section("nobody", start_ln, end_ln)
        self.indent_lines()

    def format(self) -> None:
        if args.markdown == "none":
            return

        markers = self.widget.get_markers()
        ranges: list[tuple[str, int, int]] = []

        def add(who: str, start_ln: int, end_ln: int) -> None:
            if (not ranges) and (start_ln > 1):
                ranges.append(("nobody", 1, start_ln - 1))

            ranges.append((who, start_ln, end_ln))

        for i, item in enumerate(markers):
            who = item["who"]

            if args.markdown != "both":
                if args.markdown == "user":
                    if who != "user":
                        continue
                elif args.markdown == "ai":
                    if who != "ai":
                        continue

            start_ln = item["line"]

            if i < (len(markers) - 1):
                end_ln = int(markers[i + 1]["line"] - 1)
            else:
                end_ln = self.last_line()

            add(who, start_ln, end_ln)

        for who, start_ln, end_ln in reversed(ranges):
            self.format_section(who, start_ln, end_ln)

        self.indent_lines()

    def enabled(self, who: str, what: str) -> bool:
        if who == "nobody":
            return what not in self.not_nobody

        name = f"markdown_{what}"

        if not hasattr(args, name):
            return True

        arg = getattr(args, name)

        if arg == "none":
            return False

        if arg == "both":
            return True

        if arg == "user":
            return who == "user"

        if arg == "ai":
            return who == "ai"

        return False

    def format_section(self, who: str, start_ln: int, end_ln: int) -> None:
        if self.enabled(who, "think"):
            if self.replace_think(start_ln, end_ln, who):
                end_ln = self.next_marker(start_ln)

        if self.enabled(who, "roles"):
            if self.replace_roles(start_ln, end_ln, who):
                end_ln = self.next_marker(start_ln)

        if self.enabled(who, "clean"):
            if self.clean_lines(start_ln, end_ln, who):
                end_ln = self.next_marker(start_ln)

        if self.enabled(who, "join"):
            if self.join_lines(start_ln, end_ln, who):
                end_ln = self.next_marker(start_ln)

        if self.enabled(who, "snippets"):
            snip_done, _ = self.format_snippets(start_ln, end_ln, who)

            if snip_done:
                end_ln = self.next_marker(start_ln) - 1

        # Lists

        if self.enabled(who, "ordered"):
            if self.format_lists(start_ln, end_ln, who, "ordered"):
                end_ln = self.next_marker(start_ln)

        if self.enabled(who, "unordered"):
            if self.format_lists(start_ln, end_ln, who, "unordered"):
                end_ln = self.next_marker(start_ln)

        # Bold (two chars)

        if self.enabled(who, "bold_asterisk"):
            self.do_format(start_ln, end_ln, who, Markdown.pattern_bold_aster, "bold")

        if self.enabled(who, "bold_underscore"):
            self.do_format(start_ln, end_ln, who, Markdown.pattern_bold_under, "bold")

        # Italic (one char)

        if self.enabled(who, "italic_asterisk"):
            self.do_format(
                start_ln, end_ln, who, Markdown.pattern_italic_aster, "italic"
            )

        if self.enabled(who, "italic_underscore"):
            self.do_format(
                start_ln, end_ln, who, Markdown.pattern_italic_under, "italic"
            )

        # ---

        if self.enabled(who, "quote"):
            self.do_format(start_ln, end_ln, who, Markdown.pattern_quote, "quote", True)

        if self.enabled(who, "highlight"):
            self.do_format(
                start_ln, end_ln, who, Markdown.pattern_highlight, "highlight"
            )

        self.do_format(start_ln, end_ln, who, Markdown.pattern_uselink, "uselink")

        if self.enabled(who, "link"):
            self.do_format(start_ln, end_ln, who, Markdown.pattern_link, "link")

        if self.enabled(who, "url"):
            self.do_format(start_ln, end_ln, who, Markdown.pattern_url, "url")

        if self.enabled(who, "path"):
            self.do_format(start_ln, end_ln, who, Markdown.pattern_path, "path")

        if self.enabled(who, "header"):
            self.do_format(start_ln, end_ln, who, Markdown.pattern_header_1, "header_1")
            self.do_format(start_ln, end_ln, who, Markdown.pattern_header_2, "header_2")
            self.do_format(start_ln, end_ln, who, Markdown.pattern_header_3, "header_3")

        if self.enabled(who, "separator"):
            self.format_separators(start_ln, end_ln, who)

    def do_format(
        self,
        start_ln: int,
        end_ln: int,
        who: str,
        pattern: str,
        tag: str,
        no_replace: bool = False,
    ) -> None:
        matches: list[MatchItem] = []
        lines = self.get_lines(start_ln, end_ln, who)

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            match_ = MatchItem(start_ln + i, list(re.finditer(pattern, line)))

            if match_.items:
                matches.append(match_)

        for mtch in reversed(matches):
            items = mtch.items
            indices: list[IndexItem] = []
            url = ""

            for item in reversed(items):
                all_ = item.group("all")

                if no_replace:
                    content = all_
                else:
                    content = item.group("content")

                if tag == "link":
                    url = item.group("url")

                search_col = 0

                if tag == "header_3":
                    pass

                for _ in range(999):
                    start = self.widget.search(
                        all_,
                        f"{mtch.line}.{search_col}",
                        stopindex=f"{mtch.line}.end",
                    )

                    if not start:
                        break

                    repeated = False

                    for index in indices:
                        if (index.start == start) and (index.content == content):
                            search_col = int(start.split(".")[1]) + len(all_)
                            repeated = True

                    if repeated:
                        continue

                    end = self.widget.index(f"{start} + {len(all_)}c")

                    if not end:
                        break

                    indices.append(IndexItem(start, end, content))

            sorted_indices = sorted(
                indices, key=lambda x: int(x.start.split(".")[1]), reverse=True
            )

            tag2 = ""

            if tag == "link":
                url_id = Markdown.get_url_id(url)

                if not url_id:
                    url_id = f"url_{len(Markdown.urls)}"
                    Markdown.urls[url_id] = url

                tag2 = f"{tag}_{url_id}"

            for index_item in sorted_indices:
                self.widget_delete(
                    "do_format",
                    index_item.start,
                    index_item.end,
                )

                self.widget_insert(
                    "do_format",
                    index_item.start,
                    index_item.content,
                )

                self.widget.tag_add(
                    tag,
                    index_item.start,
                    f"{index_item.start} + {len(index_item.content)}c",
                )

                if tag2:
                    self.widget.tag_add(
                        tag2,
                        index_item.start,
                        f"{index_item.start} + {len(index_item.content)}c",
                    )

    def format_snippets(self, start_ln: int, end_ln: int, who: str) -> tuple[bool, int]:
        from .snippet import Snippet

        clines = self.get_lines(start_ln, end_ln, who)
        ctext = "\n".join(clines)
        num_lines = end_ln - start_ln
        matches = []

        for match_ in re.finditer(
            Markdown.pattern_snippets, ctext, flags=re.MULTILINE | re.DOTALL
        ):
            language = match_.group(1)
            content = match_.group(2)

            # Determine whether this is an inline fenced snippet like ```something here```
            # In that case, group(1) was mistakenly captured as the language; treat it as content.
            try:
                open_ticks_end = match_.start(0) + 3  # position right after opening ```
                # Next character after the "language" capture
                after_lang_idx = open_ticks_end + (len(language) if language else 0)
                next_char = ctext[after_lang_idx : after_lang_idx + 1]
                is_inline_snippet = next_char != "\n"
            except Exception:
                is_inline_snippet = False

            if is_inline_snippet:
                # Swap: group(1) is actually the inline content and no language is specified
                content = language or ""
                language = ""

            full_match_start_idx = match_.start(0)
            full_match_end_idx = match_.end(0)

            # Determine the real start and end line numbers in the widget
            start_line_num_in_ctext = self.get_line_number(ctext, full_match_start_idx)
            real_start_line = start_ln + start_line_num_in_ctext - 1

            end_line_num_in_ctext = self.get_line_number(ctext, full_match_end_idx)
            real_end_line = start_ln + end_line_num_in_ctext - 1

            # Determine the character indices for deletion
            # For multi-line, we delete whole lines. For single-line, we use char indices.
            if real_start_line != real_end_line:
                # Multi-line block
                start_index = f"{real_start_line}.0"
                end_index = f"{real_end_line}.end"
            else:
                # Single-line block
                start_char_index = full_match_start_idx - ctext.rfind('\n', 0, full_match_start_idx) - 1
                end_char_index = full_match_end_idx - ctext.rfind('\n', 0, full_match_end_idx) - 1
                start_index = f"{real_start_line}.{start_char_index}"
                end_index = f"{real_end_line}.{end_char_index}"

            match = SnippetMatch(start_index, end_index, language, real_start_line)
            match.content = content
            matches.append(match)

        # Iterate in reverse to avoid messing up indices
        for match in reversed(matches):

            # Check for any non-whitespace characters before the start of our match on the same line
            # If present, ensure there is exactly ONE blank line separating text and the snippet widget
            line_start_index = match.start_line.split('.')[0]
            text_before = self.widget.get(f"{line_start_index}.0", match.start_line).strip()
            is_inline_start = bool(text_before)

            # Now, delete the ENTIRE ```...``` block
            self.widget_delete("snippets", match.start_line, match.end_line)

            # If the snippet was inline (same line start/end), capture and move trailing text
            start_line_num = int(match.start_line.split('.')[0])
            end_line_num = int(match.end_line.split('.')[0])
            same_line = start_line_num == end_line_num

            trailing_text = ""
            if same_line:
                trailing_text = self.widget.get(match.end_line, f"{end_line_num}.end")
                if trailing_text:
                    # Delete trailing text from the original line; we'll re-insert it after the widget
                    self.widget_delete("snippets", match.end_line, f"{end_line_num}.end")

            # Determine where to insert the widget
            insertion_line = match.line_num
            if is_inline_start:
                # Ensure a blank line between the text line and the snippet widget
                # Create exactly one empty line after the current line
                self.widget_insert("snippets", f"{insertion_line}.end", "\n")
                insertion_line += 2  # widget goes two lines below the original text line
            else:
                # Ensure exactly one empty line ABOVE the widget
                above_idx = insertion_line - 1
                if above_idx >= 1:
                    above_line = self.widget.get(f"{above_idx}.0", f"{above_idx}.end")
                    if above_line.strip() != "":
                        self.widget_insert("snippets", f"{above_idx}.end", "\n")
                        insertion_line += 1

            # Create and insert the snippet widget
            snippet = Snippet(self.widget, match.content, match.language)
            widgets.window(self.widget, insertion_line, snippet)
            self.widget.snippets.append(snippet)

            # Ensure exactly one empty line AFTER the widget
            after_idx = insertion_line + 1
            after_line = self.widget.get(f"{after_idx}.0", f"{after_idx}.end")
            if after_line.strip() != "":
                self.widget_insert("snippets", f"{after_idx}.0", "\n")

            # If there was trailing text in an inline snippet, put it after the blank line
            if same_line and trailing_text.strip():
                self.widget_insert("snippets", f"{insertion_line + 2}.0", trailing_text)

        return len(matches) > 0, num_lines

    def format_lists(self, start_ln: int, end_ln: int, who: str, mode: str) -> bool:
        lines = self.get_lines(start_ln, end_ln, who)
        text = "\n".join(lines)
        matches = []

        if mode == "ordered":
            pattern = Markdown.pattern_list_ordered
        else:
            pattern = Markdown.pattern_list_unordered

        for match_ in re.finditer(pattern, text, flags=re.MULTILINE | re.DOTALL):
            content_start = match_.start(0)
            line_1 = self.get_line_number(text, content_start)
            start_line = f"{start_ln + line_1}.0"

            content_end = match_.end(0)
            line_2 = self.get_line_number(text, content_end)
            end_line = f"{start_ln + line_2}.0"

            matches.append((start_line, end_line, content_start, match_.group(0)))

        len_matches = len(matches)

        for start_line, end_line, content_start, mtch in reversed(matches):
            line_1 = text[:content_start].count("\n")
            line_2 = len(mtch.split("\n"))
            line_end = line_1 + line_2
            sliced = lines[line_1:line_end]
            sliced = [line.strip() for line in sliced]
            spacing_mode = getattr(args, f"{mode}_spacing")
            marker = getattr(self, f"marker_indent_{mode}")

            if spacing_mode == "never":
                spaced = False
            elif spacing_mode == "always":
                spaced = True
            else:
                spaced = not all(line.strip() for line in sliced)

            space_1 = ""

            if config.font_family == "monospace":
                space_2 = " "
            else:
                space_2 = "  "

            if (mode == "ordered") and (len(sliced) > 1):
                n = 1
                char = args.ordered_char.rstrip()
                items = []

                for line in sliced:
                    if re.match(r"^\d+", line):
                        left = f"{space_1}{n}{char}{space_2}"
                        c_line = re.sub(r"^\d+[.)]", "", line).strip()
                        items.append(f"{marker}{left}{c_line}")
                        n += 1
            else:
                char = args.unordered_char.rstrip()
                items = []

                for line in sliced:
                    if line.startswith(("*", "-")):
                        left = f"{space_1}{char}{space_2}"
                        c_line = line[2:].strip()
                        items.append(f"{marker}{left}{c_line}")

            if len(items) == 0:
                len_matches -= 1
                continue

            if spaced:
                txt = "\n\n".join(items)
            else:
                txt = "\n".join(items)

            content_below = self.widget.get(
                f"{end_line} +1 lines linestart", f"{end_line} +1 lines lineend"
            ).strip()

            if content_start == 0:
                end_of_line_above = f"{start_line} lineend"
                chars = len(lines[0])
                right_bit = f"{end_of_line_above} -{chars} chars"

                self.widget_delete(
                    "lists",
                    right_bit,
                    end_of_line_above,
                )

                self.widget_insert(
                    "lists",
                    end_of_line_above,
                    "\n\n\n",
                )

                self.widget_delete(
                    "lists",
                    f"{start_line} +1 lines",
                    f"{end_line} +3 lines lineend",
                )

                txt = f"\n{txt}"

                if content_below:
                    txt += "\n"

                self.widget_insert(
                    "lists",
                    f"{start_line} +1 lines",
                    txt,
                )
            else:
                content_above = self.widget.get(
                    f"{start_line} - 1 lines linestart",
                    f"{start_line} - 1 lines lineend",
                ).strip()

                if content_above:
                    txt = f"\n{txt}"

                if content_below:
                    txt += "\n"

                self.widget_delete(
                    "lists",
                    f"{start_line} linestart",
                    f"{end_line} lineend",
                )

                self.widget_insert(
                    "lists",
                    start_line,
                    txt,
                )

        return len_matches > 0

    def format_separators(self, start_ln: int, end_ln: int, who: str) -> None:
        matches = []
        lines = self.get_lines(start_ln, end_ln, who)

        for i, line in enumerate(lines):
            if re.match(Markdown.pattern_separator, line):
                matches.append(i)

        for i in reversed(matches):
            self.widget_delete(
                "separators",
                f"{start_ln + i}.0",
                f"{start_ln + i}.end",
            )

            self.widget_insert(
                "separators",
                f"{start_ln + i}.0",
                Markdown.separator,
            )

            self.widget.tag_add(
                "separator",
                f"{start_ln + i}.0",
                f"{start_ln + i}.0 + {len(Markdown.separator)}c",
            )

    def get_lines(self, start_ln: int, end_ln: int, who: str) -> list[str]:
        text = self.widget.get(f"{start_ln}.0", f"{end_ln}.end")
        lines = text.split("\n")
        _, end_col = self.prompt_cols(start_ln)

        if who in ("user", "ai"):
            line = lines[0][end_col - 1 :].lstrip()
            lines[0] = line

        return lines

    def get_line_number(self, text: str, index: int) -> int:
        return text.count("\n", 0, index)

    def next_marker(self, start_ln: int) -> int:
        markers = self.widget.get_markers(True, append=False)

        for i, marker in enumerate(markers):
            if marker["line"] == start_ln:
                if i < len(markers) - 1:
                    return int(markers[i + 1]["line"] - 1)

        return self.last_line()

    def last_line(self) -> int:
        return int(self.widget.index("end").split(".")[0])

    def prompt_cols(self, start_ln: int) -> tuple[int, int]:
        d = utils.delimiter()
        marker = Output.marker_space
        end = f"{marker}{d}{marker}"
        start = self.widget.search(end, f"{start_ln}.0", stopindex=f"{start_ln}.end")

        if not start:
            return 0, 0

        start_col = int(start.split(".")[1])
        end_col = start_col + len(end)
        return 0, end_col

    def insert_first(self, start_ln: int, end_ln: int, text: str) -> None:
        _, end_col = self.prompt_cols(start_ln)

        self.widget_delete(
            "first",
            f"{start_ln}.{end_col}",
            f"{end_ln}.end",
        )

        self.widget_insert(
            "first",
            f"{start_ln}.{end_col + 1}",
            text,
        )

    def indent_lines(self) -> None:
        lines = self.widget.get("1.0", "end").split("\n")

        def get_lns(marker: str) -> list[int]:
            return [i + 1 for i, line in enumerate(lines) if line.startswith(marker)]

        def add_tags(lns: list[int], name: str) -> None:
            for line in lns:
                ln = f"{line}.0"
                self.widget.tag_add(name, ln, f"{ln} lineend")

                try:
                    space = lines[line - 1].index(" ")
                    ln = f"{line}.0"
                    ln_end = f"{line}.{space}"
                    self.widget.tag_add("list", ln, ln_end)
                except BaseException:
                    pass

        or_lines = get_lns(Markdown.marker_indent_ordered)
        add_tags(or_lines, "indent_ordered")

        un_lines = get_lns(Markdown.marker_indent_unordered)
        add_tags(un_lines, "indent_unordered")

    def join_lines(self, start_ln: int, end_ln: int, who: str) -> bool:
        lines = self.get_lines(start_ln, end_ln, who)
        lines = [line.strip() for line in lines]
        joined_lines = []
        current: list[str] = []
        inside_snippets = False
        char = args.join_lines_char
        ticks = "```"

        def do_join() -> None:
            nonlocal current

            if current:
                cleaned = [line for line in current if line.strip()]
                joined = f" {char} ".join(cleaned) + "\n"
                joined_lines.append(joined)
                current = []

        def do_add() -> None:
            nonlocal current

            if current:
                current.append("")
                joined_lines.extend(current)
                current = []

        for line in lines:
            if line.startswith(ticks):
                inside_snippets = not inside_snippets

                if inside_snippets:
                    do_join()
                else:
                    current.append(line)
                    do_add()
                    continue

            current.append(line)

        if inside_snippets:
            do_add()
        else:
            do_join()

        text = "\n".join(joined_lines).strip() + "\n"
        self.insert_first(start_ln, end_ln, text)
        return True

    def clean_lines(self, start_ln: int, end_ln: int, who: str) -> bool:
        lines = self.get_lines(start_ln, end_ln, who)
        lines = [line.strip() for line in lines]
        cleaned = []
        empty = False

        for line in lines:
            stripped = line.strip()

            if stripped == "":
                if not empty:
                    cleaned.append("")
                    empty = True
            else:
                cleaned.append(stripped)
                empty = False

        text = "\n".join(cleaned).strip() + "\n"
        self.insert_first(start_ln, end_ln, text)
        return True

    def replace_think(self, start_ln: int, end_ln: int, who: str) -> bool:
        lines = self.get_lines(start_ln, end_ln, who)
        new_lines = []
        started = False
        ended = False
        content = False
        no_think = False
        start = args.markdown_think_start
        end = args.markdown_think_end
        start_index = 0
        end_index = 0

        for i, line in enumerate(lines):
            if line == config.think_token_start:
                new_lines.append(f"{start}\n")
                start_index = i
                started = True
            elif line == config.think_token_end:
                if started and (not content):
                    no_think = True

                new_lines.append(f"\n{end}")
                end_index = i
                ended = True
            else:
                if started and (not ended) and line.strip():
                    content = True

                new_lines.append(line)

        if (not started) or (not ended):
            return False

        if no_think:
            new_lines = [
                line
                for i, line in enumerate(new_lines)
                if i != start_index and i != end_index
            ]

        if new_lines:
            text = "\n".join(new_lines)
            text = text.strip() + "\n"
            self.insert_first(start_ln, end_ln, text)
            return True

        return False

    def replace_roles(self, start_ln: int, end_ln: int, who: str) -> bool:
        lines = self.get_lines(start_ln, end_ln, who)
        new_lines = []
        user_text = args.role_user_text
        assistant_text = args.role_assistant_text
        system_text = args.role_system_text
        changed = False

        for line in lines:
            if line.startswith(config.role_user_token):
                new_lines.append(user_text)
                changed = True
            elif line.startswith(config.role_assistant_token):
                new_lines.append(assistant_text)
                changed = True
            elif line.startswith(config.role_system_token):
                new_lines.append(system_text)
                changed = True
            else:
                new_lines.append(line)

        if changed and new_lines:
            text = "\n".join(new_lines).strip() + "\n"
            self.insert_first(start_ln, end_ln, text)
            return True

        return False

    def widget_insert(self, where: str, *all_args: Any) -> None:
        self.widget.insert(*all_args)

    def widget_delete(self, where: str, *all_args: Any) -> None:
        self.widget.delete(*all_args)


Markdown.build_patterns()
