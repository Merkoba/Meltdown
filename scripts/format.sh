#!/usr/bin/env bash
root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"
autopep8 --in-place --recursive --aggressive --max-line-length=140 "$parent/src"