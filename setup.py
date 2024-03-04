from setuptools import setup, find_packages

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