#!/bin/env sh
poetry run python -m nuitka --follow-imports src/REPL.py -o repl
rm -r REPL.build