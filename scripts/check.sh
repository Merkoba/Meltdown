#!/usr/bin/env bash
source venv/bin/activate &&
cd meltdown
clear &&
ruff format && ruff check &&
mypy --strict --strict --strict main.py &&
pyright &&
deactivate