#!/usr/bin/env python

# This is used to create a tag in the git repo
# You probably don't want to run this

# pacman: python-gitpython
import os
import git
import json
from pathlib import Path

here = Path(__file__).resolve()
parent = here.parent.parent
os.chdir(parent)

with open("meltdown/manifest.json") as f:
    manifest = json.loads(f.read())

version = manifest["version"]
repo = git.Repo(".")
repo.create_tag(version)
repo.remotes.origin.push(version)
print(f"Created tag: {version}")
