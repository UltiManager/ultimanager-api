#!/bin/sh

# Ensure that the requirements file for installing the project on ReadTheDocs
# is up to date with the requirements from our Pipfile. This is necessary
# because ReadTheDocs does not support installing requirements using pipenv.
#
# See the following issue for details:
# https://github.com/rtfd/readthedocs.org/issues/3181

set -euf

# Check for each package currently specified in Pipfile.lock within the docs
# requirements file.
pipenv lock --requirements | while read line; do
  grep -q -- "${line}" $1 || (
    echo "$1 does not contain the line:"
    echo $line
    exit 1
  )
done

pipenv lock --dev --requirements | while read line; do
  grep -q -- "${line}" $1 || (
    echo "$1 does not contain the line:"
    echo $line
    exit 1
  )
done

