# Standard
import re
from typing import List, Any, Tuple

# Modules
from .args import args
from .output import Output
from . import utils


class MatchItem:
    def __init__(self, line: int, items: List[re.Match[Any]]) -> None:
        self.line = line
        self.items = items


class IndexItem:
    def __init__(self, start: str, end: str, content: str) -> None:
        self.start = start
        self.end = end
        self.content = content


class Markdown():
    def __init__(self, widget: Output) -> None:
        self.widget = widget
        self.start_stopppers = ["", " "]
        self.end_stoppers = ["", " ", "!", ".", "?", "\n", ",", ";"]
        self.protocols = ("http://", "https://", "ftp://", "www.")

        chars_left = utils.escape_regex("([")
        left_side = fr"[{chars_left}]?"

        chars_right = utils.escape_regex(".,;!?:)")
        right_side = fr"[{chars_right}]?"

        # Bold with two *
        self.pattern_bold_1 = fr"(?:(?<=\s)|^){left_side}(?P<all>\*{{2}}(?P<content>.*?)\*{{2}}){right_side}(?=\s|$)"

        # Italic with one *
        self.pattern_italic_1 = fr"(?:(?<=\s)|^){left_side}(?P<all>\*{{1}}(?P<content>.*?)\*{{1}}){right_side}(?=\s|$)"

        # Italic with one _
        self.pattern_italic_2 = fr"(?:(?<=\s)|^){left_side}(?P<all>\_{{1}}(?P<content>.*?)\_{{1}}){right_side}(?=\s|$)"

        # Highlight with three `
        self.pattern_highlight_1 = fr"(?:(?<=\s)|^){left_side}(?P<all>\`{{3}}(?P<content>.*?)\`{{3}}){right_side}(?=\s|$)"

        # Highlight with two `
        self.pattern_highlight_2 = fr"(?:(?<=\s)|^){left_side}(?P<all>\`{{2}}(?P<content>.*?)\`{{2}}){right_side}(?=\s|$)"

        # Highlight with one `
        self.pattern_highlight_3 = fr"(?:(?<=\s)|^){left_side}(?P<all>\`{{1}}(?P<content>.*?)\`{{1}}){right_side}(?=\s|$)"

        # URLs with http:// | https:// | ftp:// | www.
        self.pattern_url = r"(?:(?<=\s)|^)(?P<all>(?P<content>(http:\/\/|https:\/\/|ftp:\/\/|www\.)([^\s]+?)))(?=\s|$)"

    def format(self) -> None:
        markers, num_lines = self.widget.get_markers()
        ranges: List[Tuple[int, int]] = []
        start_ln = 0
        end_ln = 0

        def add() -> None:
            ranges.append((start_ln, end_ln))

        if args.markdown == "none":
            return
        elif args.markdown == "all":
            start_ln = 1
            end_ln = num_lines + 1
            add()
        else:
            if args.markdown == "user":
                name_a = "ai"
                name_b = "user"
            elif args.markdown == "ai":
                name_a = "user"
                name_b = "ai"

            for i, item in enumerate(markers):
                if item["who"] == name_a:
                    if start_ln:
                        end_ln = item["line"] - 1
                        add()
                elif item["who"] == name_b:
                    start_ln = item["line"]

                    if i == len(markers) - 1:
                        end_ln = num_lines + 1
                        add()

        for start, end in reversed(ranges):
            self.format_all(start, end)

    def format_all(self, start_ln: int, end_ln: int) -> None:
        self.format_snippets(start_ln, end_ln)
        self.do_format(start_ln, end_ln, self.pattern_bold_1, "bold")
        self.do_format(start_ln, end_ln, self.pattern_italic_1, "italic")
        self.do_format(start_ln, end_ln, self.pattern_italic_2, "italic")
        self.do_format(start_ln, end_ln, self.pattern_highlight_1, "highlight")
        self.do_format(start_ln, end_ln, self.pattern_highlight_2, "highlight")
        self.do_format(start_ln, end_ln, self.pattern_highlight_3, "highlight")
        self.do_format(start_ln, end_ln, self.pattern_url, "url")

    def do_format(self, start_ln: int, end_ln: int, pattern: str, tag: str) -> None:
        matches: List[MatchItem] = []

        for ln in range(start_ln, end_ln + 1):
            line = self.widget.get(f"{ln}.0", f"{ln}.end")

            if not line.strip():
                continue

            match = MatchItem(ln, list(re.finditer(pattern, line)))
            matches.append(match)

        for match in reversed(matches):
            items = match.items
            indices: List[IndexItem] = []

            for item in reversed(items):
                all = item.group("all")
                content = item.group("content")
                search_col = 0

                for _ in range(0, 999):
                    start = self.widget.search(all, f"{match.line}.{search_col}", stopindex=f"{match.line}.end")

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

            sorted_indices = reversed(sorted(indices, key=lambda x: int(x.start.split(".")[1])))

            for index_item in sorted_indices:
                self.widget.delete(index_item.start, index_item.end)
                self.widget.insert(index_item.start, index_item.content)
                self.widget.tag_add(tag, index_item.start, f"{index_item.start} + {len(index_item.content)}c")

    def format_snippets(self, start_ln: int, end_ln: int) -> None:
        from .snippet import Snippet
        text = self.widget.get(f"{start_ln}.0", f"{end_ln}.end")
        pattern = r"```([-\w.#]*)\n(.*?)\n```$"
        matches = []

        for match in re.finditer(pattern, text, flags=re.MULTILINE | re.DOTALL):
            language = match.group(1)

            content_start = match.start(2)
            line_1 = self.get_line_number(text, content_start)
            start_line = f"{start_ln + line_1}.0"

            content_end = match.end(2)
            line_2 = self.get_line_number(text, content_end)
            end_line = f"{start_ln + line_2}.0"

            matches.append((start_line, end_line, language))

        for start_line, end_line, language in reversed(matches):
            snippet_text = self.widget.get(f"{start_line} linestart", f"{end_line} lineend")
            content_above = self.widget.get(f"{start_line} -1 line linestart", f"{start_line} -1 line lineend").strip()
            snippet = Snippet(self.widget, snippet_text, language)
            numchars = 3

            if language:
                numchars += len(language)

            if len(content_above) > numchars:
                end_of_line_above = f"{start_line} -1 line lineend"
                right_bit = f"{end_of_line_above} -{numchars} chars"
                self.widget.delete(right_bit, end_of_line_above)
                self.widget.delete(start_line, f"{end_line} +1 line lineend")
                self.widget.window_create(start_line, window=snippet)
            else:
                self.widget.delete(f"{start_line} -1 line linestart", f"{end_line} +1 line lineend")
                self.widget.window_create(f"{start_line} - 1 lines", window=snippet)

            self.widget.snippets.append(snippet)

    def get_line_number(self, text: str, index: int) -> int:
        return text.count("\n", 0, index)
