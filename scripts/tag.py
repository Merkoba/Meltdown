#!/usr/bin/env python

# This is used to create a tag in the git repo
# You probably don't want to run this

# pacman: python-gitpython
import os
import git
import time
from pathlib import Path

here = Path(__file__).resolve()
parent = here.parent.parent
os.chdir(parent)

name = int(time.time())
repo = git.Repo(".")
repo.create_tag(name)
repo.remotes.origin.push(name)
print(f"Created tag: {name}")