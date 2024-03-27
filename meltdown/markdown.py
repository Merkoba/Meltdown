# Modules
from .output import Output

# Standard
import re
from typing import List, Any


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

        chars_left = self.escape_regex("([")
        left_side = fr"[{chars_left}]?"

        chars_right = self.escape_regex(".,;!?:)")
        right_side = fr"[{chars_right}]?"

        # Bold with two *
        self.pattern_bold = fr"(?:(?<=\s)|^){left_side}(?P<all>\*{{2}}(?P<content>.*?)\*{{2}}){right_side}(?=\s|$)"

        # Italic with one *
        self.pattern_italic_1 = fr"(?:(?<=\s)|^){left_side}(?P<all>\*(?P<content>.*?)\*){right_side}(?=\s|$)"

        # Italic with one _
        self.pattern_italic_2 = fr"(?:(?<=\s)|^){left_side}(?P<all>\_(?P<content>.*?)\_){right_side}(?=\s|$)"

        # Highlight with one `
        self.pattern_highlight = fr"(?:(?<=\s)|^){left_side}(?P<all>\`(?P<content>.*?)\`){right_side}(?=\s|$)"

        # URLs with http:// | https:// | ftp:// | www.
        self.pattern_url = r"(?:(?<=\s)|^)(?P<all>(?P<content>(http:\/\/|https:\/\/|ftp:\/\/|www\.)([^\s]+?)))(?=\s|$)"

    def escape_regex(self, chars: str) -> str:
        escaped_chars = [re.escape(char) for char in chars]
        return "".join(escaped_chars)

    def format(self) -> None:
        self.format_snippets()
        lines = self.widget.get("1.0", "end-1c").split("\n")
        self.do_format(lines, self.pattern_bold, "bold")
        self.do_format(lines, self.pattern_italic_1, "italic")
        self.do_format(lines, self.pattern_italic_2, "italic")
        self.do_format(lines, self.pattern_highlight, "highlight")
        self.do_format(lines, self.pattern_url, "url")

    def do_format(self, lines: List[str], pattern: str, tag: str) -> None:
        matches: List[MatchItem] = []

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            match = MatchItem(i + 1, list(re.finditer(pattern, line)))
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

    def format_snippets(self) -> None:
        from .snippet import Snippet
        text = self.widget.get("1.0", "end-1c")
        pattern = r"```([-\w.#]*)\n(.*?)\n```$"
        matches = []

        for match in re.finditer(pattern, text, flags=re.MULTILINE | re.DOTALL):
            language = match.group(1)
            content_start = match.start(2)
            content_end = match.end(2)
            matches.append((content_start, content_end, language))

        for content_start, content_end, language in reversed(matches):
            start_index = self.index_of_relative(content_start, "1.0")
            end_index = self.index_of_relative(content_end, "1.0")
            start_line = self.get_line(start_index)
            end_line = self.get_line(end_index)
            snippet_text = self.widget.get(f"{start_line} linestart", f"{end_line} lineend")
            self.widget.delete(f"{start_line} - 1 lines linestart", f"{end_line} + 1 lines lineend")
            snippet = Snippet(self.widget, snippet_text, language)
            self.widget.window_create(f"{start_line} - 1 lines", window=snippet)
            self.widget.snippets.append(snippet)

    def index_of_relative(self, index: int, position: str) -> str:
        line, col = map(int, position.split("."))
        text = self.widget.get(position, "end-1c")

        for i in range(index):
            if i >= len(text):
                break
            elif (text[i] == "\n"):
                line += 1
                col = 0
            else:
                col += 1

        return f"{line}.{col}"

    def get_line(self, index: str) -> str:
        return str(index.split(".")[0]) + ".0"
