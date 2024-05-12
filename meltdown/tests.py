format_test = {
    "id": "ignore",
    "name": "Test",
    "items": [
        {"user": "Highlight Test"},
        {
            "assistant": "Here is a `highlight` and `a longer highlight`.\nHere is a `highlight` and `a longer highlight`."
        },
        {"user": "Highlight Test 2"},
        {"assistant": "`another highlight 123`"},
        {"user": "Bold Test"},
        {
            "assistant": "Here is a bold **word** and **a bold sentence**.\nHere is a bold **word** and **a bold sentence**."
        },
        {"user": "Bold Test 2"},
        {
            "assistant": "\n1) **Some Item:** Description\n2) **Another Item:** Description\n3) **Third Item:** Description"
        },
        {"user": "Bold Test 3"},
        {"assistant": "**This is a bold sentence**\n**This is a bold sentence**"},
        {"user": "Italic Test with Asterisk"},
        {
            "assistant": "Here is an italic *word* and *an italic sentence*.\nHere is an italic *word* and *an italic sentence*."
        },
        {"user": "Italic Test with Underscore"},
        {
            "assistant": "Here is a an italic _word_ and _an italic sentence_.\nHere is a an italic _word_ and _an italic sentence_."
        },
        {"user": "Italic Test 3"},
        {"assistant": "*This is an italic sentence*\n*This is an italic sentence*"},
        {"user": "Italic Test 4"},
        {"assistant": "_This is an italic sentence_ 2\n_This is an italic sentence_ 2"},
        {"user": "Snippet Test"},
        {
            "assistant": "```python\na = 123\nprint('Hello, World!')\n```\n\n"
            + "Here is more code:\n\n```js\nlet a = 123\nconsole.log('Hello, World!')\n```"
        },
        {"user": "Snippet Test 2"},
        {
            "assistant": "Here is some code:\n\n```\na = 123\nprint('Hello, World!')\n```\n\n"
            + "Here is more code:\n\n```js\nlet a = 123\nconsole.log('Hello, World!')\n```"
        },
        {"user": "Snippet Test 3"},
        {"assistant": "```python\na = 123\nprint('Hello, World!')\n```"},
        {"user": "Snippet Test 4"},
        {
            "assistant": "Last snippet 1:\n```python\na = 123\nprint('Hello, World!')\nx = 6\n```\n"
            + "```python\na = 123\nprint('Hello, World!')\nx = 6\n```"
        },
        {"user": "URL Test"},
        {
            "assistant": "Here are some urls https://aa.com and http://cc.com and ftp://44.com\n"
            + "Here are some urls https://aa.com and http://cc.com\nftp://44.com"
        },
        {"user": "Normal Sentence"},
        {"assistant": "Here is a normal sentence"},
        {"user": "Loading dolphin-2_6-phi-2.Q5_K_M.gguf"},
        {"assistant": "Ok"},
        {"user": "Here is a path /home/yo/file.txt"},
        {"assistant": "That is indeed /home/yo/file.txt"},
    ],
}
