#!/usr/bin/env bash

root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"
cd "$parent"

venv/bin/pip install -r llama_reqs.txt