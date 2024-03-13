#!/usr/bin/env bash
root="$(dirname "$(readlink -f "$0")")"
cd "$root"
venv/bin/python -m meltdown.main "$@"