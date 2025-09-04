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
                "user": """good morning i need to adapt this reflect algorithm which changes the rotation when the laser hits the surface of a circle area

however it's not working correctly for all angles

  App.safe_zone_reflect = (laser) => {
    let deg = App.get_direction(laser)
    let side = App.get_safe_zone_side(laser, App.safe_zone)
    let new_rotation

    if ([`top`, `bottom`].includes(side)) {
      new_rotation = App.reflect_angle_horizontal(deg)
    }
    else if ([`left`, `right`].includes(side)) {
      new_rotation = App.reflect_angle_vertical(deg)
    }
    else {
      new_rotation = laser.rotation + 180
    }

    laser.rotation = new_rotation
    laser.calc_velocities()
    laser.x += laser.vx * BOUNCE_PUSH
    laser.y += laser.vy * BOUNCE_PUSH
    App.safe_zone.charge_date = Date.now()
  }

  App.reflect_angle_horizontal = (heading) => {
    let reflected = 360 - heading
    return (reflected + 180) % 360
  }

  App.reflect_angle_vertical = (heading) => {
    let reflected = 360 - heading
    return reflected % 360
  }

i need the rotation to always be inverted in a minimum amount towards the outside of the circle because if it enters at any moment the laser disappears on the next tick.""",
                "ai": """The issue is that you're treating a circle like a rectangle with sides. For circular reflection, you need to reflect based on the normal vector at the collision point, not arbitrary "sides".

Here's the corrected approach:

```javascript
App.safe_zone_reflect = (laser) => {
  // Get the collision point and circle center
  let collision_point = { x: laser.x, y: laser.y }
  let center = { x: App.safe_zone.x, y: App.safe_zone.y }

  // Calculate the normal vector at collision point
  let normal_x = collision_point.x - center.x
  let normal_y = collision_point.y - center.y

  // Normalize the normal vector
  let normal_length = Math.sqrt(normal_x * normal_x + normal_y * normal_y)
  normal_x /= normal_length
  normal_y /= normal_length

  // Get current velocity components
  let speed = Math.sqrt(laser.vx * laser.vx + laser.vy * laser.vy)
  let vel_x = laser.vx
  let vel_y = laser.vy

  // Reflect velocity: v' = v - 2(v·n)n
  let dot_product = vel_x * normal_x + vel_y * normal_y
  let reflected_vx = vel_x - 2 * dot_product * normal_x
  let reflected_vy = vel_y - 2 * dot_product * normal_y

  // Convert back to rotation
  let new_rotation = Math.atan2(reflected_vy, reflected_vx) * (180 / Math.PI)
  if (new_rotation < 0) new_rotation += 360

  // Ensure the laser moves away from center (safety check)
  let away_angle = Math.atan2(normal_y, normal_x) * (180 / Math.PI)
  if (away_angle < 0) away_angle += 360

  // Check if reflection is pointing inward, if so, use outward direction
  let angle_diff = Math.abs(new_rotation - away_angle)
  if (angle_diff > 90 && angle_diff < 270) {
    new_rotation = away_angle
  }

  laser.rotation = new_rotation
  laser.calc_velocities()

  // Push laser outside the circle
  laser.x += normal_x * BOUNCE_PUSH
  laser.y += normal_y * BOUNCE_PUSH

  App.safe_zone.charge_date = Date.now()
}
```

This properly reflects off the circular surface and ensures the laser always moves away from the circle center.""",
            },
            {
                "user": "you didn't use 'speed' , why",
                "ai": """You're right, I calculated `speed` but didn't use it. That was an oversight - I should have used it to maintain the original speed magnitude after reflection.

Here's the corrected version:

```javascript
App.safe_zone_reflect = (laser) => {
  // Get the collision point and circle center
  let collision_point = { x: laser.x, y: laser.y }
  let center = { x: App.safe_zone.x, y: App.safe_zone.y }

  // Calculate the normal vector at collision point
  let normal_x = collision_point.x - center.x
  let normal_y = collision_point.y - center.y

  // Normalize the normal vector
  let normal_length = Math.sqrt(normal_x * normal_x + normal_y * normal_y)
  normal_x /= normal_length
  normal_y /= normal_length

  // Get current velocity components and speed
  let speed = Math.sqrt(laser.vx * laser.vx + laser.vy * laser.vy)
  let vel_x = laser.vx
  let vel_y = laser.vy

  // Reflect velocity: v' = v - 2(v·n)n
  let dot_product = vel_x * normal_x + vel_y * normal_y
  let reflected_vx = vel_x - 2 * dot_product * normal_x
  let reflected_vy = vel_y - 2 * dot_product * normal_y

  // Normalize and apply original speed
  let reflected_length = Math.sqrt(reflected_vx * reflected_vx + reflected_vy * reflected_vy)
  reflected_vx = (reflected_vx / reflected_length) * speed
  reflected_vy = (reflected_vy / reflected_length) * speed

  // Convert back to rotation
  let new_rotation = Math.atan2(reflected_vy, reflected_vx) * (180 / Math.PI)
  if (new_rotation < 0) new_rotation += 360

  laser.rotation = new_rotation
  laser.calc_velocities()

  // Push laser outside the circle
  laser.x += normal_x * BOUNCE_PUSH
  laser.y += normal_y * BOUNCE_PUSH

  App.safe_zone.charge_date = Date.now()
}
```

Now the reflected velocity maintains the original speed magnitude.""",
            }
        ]
    }


tests = Tests()
