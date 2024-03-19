# Standard
import re
import tkinter as tk
from typing import Optional


class Markdown():
    def __init__(self, widget: tk.Text) -> None:
        self.widget = widget

    def format(self, complete: bool, position: str) -> None:
        # self.format_snippets(complete, position)
        self.format_highlights(complete, position)
        # self.format_bold(complete, position)
        # self.format_italic(complete, position)
        # self.format_urls(complete, position)

    def is_space(self, char: Optional[str]) -> bool:
        if char is None:
            return True

        return char == " "

    def index_of_relative(self, index: int, position: str) -> str:
        line, col = map(int, position.split("."))
        text = self.widget.get(position, "end")

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

    def format_snippets(self, complete: bool, position: str) -> None:
        from .snippet import Snippet
        text = self.widget.get(position, "end")
        pattern = r"^```([\w#]*)\n(.*?)\n```$"
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

    def format_highlights(self, complete: bool, position: str) -> None:
        token = "`"
        result = ""
        code_string = ""
        in_code = False
        index_start = ""
        last = self.widget.index("end-1c")

        def ended(i: int) -> bool:
            if complete:
                return index == last
            else:
                return False

        def reset_code() -> None:
            nonlocal in_code
            nonlocal code_string
            global index_start
            in_code = False
            code_string = ""
            index_start = 0

        def rollback() -> None:
            nonlocal result
            result += token + code_string

        def on_match(start: int, end: int) -> None:
            # print(end - start)
            # print(len("highlight"))
            # print(end - start)
            # print(len("highlight"))
            start_index = self.index_of_relative(start, position)
            # print(start_index)
            end_index = self.index_of_relative(end, position)
            end_space = f"{end_index}"
            # print(start_index, end_index)
            # print(self.widget.get(f"{start_index}"))
            original_text = self.widget.get(f"{start_index}", end_space)
            print("1" + original_text + "2")
            clean_text = self.untoken(original_text, token)
            # print(clean_text)
            self.widget.delete(f"{start_index}", end_space)
            self.widget.insert(f"{start_index}", f"{clean_text}")
            self.widget.tag_add("highlight", f"{start_index}", f"{end_index}")
            next_position = self.index_of_relative(end + 2, position)
            self.format_highlights(complete, next_position)

        current_line, original_col = map(int, position.split("."))
        lines = self.widget.get(position, "end-1c").split("\n")

        for line in lines:
            col = 0

            for char in self.widget.get(position, "end"):
                index = f"{current_line}.{col}"

                if char == token:
                    prev_char = self.widget.get(f"{index} - 1c")
                    next_char = self.widget.get(f"{index} + 1c")

                    if in_code:
                        if (prev_char != token) and (next_char != token):
                            on_match(index_start, index)
                            return
                    elif self.is_space(prev_char) and (next_char != token):
                        reset_code()
                        in_code = True
                        index_start = index
                else:
                    if char == "\n" or ended(index):
                        if in_code:
                            rollback()
                            reset_code()

                        result += char
                    else:
                        if in_code:
                            code_string += char
                        else:
                            result += char

                col += 1

            current_line += 1

    def format_bold(self, complete: bool, position: str) -> None:
        text = self.widget.get(position, "end")
        token = "*"
        result = ""
        code_string = ""
        in_code = False
        index_start = 0
        last = len(text) - 1

        def ended(i: int) -> bool:
            if complete:
                return i == last
            else:
                return False

        def reset_code() -> None:
            nonlocal in_code
            nonlocal code_string
            in_code = False
            code_string = ""

        def rollback() -> None:
            nonlocal result
            result += token + code_string

        def on_match(start: int, end: int) -> None:
            start_index = self.index_of_relative(start, position)
            end_index = self.index_of_relative(end, position)
            end_space = f"{end_index} + 1c"
            original_text = self.widget.get(f"{start_index}", end_space)
            clean_text = self.untoken(original_text, token)
            self.widget.delete(f"{start_index}", end_space)
            self.widget.insert(f"{start_index}", f"{clean_text}")
            self.widget.tag_add("bold", f"{start_index} + 1c", f"{end_index} - 1c")
            next_position = self.index_of_relative(end + 2, position)
            self.format_bold(complete, next_position)

        for i, char in enumerate(text):
            if char == token:
                prev_char = text[i - 1] if (i - 1) >= 0 else None
                next_char = text[i + 1] if (i + 1) < len(text) else None
                next_char_2 = text[i + 2] if (i + 2) < len(text) else None

                if in_code:
                    if (prev_char != token) and (next_char == token) and (next_char_2 != token):
                        on_match(index_start, i)
                        return
                elif self.is_space(prev_char) and (next_char == token) and (next_char_2 != token):
                    reset_code()
                    in_code = True
                    index_start = i
            else:
                if char == "\n" or ended(i):
                    if in_code:
                        rollback()
                        reset_code()

                    result += char
                else:
                    if in_code:
                        code_string += char
                    else:
                        result += char

    def format_italic(self, complete: bool, position: str) -> None:
        text = self.widget.get(position, "end")
        token = ""
        result = ""
        code_string = ""
        in_code = False
        matches = []
        index_start = 0
        last = len(text) - 1

        def is_token(char: str) -> bool:
            return char in ("*", "_")

        def ended(i: int) -> bool:
            if complete:
                return i == last
            else:
                return False

        def reset_code() -> None:
            nonlocal in_code
            nonlocal code_string
            in_code = False
            code_string = ""

        def rollback() -> None:
            nonlocal result
            result += token + code_string

        for i, char in enumerate(text):
            if is_token(char):
                prev_char = text[i - 1] if (i - 1) >= 0 else None
                next_char = text[i + 1] if (i + 1) < len(text) else None

                if in_code:
                    if (prev_char != token) and (next_char != token):
                        matches.append((index_start, i))
                        reset_code()
                elif self.is_space(prev_char) and (next_char != token):
                    reset_code()
                    in_code = True
                    index_start = i
                    token = char
            else:
                if char == "\n" or ended(i):
                    if in_code:
                        rollback()
                        reset_code()

                    result += char
                else:
                    if in_code:
                        code_string += char
                    else:
                        result += char

        if matches:
            for start, end in reversed(matches):
                start_index = self.index_of_relative(start, position)
                end_index = self.index_of_relative(end, position)
                clean_text = self.widget.get(f"{start_index} + 2c", f"{end_index}")
                self.widget.delete(start_index, f"{end_index} + 2c")
                self.widget.insert(start_index, clean_text)
                self.widget.tag_add("bold", start_index, end_index)

    def format_urls(self, complete: bool, position: str) -> None:
        text = self.widget.get(position, "end")
        protocols = ("http://", "https://", "ftp://", "www.")
        stoppers = (" ", "\n")
        matches = []
        last = len(text) - 1
        word = ""

        def ended(i: int) -> bool:
            if complete:
                return i == last
            else:
                return False

        for i, char in enumerate(text):
            if char in stoppers or ended(i):
                end_index = i

                if ended(i):
                    word += char
                    end_index += 1

                if any([word.startswith(protocol) for protocol in protocols]):
                    matches.append((i - len(word), end_index))

                word = ""
            else:
                word += char

        if matches:
            for start, end in reversed(matches):
                start_index = self.index_of_relative(start, position)
                end_index = self.index_of_relative(end, position)
                self.widget.tag_add("url", start_index, end_index)

    def untoken(self, string: str, token: str) -> str:
        if string.startswith(token):
            string = string[1:]

        if string.endswith(token):
            string = string[:-1]

        return string
