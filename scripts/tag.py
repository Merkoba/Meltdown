#!/usr/bin/env python

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
