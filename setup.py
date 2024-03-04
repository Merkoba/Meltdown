from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Meltdown",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "."},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "meltdown = main:main",
        ],
    },
)