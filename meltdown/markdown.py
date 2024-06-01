# Standard
import re
from typing import Any

# Modules
from .args import args
from .output import Output
from .utils import utils


class MatchItem:
    def __init__(self, line: int, items: list[re.Match[Any]]) -> None:
        self.line = line
        self.items = items


class IndexItem:
    def __init__(self, start: str, end: str, content: str) -> None:
        self.start = start
        self.end = end
        self.content = content


class Markdown:
    def __init__(self, widget: Output) -> None:
        self.widget = widget

        chars_left = ["(", "[", "/"]
        left_string = self.escape_chars(chars_left, "|")
        left = rf"(?:(?<=\s)|^|{left_string})"

        chars_right = [".", ",", ";", "!", "?", ":", "/", ")", "]"]
        right_string = self.escape_chars(chars_right, "|")
        right = rf"(?=\s|$|{right_string})"

        protocols_list = ["http://", "https://", "www.", "ftp://", "sftp://", "ssh://"]
        protocols_string = self.escape_chars(protocols_list, "|")
        protocols = rf"({protocols_string})"

        self.separator = "───────────────────"
        self.marker_indent_ordered = "\u200b\u200c\u200b"
        self.marker_indent_unordered = "\u200c\u200b\u200c"

        aster = utils.escape_regex("*")
        under = utils.escape_regex("_")
        tick = utils.escape_regex("`")
        quote = utils.escape_regex('"')
        hash_ = utils.escape_regex("#")

        # Code snippets / fences
        self.pattern_snippets = rf"{tick}{{3}}([-\w.#]*)\n(.*?)\n{tick}{{3}}$"

        # Bold with two asterisks
        self.pattern_bold_1 = (
            rf"{left}(?P<all>{aster}{{2}}(?P<content>.*?){aster}{{2}}){right}"
        )

        # Italic with one asterisk
        self.pattern_italic_1 = (
            rf"{left}(?P<all>{aster}{{1}}(?P<content>.*?){aster}{{1}}){right}"
        )

        # Italic with one underscore
        self.pattern_italic_2 = (
            rf"{left}(?P<all>{under}{{1}}(?P<content>.*?){under}{{1}}){right}"
        )

        # Highlight with three backticks
        self.pattern_highlight_1 = (
            rf"{left}(?P<all>{tick}{{3}}(?P<content>.*?){tick}{{3}}){right}"
        )

        # Highlight with two backticks
        self.pattern_highlight_2 = (
            rf"{left}(?P<all>{tick}{{2}}(?P<content>.*?){tick}{{2}}){right}"
        )

        # Highlight with one backtick
        self.pattern_highlight_3 = (
            rf"{left}(?P<all>{tick}{{1}}(?P<content>.*?){tick}{{1}}){right}"
        )

        # Highlight with one double-quote
        self.pattern_quote = (
            rf"{left}(?P<all>{quote}{{1}}(?P<content>.*?){quote}{{1}}){right}"
        )

        # URLs with http:// | https:// | ftp:// | www.
        self.pattern_url = (
            rf"(?:(?<=\s)|^)(?P<all>(?P<content>({protocols})([^\s]+?)))(?=\s|$)"
        )

        # Unix paths like /home/user/file.txt
        self.pattern_path = r"(?:(?<=\s)|^)(?P<all>(?P<content>\/[^\s]*))(?=\s|$)"

        # Header with three hashes
        self.pattern_header_1 = rf"^(?P<all>{hash_}{{3}}\s+(?P<content>.*))$"

        # Header with two hashes
        self.pattern_header_2 = rf"^(?P<all>{hash_}{{2}}\s+(?P<content>.*))$"

        # Header with one hash
        self.pattern_header_3 = rf"^(?P<all>{hash_}{{1}}\s+(?P<content>.*))$"

        # Separator line
        self.pattern_separator = r"^-{3,}$"

        # Bullet list (ordered)
        self.pattern_list_ordered = (
            r"(^|(?<=\n\n))\d+[.)] [^\n]+(?:\n{1,2}[ \t]*\d+[.)] [^\n]+)*"
        )

        # Bullet list (unordered)
        self.pattern_list_unordered = (
            r"(^|(?<=\n\n))[*-] [^\n]+(?:\n{1,2}[ \t]*[*-] [^\n]+)*"
        )

    def format_all(self) -> None:
        start_ln = 1
        end_ln = self.last_line()
        self.format_section("nobody", start_ln, end_ln)
        self.indent_lines()

    def format(self) -> None:
        if args.markdown == "none":
            return

        markers = self.widget.get_markers()
        ranges: list[tuple[str, int, int]] = []

        def add(who: str, start_ln: int, end_ln: int) -> None:
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

            if i < len(markers) - 1:
                end_ln = int(markers[i + 1]["line"] - 1)
            else:
                end_ln = self.last_line()

            add(who, start_ln, end_ln)

        for who, start_ln, end_ln in reversed(ranges):
            self.format_section(who, start_ln, end_ln)

        self.indent_lines()

    def enabled(self, who: str, what: str) -> bool:
        if who == "nobody":
            return True

        arg = getattr(args, f"markdown_{what}")

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
        if self.enabled(who, "snippets"):
            if self.format_snippets(start_ln, end_ln):
                end_ln = self.next_marker(start_ln)

        if self.enabled(who, "ordered"):
            if self.format_lists(start_ln, end_ln, who, "ordered"):
                end_ln = self.next_marker(start_ln)

        if self.enabled(who, "unordered"):
            if self.format_lists(start_ln, end_ln, who, "unordered"):
                end_ln = self.next_marker(start_ln)

        if self.enabled(who, "bold"):
            self.do_format(start_ln, end_ln, who, self.pattern_bold_1, "bold")

        if self.enabled(who, "italic"):
            self.do_format(start_ln, end_ln, who, self.pattern_italic_1, "italic")
            self.do_format(start_ln, end_ln, who, self.pattern_italic_2, "italic")

        if self.enabled(who, "highlights"):
            self.do_format(start_ln, end_ln, who, self.pattern_highlight_1, "highlight")
            self.do_format(start_ln, end_ln, who, self.pattern_highlight_2, "highlight")
            self.do_format(start_ln, end_ln, who, self.pattern_highlight_3, "highlight")

        if self.enabled(who, "quotes"):
            self.do_format(start_ln, end_ln, who, self.pattern_quote, "quote", True)

        if self.enabled(who, "urls"):
            self.do_format(start_ln, end_ln, who, self.pattern_url, "url")

        if self.enabled(who, "paths"):
            self.do_format(start_ln, end_ln, who, self.pattern_path, "path")

        if self.enabled(who, "headers"):
            self.do_format(start_ln, end_ln, who, self.pattern_header_1, "header_1")
            self.do_format(start_ln, end_ln, who, self.pattern_header_2, "header_2")
            self.do_format(start_ln, end_ln, who, self.pattern_header_3, "header_3")

        if self.enabled(who, "separators"):
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

            for item in reversed(items):
                all = item.group("all")

                if no_replace:
                    content = all
                else:
                    content = item.group("content")

                search_col = 0

                if tag == "header_3":
                    pass

                for _ in range(999):
                    start = self.widget.search(
                        all,
                        f"{mtch.line}.{search_col}",
                        stopindex=f"{mtch.line}.end",
                    )

                    if not start:
                        break

                    repeated = False

                    for index in indices:
                        if (index.start == start) and (index.content == content):
                            search_col = int(start.split(".")[1]) + len(all)
                            repeated = True

                    if repeated:
                        continue

                    end = self.widget.index(f"{start} + {len(all)}c")

                    if not end:
                        break

                    indices.append(IndexItem(start, end, content))

            sorted_indices = sorted(
                indices, key=lambda x: int(x.start.split(".")[1]), reverse=True
            )

            for index_item in sorted_indices:
                self.widget.delete(index_item.start, index_item.end)
                self.widget.insert(index_item.start, index_item.content)

                self.widget.tag_add(
                    tag,
                    index_item.start,
                    f"{index_item.start} + {len(index_item.content)}c",
                )

    def format_snippets(self, start_ln: int, end_ln: int) -> bool:
        from .snippet import Snippet

        text = self.widget.get(f"{start_ln}.0", f"{end_ln}.end")
        matches = []

        for match_ in re.finditer(
            self.pattern_snippets, text, flags=re.MULTILINE | re.DOTALL
        ):
            language = match_.group(1)

            content_start = match_.start(2)
            line_1 = self.get_line_number(text, content_start)
            start_line = f"{start_ln + line_1}.0"

            content_end = match_.end(2)
            line_2 = self.get_line_number(text, content_end)
            end_line = f"{start_ln + line_2}.0"

            matches.append((start_line, end_line, language))

        for start_line, end_line, language in reversed(matches):
            snippet_text = self.widget.get(
                f"{start_line} linestart", f"{end_line} lineend"
            )

            content_above = self.widget.get(
                f"{start_line} -1 lines linestart", f"{start_line} -1 lines lineend"
            ).strip()

            content_below = self.widget.get(
                f"{end_line} +2 lines linestart", f"{end_line} +2 lines lineend"
            ).strip()

            if content_below:
                self.widget.insert(f"{end_line} +1 lines lineend", "\n")

            snippet = Snippet(self.widget, snippet_text, language)
            numchars = 3

            if language:
                numchars += len(language)

            if len(content_above) > numchars:
                end_of_line_above = f"{start_line} -1 lines lineend"
                right_bit = f"{end_of_line_above} -{numchars} chars"
                self.widget.delete(right_bit, end_of_line_above)
                self.widget.insert(end_of_line_above, "\n")

                self.widget.delete(
                    f"{start_line} +1 lines", f"{end_line} +2 lines lineend"
                )

                self.widget.window_create(f"{start_line} +1 lines", window=snippet)
            else:
                start_of_line_above = f"{start_line} -2 lines linestart"
                end_of_line_above = f"{start_line} -2 lines lineend"

                line_above = self.widget.get(
                    start_of_line_above, end_of_line_above
                ).strip()

                if line_above:
                    self.widget.insert(end_of_line_above, "\n")

                    self.widget.delete(
                        f"{start_line} linestart", f"{end_line} +2 lines lineend"
                    )

                    self.widget.window_create(start_line, window=snippet)
                else:
                    self.widget.delete(
                        f"{start_line} -1 lines linestart",
                        f"{end_line} +1 lines lineend",
                    )

                    self.widget.window_create(f"{start_line} -1 lines", window=snippet)

            self.widget.snippets.append(snippet)

        return len(matches) > 0

    def format_lists(self, start_ln: int, end_ln: int, who: str, mode: str) -> bool:
        lines = self.get_lines(start_ln, end_ln, who)
        text = "\n".join(lines)
        matches = []

        if mode == "ordered":
            pattern = self.pattern_list_ordered
        else:
            pattern = self.pattern_list_unordered

        for match_ in re.finditer(pattern, text, flags=re.MULTILINE | re.DOTALL):
            content_start = match_.start(0)
            line_1 = self.get_line_number(text, content_start)
            start_line = f"{start_ln + line_1}.0"

            content_end = match_.end(0)
            line_2 = self.get_line_number(text, content_end)
            end_line = f"{start_ln + line_2}.0"

            matches.append((start_line, end_line, content_start, match_.group(0)))

        for start_line, end_line, content_start, mtch in reversed(matches):
            line_1 = text[:content_start].count("\n")
            line_2 = len(mtch.split("\n"))
            line_end = line_1 + line_2
            sliced = lines[line_1:line_end]
            spacing_mode = getattr(args, f"{mode}_spacing")
            marker = getattr(self, f"marker_indent_{mode}")

            if spacing_mode == "never":
                spaced = False
            elif spacing_mode == "always":
                spaced = True
            else:
                spaced = not all(line.strip() for line in sliced)

            space_1 = ""
            space_2 = "  "

            if mode == "ordered":
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
                self.widget.delete(right_bit, end_of_line_above)
                self.widget.insert(end_of_line_above, "\n\n\n")

                self.widget.delete(
                    f"{start_line} +1 lines", f"{end_line} +3 lines lineend"
                )

                txt = f"\n{txt}"

                if content_below:
                    txt += "\n"

                self.widget.insert(f"{start_line} +1 lines", txt)
            else:
                content_above = self.widget.get(
                    f"{start_line} -1 lines linestart", f"{start_line} -1 lines lineend"
                ).strip()

                if content_above:
                    txt = f"\n{txt}"

                if content_below:
                    txt += "\n"

                self.widget.delete(f"{start_line} linestart", f"{end_line} lineend")
                self.widget.insert(start_line, txt)

        return len(matches) > 0

    def format_separators(self, start_ln: int, end_ln: int, who: str) -> None:
        matches = []
        lines = self.get_lines(start_ln, end_ln, who)

        for i, line in enumerate(lines):
            if re.match(self.pattern_separator, line):
                matches.append(i)

        for i in reversed(matches):
            self.widget.delete(f"{start_ln + i}.0", f"{start_ln + i}.end")
            self.widget.insert(f"{start_ln + i}.0", self.separator)

            self.widget.tag_add(
                "separator",
                f"{start_ln + i}.0",
                f"{start_ln + i}.0 + {len(self.separator)}c",
            )

    def get_lines(self, start_ln: int, end_ln: int, who: str) -> list[str]:
        text = self.widget.get(f"{start_ln}.0", f"{end_ln}.end")
        lines = text.split("\n")

        if who in ("user", "ai"):
            index = lines[0].index(f":{Output.marker_space}") + 2
            lines[0] = lines[0][index:]

        return lines

    def get_line_number(self, text: str, index: int) -> int:
        return text.count("\n", 0, index)

    def escape_chars(self, chars: list[str], separator: str = "") -> str:
        clean = [utils.escape_regex(c) for c in chars]
        return separator.join(clean)

    def next_marker(self, start_ln: int) -> int:
        markers = self.widget.get_markers(True)

        for i, marker in enumerate(markers):
            if marker["line"] == start_ln:
                if i < len(markers) - 1:
                    return int(markers[i + 1]["line"] - 1)

        return self.last_line()

    def last_line(self) -> int:
        return int(self.widget.index("end").split(".")[0])

    def indent_lines(self) -> None:
        lines = self.widget.get("1.0", "end").split("\n")

        def get_lns(marker: str) -> list[int]:
            return [i + 1 for i, line in enumerate(lines) if line.startswith(marker)]

        def add_tags(lns: list[int], name: str) -> None:
            for line in lns:
                ln = f"{line}.0"
                self.widget.tag_add(name, ln, f"{ln} lineend")

        or_lines = get_lns(self.marker_indent_ordered)
        add_tags(or_lines, "indent_ordered")

        un_lines = get_lns(self.marker_indent_unordered)
        add_tags(un_lines, "indent_unordered")
