#!/bin/sh

set -euf

usage() {
  echo "Usage: lock-requirements.sh <dest>"
  echo
  echo "Lock the requirements from a Pipenv environment to a requirements.txt file."
  echo
  echo "Positional Arguments:"
  echo "  dest: The path to output the requirements.txt file to. This file will be"
  echo "        overwritten if it already exists."
  echo
}

if [ -z "${1+x}" ]; then
  echo "requirements.txt path not set."
  echo
  usage
  
  exit 1
fi

pipenv lock --requirements > "$1"
pipenv lock --dev --requirements >> "$1"

# De-duplicate lines
cat "$1" | LC_COLLATE=c sort | uniq | tee "$1"

