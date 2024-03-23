# Modules
from .output import Output

# Standard
import re
from typing import Optional


class Markdown():
    protocols = ("http://", "https://", "ftp://", "www.")

    def __init__(self, widget: Output) -> None:
        self.widget = widget

    def format(self, position: str) -> None:
        self.format_snippets(position)
        self.format_highlights(position)
        self.format_bold(position)
        self.format_italic(position)
        self.format_urls(position)

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

    def format_snippets(self, position: str) -> None:
        from .snippet import Snippet
        text = self.widget.get(position, "end-1c")
        pattern = r"^```([-\w.#]*)\n(.*?)\n```$"
        matches = []

        for match in re.finditer(pattern, text, flags=re.MULTILINE | re.DOTALL):
            language = match.group(1)
            content_start = match.start(2)
            content_end = match.end(2)
            matches.append((content_start, content_end, language))

        for content_start, content_end, language in reversed(matches):
            start_index = self.index_of_relative(content_start, position)
            end_index = self.index_of_relative(content_end, position)
            start_line = self.get_line(start_index)
            end_line = self.get_line(end_index)
            snippet_text = self.widget.get(f"{start_line} linestart", f"{end_line} lineend")
            self.widget.delete(f"{start_line} - 1 lines linestart", f"{end_line} + 1 lines lineend")

            snippet = Snippet(self.widget, snippet_text, language)
            self.widget.window_create(f"{start_line} - 1 lines", window=snippet)
            self.widget.snippets.append(snippet)

    def format_highlights(self, position: str) -> None:
        token = "`"
        code_string = ""
        in_code = False
        index_start = ""

        def reset_code() -> None:
            nonlocal in_code
            nonlocal code_string
            nonlocal index_start
            in_code = False
            code_string = ""
            index_start = ""

        def on_match(start: str, end: str) -> None:
            original_text = self.widget.get(f"{start}", f"{end}")
            clean_text = self.untoken(original_text, token)
            self.widget.delete(f"{start}", f"{end}")
            self.widget.insert(f"{start}", f"{clean_text}")
            end_index = self.get_end_index(start, clean_text)
            self.widget.tag_add("highlight", f"{start}", end_index)
            self.format_highlights(self.solve_index(end_index))

        current_line, col_ = map(int, position.split("."))
        lines = self.widget.get(position, "end-1c").split("\n")

        for line_ in lines:
            in_code = False

            if col_ > 0:
                col = col_
                col_ = 0
            else:
                col = 0

            chars = self.widget.get(f"{current_line}.0", f"{current_line}.end")

            for i, char_ in enumerate(chars):
                index = f"{current_line}.{col}"
                char = self.widget.get(index)

                if char == token:
                    prev_char = self.widget.get(f"{index} - 1c") if i > 0 else ""
                    next_char = self.widget.get(f"{index} + 1c") if i < len(chars) else ""

                    if in_code:
                        if (prev_char != token) and (next_char != token):
                            on_match(index_start, f"{index} + 1c")
                            return
                    elif (prev_char != token) and (next_char not in (token, " ")):
                        reset_code()
                        in_code = True
                        index_start = index

                col += 1

            current_line += 1

    def format_bold(self, position: str) -> None:
        token = "*"
        code_string = ""
        in_code = False
        index_start = ""

        def reset_code() -> None:
            nonlocal in_code
            nonlocal code_string
            in_code = False
            code_string = ""

        def on_match(start: str, end: str) -> None:
            original_text = self.widget.get(f"{start}", f"{end}")
            clean_text = self.untoken(original_text, token * 2)
            self.widget.delete(f"{start}", f"{end}")
            self.widget.insert(f"{start}", f"{clean_text}")
            end_index = self.get_end_index(start, clean_text)
            self.widget.tag_add("bold", f"{start}", end_index)
            self.format_bold(self.solve_index(end_index))

        current_line, col_ = map(int, position.split("."))
        lines = self.widget.get(position, "end-1c").split("\n")

        for line_ in lines:
            in_code = False

            if col_ > 0:
                col = col_
                col_ = 0
            else:
                col = 0

            chars = self.widget.get(f"{current_line}.0", f"{current_line}.end")

            for i, char_ in enumerate(chars):
                index = f"{current_line}.{col}"
                char = self.widget.get(index)

                if char == token:
                    prev_char = self.widget.get(f"{index} - 1c") if i > 0 else ""
                    next_char = self.widget.get(f"{index} + 1c") if i < len(chars) else ""
                    next_char_2 = self.widget.get(f"{index} + 2c") if i < len(chars) - 1 else ""

                    if in_code:
                        if (prev_char != token) and (next_char == token) and (next_char_2 != token):
                            on_match(f"{index_start}", f"{index} + 2c")
                            return
                    elif (prev_char != token) and (next_char == token) and (next_char_2 not in (token, " ")):
                        reset_code()
                        in_code = True
                        index_start = index

                col += 1

            current_line += 1

    def format_italic(self, position: str) -> None:
        token = ""
        tokens = ("*", "_")
        code_string = ""
        in_code = False
        index_start = ""

        def reset_code() -> None:
            nonlocal in_code
            nonlocal code_string
            in_code = False
            code_string = ""

        def on_match(start: str, end: str) -> None:
            original_text = self.widget.get(f"{start}", f"{end}")
            print(original_text)
            clean_text = self.untoken(original_text, token)
            self.widget.delete(f"{start}", f"{end}")
            self.widget.insert(f"{start}", f"{clean_text}")
            end_index = self.get_end_index(start, clean_text)
            self.widget.tag_add("italic", f"{start}", end_index)
            self.format_italic(self.solve_index(end_index))

        current_line, col_ = map(int, position.split("."))
        lines = self.widget.get(position, "end-1c").split("\n")

        for line_ in lines:
            in_code = False

            if col_ > 0:
                col = col_
                col_ = 0
            else:
                col = 0

            chars = self.widget.get(f"{current_line}.0", f"{current_line}.end")

            for i, char_ in enumerate(chars):
                index = f"{current_line}.{col}"
                char = self.widget.get(index)

                if char in tokens:
                    prev_char = self.widget.get(f"{index} - 1c") if i > 0 else ""
                    next_char = self.widget.get(f"{index} + 1c") if i < len(chars) else ""

                    if in_code:
                        print(prev_char, char, next_char)
                        print(prev_char not in tokens, next_char not in tokens)
                        if (prev_char not in tokens) and (next_char not in tokens):
                            on_match(index_start, f"{index} + 1c")
                            return
                    elif (prev_char not in tokens) and (next_char not in tokens):
                        reset_code()
                        in_code = True
                        index_start = index
                        token = char

                col += 1

            current_line += 1

    def format_urls(self, position: str) -> None:
        index_start = ""

        def on_match(start: str, end: str) -> None:
            end = self.solve_index(end)
            self.widget.tag_add("url", start, end)
            self.format_urls(self.solve_index(end))

        current_line, col_ = map(int, position.split("."))
        lines = self.widget.get(position, "end-1c").split("\n")

        for line_ in lines:
            index_start = ""

            if col_ > 0:
                col = col_
                col_ = 0
            else:
                col = 0

            chars = self.widget.get(f"{current_line}.0", f"{current_line}.end")

            for i, char_ in enumerate(chars):
                index = f"{current_line}.{col}"
                char = self.widget.get(index)
                next_char = self.widget.get(f"{index} + 1c") if i < len(chars) else ""
                stopper = False

                if index_start:
                    if (next_char == " ") or (i == len(chars) - 1):
                        stopper = True

                if stopper:
                    word = self.widget.get(index_start, f"{index} + 1c")

                    if word and any([word.startswith(protocol) for protocol in Markdown.protocols]):
                        on_match(index_start, f"{index} + 1c")
                        return

                    index_start = ""
                else:
                    if char != " ":
                        if not index_start:
                            index_start = index
                    else:
                        index_start = ""

                col += 1

            current_line += 1

    def untoken(self, string: str, token: str) -> str:
        length = len(token)
        string = string[length:]
        string = string[:-length]
        return string

    def solve_index(self, index: str) -> str:
        return self.widget.index(index)

    def get_end_index(self, start: str, text: str) -> str:
        start_index = self.solve_index(start)
        start_line, start_col = map(int, start_index.split("."))
        return f"{start_line}.{start_col + len(text)}"
