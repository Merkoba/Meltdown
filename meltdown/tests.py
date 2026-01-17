# Standard
from typing import Any


Test = dict[str, Any]


class Tests:
    @staticmethod
    def get(name: str) -> Any:
        test_name = f"{name}_test"

        if not hasattr(Tests, test_name):
            return None

        obj = getattr(Tests, test_name)
        obj["id"] = "ignore"
        obj["name"] = test_name.replace("_", " ").title()
        return obj

    format_test: Test = {
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
                "user": "Snippet Test 5",
                "ai": "```arrocado brokas```",
            },
            {
                "user": "Snippet Test 6",
                "ai": "```crotcas catum```",
            },
            {
                "user": """Snippet Test 7""",
                "ai": """Test

            ```js
            some line
            another line
            ```

more text""",
            },
            {
                "user": """Snippet Test 8""",
                "ai": '```bash\nwhile true; do echo "Hello, World!"; sleep 1; done\n```',
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
            {
                "user": """Glue Test""",
                "ai": """1. **Glazed Walnuts:**
	* In a small skillet, combine honey, water, and salt. Bring to a simmer over medium heat.
	* Add the walnuts to the skillet, stirring to coat them evenly with the honey mixture. Cook for 2-3 minutes, or until the nuts are glazed and golden.
	* Transfer the walnuts to a parchment-lined baking sheet, using a spoon to spread them out in a single layer. Allow them to cool.
2. **Assembly:**
	* Spoon some of the reserved poaching liquid into the bottom of each serving dish.
	* Place a poached pear upright in each dish.
	* Top each pear with a generous amount of gingerbread crumble and glazed walnuts.
	* Serve immediately, and enjoy the symphony of flavors and textures in this glue-inspired dessert.""",
            },
        ],
    }

    snippets_test: Test = {
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

    join_test: Test = {
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

    asterisk_test: Test = {
        "items": [
            {
                "user": "Normal line",
                "ai": "Some *word like that for some reason and then *this* thing.",
            },
        ],
    }

    bullet_test: Test = {
        "items": [
            {
                "user": "Weird bullet problem",
                "ai": "The key change is within the `content` named capture group. I've replaced `[^\\*]` with `(?:[^\\*]|\\*(?!\\b\\w+\\*))`.  Let's break that down:\n* `(?: ... )` is a non-capturing group.\n* `[^\\*]`  matches any character that is *not* an asterisk. This is the original behavior.\n* `|` acts as an \"or\".\n* `\\*(?!\\b\\w+\\*)` This is the crucial addition. It matches an asterisk (`\\*`) only if it's *not* followed by:\n    * `\\b`: A word boundary.  This ensures we're checking for a whole word.\n    * `\\w+`: One or more word characters (letters, numbers, underscore). This is the \"word\" part.\n    * `\\*`:  A closing asterisk.\nThis effectively allows single asterisks within words while still capturing content between single asterisks that are intended for emphasis.",
            },
        ],
    }

    url_test: Test = {
        "items": [
            {
                "user": "This is a markdown URL",
                "ai": "[Click this URL](https://merkoba.com)",
            },
        ],
    }

    escape_test: Test = {
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

    ref_test: Test = {
        "items": [
            {
                "user": "Ref Test",
                "ai": 'this thing: `rel="noreferrer"`',
            },
        ],
    }

    p5list_test: Test = {
        "items": [
            {
                "user": "p5list Test",
                "ai": """3.  **webgl-fluid:**
*   **Description:** Focuses specifically on fluid simulation in WebGL, and you can create beautiful, flowing, Milkdrop-like visuals with it.
*   **Lightweight?:** Relatively light, very focused.
*   **GitHub:** Some link here
*   **Pros:** Great for fluid visuals, efficient.
*   **Cons:** Limited to fluid-style visual effects.
*   **How to use:** You'd use it's fluid sim engine and render to canvas.
""",
            },
        ],
    }

    drum_test: Test = {
        "items": [
            {
                "user": "Drum list",
                "ai": """*   **FPC (FL Studio Plugin):** I mentioned this before, but it's worth highlighting again. It comes *free* with FL Studio, and it's a powerful drum sampler. You just need to load in your own samples (which there are many free ones online) or use the included ones. It's very versatile.
*   **MT Power Drum Kit 2:** This is a very popular free drum sampler that comes with a decent acoustic drum kit and various mixing options. It's known for its realistic sound.
*   **SSD5 Free (Steven Slate Drums):** Steven Slate Drums offers a free version of their SSD5 drum plugin. It includes a single drum kit that sounds fantastic and is great for modern, punchy drums.
*   **Sitala:** This is a very simple and intuitive sampler that's great for creating drum kits. It has a very clean interface.
""",
            },
            {
                "user": "Drum list 2",
                "ai": """1)   **FPC (FL Studio Plugin):** I mentioned this before, but it's worth highlighting again. It comes *free* with FL Studio, and it's a powerful drum sampler. You just need to load in your own samples (which there are many free ones online) or use the included ones. It's very versatile.
2)   **MT Power Drum Kit 2:** This is a very popular free drum sampler that comes with a decent acoustic drum kit and various mixing options. It's known for its realistic sound.
3)   **SSD5 Free (Steven Slate Drums):** Steven Slate Drums offers a free version of their SSD5 drum plugin. It includes a single drum kit that sounds fantastic and is great for modern, punchy drums.
4)   **Sitala:** This is a very simple and intuitive sampler that's great for creating drum kits. It has a very clean interface.
""",
            },
            {
                "user": "Drum list 3",
                "ai": "*   `{2}`: Exactly two of the preceding item",
            },
        ],
    }

    what_test: Test = {
        "items": [
            {
                "user": "What do test",
                "ai": "aaa **What You *Can* Do in Python:** aaa",
            },
        ],
    }

    singlelist_test: Test = {
        "items": [
            {
                "user": "What do test",
                "ai": "aaaaaaa\n\n* bbbbbbbb\n\ncccccccc",
            },
            {
                "user": "What do test 2",
                "ai": "aaaaaaa\n\n* bbbbbbbb\n\ncccccccc\n* aaaaaaa\n* bbbbbbbb",
            },
        ],
    }

    snippet_test: Test = {
        "items": [
            {
                "user": """Snippet test""",
                "ai": """```python
def debug_print(var_name, value):
    print(f"DEBUG: {var_name} = {value} (type: {type(value).__name__})")
    return value
```""",
            },
        ]
    }

    slash_test: Test = {
        "items": [
            {
                "user": """Slash test""",
                "ai": """/m/ slash test""",
            },
        ]
    }


tests = Tests()
