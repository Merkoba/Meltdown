# Modules
from .output import Output

# Standard
import re
from typing import List, Any


class MatchItem:
    def __init__(self, line: int, items: List[re.Match[Any]]) -> None:
        self.line = line
        self.items = items


class Markdown():
    def __init__(self, widget: Output) -> None:
        self.widget = widget
        self.start_stopppers = ["", " "]
        self.end_stoppers = ["", " ", "!", ".", "?", "\n", ",", ";"]
        self.protocols = ("http://", "https://", "ftp://", "www.")

    def format(self) -> None:
        # Code fences
        self.format_snippets()

        # All lines
        lines = self.widget.get("1.0", "end-1c").split("\n")

        # Bold with two *
        pattern = r"(?:(?<=\s)|^)(?P<all>\*{2}(?P<content>.*?)\*{2})[\.\,\;\!\?\:]?(?=\s|$)"
        self.do_format(lines, pattern, "bold")

        # Italic with one *
        pattern = r"(?:(?<=\s)|^)(?P<all>\*(?P<content>.*?)\*)[\.\,\;\!\?\:]?(?=\s|$)"
        self.do_format(lines, pattern, "italic")

        # Italic with one _
        pattern = r"(?:(?<=\s)|^)(?P<all>\_(?P<content>.*?)\_)[\.\,\;\!\?\:]?(?=\s|$)"
        self.do_format(lines, pattern, "italic")

        # Highlight with one `
        pattern = r"(?:(?<=\s)|^)(?P<all>\`(?P<content>.*?)\`)[\.\,\;\!\?\:]?(?=\s|$)"
        self.do_format(lines, pattern, "highlight")

        # URLs with http:// | https:// | ftp:// | www.
        pattern = r"(?:(?<=\s)|^)(?P<all>(?P<content>(http:\/\/|https:\/\/|ftp:\/\/|www\.)([^\s]+?)))(?=\s|$)"
        self.do_format(lines, pattern, "url")

    def do_format(self, lines: List[str], pattern: str, tag: str) -> None:
        matches: List[MatchItem] = []

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            match = MatchItem(i + 1, list(re.finditer(pattern, line)))
            matches.append(match)

        for match in reversed(matches):
            items = match.items
            indices = []

            for item in reversed(items):
                all = item.group("all")
                content = item.group("content")
                start = self.widget.search(all, f"{match.line}.0", stopindex="end")

                if not start:
                    continue

                end = self.widget.index(f"{start} + {len(all)}c")
                indices.append((start, end, content))

            for start, end, content in indices:
                self.widget.delete(start, end)
                self.widget.insert(start, content)
                self.widget.tag_add(tag, start, f"{start} + {len(content)}c")

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
