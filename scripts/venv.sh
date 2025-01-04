#!/usr/bin/env bash

root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"
cd "$parent"

rm -rf venv &&
python -m venv venv &&
venv/bin/pip install -r requirements.txt
