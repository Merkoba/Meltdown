from setuptools import setup, find_packages
from pathlib import Path
import shutil


def _post_install():
    try:
        _copy_icon_file()
        _create_desktop_file()
    except Exception as e:
        print(f"Error during post install: {e}")


def _copy_icon_file():
    source = Path("meltdown/icon.png").expanduser().resolve()
    destination = Path("~/.local/share/icons/meltdown.png").expanduser().resolve()
    shutil.copy2(source, destination)


def _create_desktop_file():
    content = f"""[Desktop Entry]
Version=1.0
Name=Meltdown
Exec={Path("~/.local/bin/meltdown").expanduser().resolve()}
Icon={Path("~/.local/share/icons/meltdown.png").expanduser().resolve()}
Terminal=false
Type=Application
Categories=Utility;
"""

    file_path = Path("~/.local/share/applications/meltdown.desktop").expanduser().resolve()

    with open(file_path, 'w') as f:
        f.write(content)


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Meltdown",
    version="1.0.0",
    install_requires=requirements,
    packages=find_packages(where="."),
    package_dir={"": "."},
    package_data={
        "meltdown": ["*.png"],
    },
    entry_points={
        "console_scripts": [
            "meltdown=meltdown.main:main",
        ],
    },
)

_post_install()
