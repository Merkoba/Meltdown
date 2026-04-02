#!/usr/bin/env bash

root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"
cd "$parent"

venv/bin/pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir --no-binary llama-cpp-python -r llama_reqs.txt