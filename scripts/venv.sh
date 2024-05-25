#!/usr/bin/env bash
# This is used to install the python virtual env

root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"
cd "$parent"

rm -rf venv &&
python -m venv venv &&
venv/bin/pip install -r requirements.txt