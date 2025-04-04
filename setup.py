from setuptools import setup, find_packages
from pathlib import Path
import shutil
import json
import platform

with open("meltdown/manifest.json", "r") as file:
    manifest = json.load(file)

title = manifest["title"]
program = manifest["program"]
version = manifest["version"]


def _post_install():
    system = platform.system()

    if system == "Linux":
        try:
            _copy_icon_file()
            _create_desktop_file()
        except Exception as e:
            print(f"Error during post install: {e}")


def _copy_icon_file():
    source = Path(f"{program}/icon.png").expanduser().resolve()
    destination = Path(f"~/.local/share/icons/{program}.png").expanduser().resolve()
    shutil.copy2(source, destination)


def _create_desktop_file():
    content = f"""[Desktop Entry]
Version=1.0
Name={title}
Exec={Path(f"~/.local/bin/{program}").expanduser().resolve()}
Icon={Path(f"~/.local/share/icons/{program}.png").expanduser().resolve()}
Terminal=false
Type=Application
Categories=Utility;
"""

    file_path = (
        Path(f"~/.local/share/applications/{program}.desktop").expanduser().resolve()
    )

    with open(file_path, "w") as f:
        f.write(content)


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("llama_reqs.txt") as f:
    llama_reqs = f.read().strip()

package_data = {}
package_data[program] = ["*.png", "*.jpg", "*.json"]

setup(
    name=title,
    version=version,
    install_requires=requirements,
    packages=find_packages(where="."),
    package_dir={"": "."},
    package_data=package_data,
    entry_points={
        "console_scripts": [
            f"{program}={program}.main:main",
        ],
    },
    extras_require={
        "llama": [llama_reqs],
    },
)

_post_install()
