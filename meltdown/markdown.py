# Standard
import re
from typing import List, Any, Tuple

# Modules
from .app import app
from .args import args
from .output import Output
from .utils import utils
from .separatorbox import SeparatorBox


class MatchItem:
    def __init__(self, line: int, items: List[re.Match[Any]]) -> None:
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

        chars_right = [".", ",", ";", "!", "?", ":", "/"]
        right_string = self.escape_chars(chars_right, "|")
        right = rf"(?=\s|$|{right_string})"

        protocols_list = ["http://", "https://", "ftp://", "www."]
        protocols_string = self.escape_chars(protocols_list, "|")
        protocols = rf"({protocols_string})"

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
        self.pattern_header_1 = rf"^(?P<all>{hash_}{{3}}\s*(?P<content>.*))$"

        # Header with two hashes
        self.pattern_header_2 = rf"^(?P<all>{hash_}{{2}}\s*(?P<content>.*))$"

        # Header with one hash
        self.pattern_header_3 = rf"^(?P<all>{hash_}{{1}}\s*(?P<content>.*))$"

        # Separator line
        self.pattern_separator = r"^---$"

    def format_all(self) -> None:
        start_ln = 1
        end_ln = int(self.widget.index("end").split(".")[0])
        self.format_section("nobody", start_ln, end_ln)

    def format(self) -> None:
        if args.markdown == "none":
            return

        markers, num_lines = self.widget.get_markers()
        ranges: List[Tuple[str, int, int]] = []

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
                end_ln = markers[i + 1]["line"] - 1
            else:
                end_ln = num_lines

            add(who, start_ln, end_ln)

        for who, start_ln, end_ln in reversed(ranges):
            self.format_section(who, start_ln, end_ln)

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
            self.format_snippets(start_ln, end_ln)

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
            self.do_format(start_ln, end_ln, who, self.pattern_header_1, "header_3")
            self.do_format(start_ln, end_ln, who, self.pattern_header_2, "header_2")
            self.do_format(start_ln, end_ln, who, self.pattern_header_3, "header_1")

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
        matches: List[MatchItem] = []
        lines = self.get_lines(start_ln, end_ln, who)

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            match = MatchItem(start_ln + i, list(re.finditer(pattern, line)))

            if match.items:
                matches.append(match)

        for match_ in reversed(matches):
            items = match_.items
            indices: List[IndexItem] = []

            for item in reversed(items):
                all = item.group("all")

                if no_replace:
                    content = all
                else:
                    content = item.group("content")

                search_col = 0

                if tag == "header_3":
                    pass

                for _ in range(0, 999):
                    start = self.widget.search(
                        all,
                        f"{match_.line}.{search_col}",
                        stopindex=f"{match_.line}.end",
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

            sorted_indices = reversed(
                sorted(indices, key=lambda x: int(x.start.split(".")[1]))
            )

            for index_item in sorted_indices:
                self.widget.delete(index_item.start, index_item.end)
                self.widget.insert(index_item.start, index_item.content)

                self.widget.tag_add(
                    tag,
                    index_item.start,
                    f"{index_item.start} + {len(index_item.content)}c",
                )

    def format_snippets(self, start_ln: int, end_ln: int) -> None:
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

    def format_separators(self, start_ln: int, end_ln: int, who: str) -> None:
        matches = []
        lines = self.get_lines(start_ln, end_ln, who)

        for i, line in enumerate(lines):
            if re.match(self.pattern_separator, line):
                matches.append(i)

        for i in reversed(matches):
            separator = SeparatorBox(
                self.widget, app.theme.menu_background, padx=100, pady=1
            )

            self.widget.delete(f"{start_ln + i}.0", f"{start_ln + i}.end")
            self.widget.window_create(f"{start_ln + i}.0", window=separator)

    def get_lines(self, start_ln: int, end_ln: int, who: str) -> List[str]:
        text = self.widget.get(f"{start_ln}.0", f"{end_ln}.end")
        lines = text.split("\n")

        if (who == "user") or (who == "ai"):
            index = lines[0].index(f":{Output.marker_space}") + 2
            lines[0] = lines[0][index:]

        return lines

    def get_line_number(self, text: str, index: int) -> int:
        return text.count("\n", 0, index)

    def escape_chars(self, chars: List[str], separator: str = "") -> str:
        clean = [utils.escape_regex(c) for c in chars]
        return separator.join(clean)
