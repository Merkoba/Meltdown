format_test = {
    "id": "ignore",
    "name": "Test",
    "items": [
        {"user": "Highlight Test"},
        {
            "ai": "Here is a `highlight` and `a longer highlight`.\nHere is a `highlight` and `a longer highlight`."
        },
        {"user": "Highlight Test 2"},
        {"ai": "`another highlight 123`"},
        {"user": "Bold Test"},
        {
            "ai": "Here is a bold **word** and **a bold sentence**.\nHere is a bold **word** and **a bold sentence**."
        },
        {"user": "Bold Test 2"},
        {
            "ai": "\n1) **Some Item:** Description\n2) **Another Item:** Description\n3) **Third Item:** Description"
        },
        {"user": "Bold Test 3"},
        {"ai": "**This is a bold sentence**\n**This is a bold sentence**"},
        {"user": "Italic Test with Asterisk"},
        {
            "ai": "Here is an italic *word* and *an italic sentence*.\nHere is an italic *word* and *an italic sentence*."
        },
        {"user": "Italic Test with Underscore"},
        {
            "ai": "Here is a an italic _word_ and _an italic sentence_.\nHere is a an italic _word_ and _an italic sentence_."
        },
        {"user": "Italic Test 3"},
        {"ai": "*This is an italic sentence*\n*This is an italic sentence*"},
        {"user": "Italic Test 4"},
        {"ai": "_This is an italic sentence_ 2\n_This is an italic sentence_ 2"},
        {"user": "Snippet Test"},
        {
            "ai": "```python\na = 123\nprint('Hello, World!')\n```\n\n"
            + "Here is more code:\n\n```js\nlet a = 123\nconsole.log('Hello, World!')\n```"
        },
        {"user": "Snippet Test 2"},
        {
            "ai": "Here is some code:\n\n```\na = 123\nprint('Hello, World!')\n```\n\n"
            + "Here is more code:\n\n```js\nlet a = 123\nconsole.log('Hello, World!')\n```"
        },
        {"user": "Snippet Test 3"},
        {"ai": "```python\na = 123\nprint('Hello, World!')\n```"},
        {"user": "Snippet Test 4"},
        {
            "ai": "Last snippet 1:\n```python\na = 123\nprint('Hello, World!')\nx = 6\n```\n"
            + "```python\na = 123\nprint('Hello, World!')\nx = 6\n```"
        },
        {"user": "URL Test"},
        {
            "ai": "Here are some urls https://aa.com and http://cc.com and ftp://44.com\n"
            + "Here are some urls https://aa.com and http://cc.com\nftp://44.com"
        },
        {"user": "Normal Sentence"},
        {"ai": "Here is a normal sentence"},
        {"user": "Loading dolphin-2_6-phi-2.Q5_K_M.gguf"},
        {"ai": "Ok"},
        {"user": "Here is a path /home/yo"},
        {"ai": "That is indeed /home/yo/file.txt"},
        {"user": 'This is "a quoted text"'},
        {"ai": 'That is a "quoted text".'},
        {"user": "Some backtick test"},
        {
            "ai": "Rendering LaTeX code as an image within a Tkinter Text widget can be achieved by using a combination of packages such as `mathjax` (to convert LaTeX to MathML) and `svglib`/`reportlab` (to convert MathML to SVG)"
        },
        {"user": "Show me 3 hashes"},
        {"ai": "### The Title"},
        {"user": "Show me 2 hashes"},
        {"ai": "## The Title"},
        {"user": "Show me 1 hash"},
        {"ai": "#No Title\n# The Title"},
        {"user": "Show me a separator"},
        {"ai": "First line\n---\nSecond line"},
        {"user": "Quoted header"},
        {"ai": '## "What is this"'},
        {"user": "Bullets"},
        {"ai": "- One\n- Two\n- Three"},
        {"user": "Bullets"},
        {"ai": "- One\n- Two\n- Three\naaaaaaaa"},
        {"user": "Bullets"},
        {"ai": "Hello\n- Uno\n- Dos\n- Tres\n44444"},
    ],
}

format_test_2 = {
    "id": "ignore",
    "name": "Test 2",
    "items": [
        {"user": "Some case"},
        {"ai": "* **Levixs**"},
    ],
}
