# Standard
from typing import Any


Test = dict[str, Any]


class Tests:
    def __init__(self) -> None:
        self.format_test: Test = {
            "items": [
                {
                    "user": "Highlight Test",
                    "ai": "Here is a `highlight` and `a longer highlight`.\nHere is a `highlight` and `a longer highlight`.",
                },
                {
                    "user": "Highlight Test 2",
                    "ai": "`another highlight 123`",
                },
                {
                    "user": "Bold Test",
                    "ai": "Here is a bold **word** and **a bold sentence**.\nHere is a bold **word** and **a bold sentence**.",
                },
                {
                    "user": "Bold Test 2",
                    "ai": "\n1) **Some Item:** Description\n2) **Another Item:** Description\n3) **Third Item:** Description",
                },
                {
                    "user": "Bold Test 3",
                    "ai": "**This is a bold sentence**\n**This is a bold sentence**",
                },
                {
                    "user": "Italic Test with Asterisk",
                    "ai": "Here is an italic *word* and *an italic sentence*.\nHere is an italic *word* and *an italic sentence*.",
                },
                {
                    "user": "Italic Test with Underscore",
                    "ai": "Here is a an italic _word_ and _an italic sentence_.\nHere is a an italic _word_ and _an italic sentence_.",
                },
                {
                    "user": "Italic Test 3",
                    "ai": "*This is an italic sentence*\n*This is an italic sentence*",
                },
                {
                    "user": "Italic Test 4",
                    "ai": "_This is an italic sentence_ 2\n_This is an italic sentence_ 2",
                },
                {
                    "user": "Snippet Test",
                    "ai": "```python\na = 123\nprint('Hello, World!')\n```\n\n"
                    + "Here is more code:\n\n```js\nlet a = 123\nconsole.log('Hello, World!')\n```",
                },
                {
                    "user": "Snippet Test 2",
                    "ai": "Here is some code:\n\n```\na = 123\nprint('Hello, World!')\n```\n\n"
                    + "Here is more code:\n\n```js\nlet a = 123\nconsole.log('Hello, World!')\n```",
                },
                {
                    "user": "Snippet Test 3",
                    "ai": "```python\na = 123\nprint('Hello, World!')\n```",
                },
                {
                    "user": "Snippet Test 4",
                    "ai": "Last snippet 1:\n```python\na = 123\nprint('Hello, World!')\nx = 6\n```\n"
                    + "```python\na = 123\nprint('Hello, World!')\nx = 6\n```",
                },
                {
                    "user": "URL Test",
                    "ai": "Here are some urls https://aa.com and http://cc.com and ftp://44.com\n"
                    + "Here are some urls https://aa.com and http://cc.com\nftp://44.com",
                },
                {
                    "user": "Normal Sentence",
                    "ai": "Here is a normal sentence",
                },
                {
                    "user": "Loading dolphin-2_6-phi-2.Q5_K_M.gguf",
                    "ai": "Ok",
                },
                {
                    "user": "Here is a path /home/yo",
                    "ai": "That is indeed /home/yo/file.txt",
                },
                {
                    "user": 'This is "a quoted text"',
                    "ai": 'That is a "quoted text".',
                },
                {
                    "user": "Some backtick test",
                    "ai": "Rendering LaTeX code as an image within a Tkinter Text widget can be achieved by using a combination of packages such as `mathjax` (to convert LaTeX to MathML) and `svglib`/`reportlab` (to convert MathML to SVG)",
                },
                {
                    "user": "Show me 3 hashes",
                    "ai": "### The Title",
                },
                {
                    "user": "Show me 2 hashes",
                    "ai": "## The Title",
                },
                {
                    "user": "Show me 1 hash",
                    "ai": "#No Title\n# The Title",
                },
                {
                    "user": "Show me a separator",
                    "ai": "First line\n---\nSecond line",
                },
                {
                    "user": "Quoted header",
                    "ai": '## "What is this"',
                },
                {
                    "user": "Bullets",
                    "ai": "- One\n- Two\n- Three\naaaaaaaa",
                },
                {
                    "user": "Bullets",
                    "ai": "Hello\n- Uno\n- Dos\n- Tres\n44444",
                },
            ],
        }

        self.snippets_test: Test = {
            "items": [
                {
                    "user": "Normal Snippet",
                    "ai": "```python\na = 123\nprint('Hello, World!')```",
                },
                {
                    "user": "Normal Snippet (With an empty line at the end)",
                    "ai": "```python\na = 123\nprint('Hello, World!')\n```",
                },
                {
                    "user": "Malformed Snippet",
                    "ai": "```python\na = 123\nprint('Hello, World!')",
                },
                {
                    "user": "Malformed Snippets (With an empty line at the end)",
                    "ai": "```python\na = 123\nprint('Hello, World!')\n",
                },
                {
                    "user": "Normal message 1",
                    "ai": "Normal message 2",
                },
            ],
        }

        self.join_test: Test = {
            "items": [
                {
                    "user": "Some sentences, one per line",
                    "ai": "Hello dog\nHello cat\nHello bird",
                },
                {
                    "user": "Normal line",
                    "ai": "Normal line",
                },
            ],
        }

        self.asterisk_test: Test = {
            "items": [
                {
                    "user": "Normal line",
                    "ai": "Some *word like that for some reason and then *this* thing.",
                },
            ],
        }

        self.bullet_test: Test = {
            "items": [
                {
                    "user": "Weird bullet problem",
                    "ai": "The key change is within the `content` named capture group. I've replaced `[^\\*]` with `(?:[^\\*]|\\*(?!\\b\\w+\\*))`.  Let's break that down:\n* `(?: ... )` is a non-capturing group.\n* `[^\\*]`  matches any character that is *not* an asterisk. This is the original behavior.\n* `|` acts as an \"or\".\n* `\\*(?!\\b\\w+\\*)` This is the crucial addition. It matches an asterisk (`\\*`) only if it's *not* followed by:\n    * `\\b`: A word boundary.  This ensures we're checking for a whole word.\n    * `\\w+`: One or more word characters (letters, numbers, underscore). This is the \"word\" part.\n    * `\\*`:  A closing asterisk.\nThis effectively allows single asterisks within words while still capturing content between single asterisks that are intended for emphasis.",
                },
            ],
        }

        self.url_test: Test = {
            "items": [
                {
                    "user": "This is a markdown URL",
                    "ai": "[Click this URL](https://merkoba.com)",
                },
            ],
        }

        self.escape_test: Test = {
            "items": [
                {
                    "user": "Normal",
                    "ai": '"hello world"',
                },
                {
                    "user": "Escape test",
                    "ai": '"hello\\"world"',
                },
                {
                    "user": "Escape test",
                    "ai": "*hello\\*world*",
                },
                {
                    "user": "Escape test",
                    "ai": "`hello\\`world`",
                },
            ],
        }

        self.ref_test: Test = {
            "items": [
                {
                    "user": "Ref Test",
                    "ai": 'this thing: `rel="noreferrer"`',
                },
            ],
        }

    def get(self, name: str) -> Any:
        test_name = f"{name}_test"
        obj = getattr(self, test_name)
        obj["id"] = "ignore"
        obj["name"] = test_name.replace("_", " ").title()
        return obj


tests = Tests()
