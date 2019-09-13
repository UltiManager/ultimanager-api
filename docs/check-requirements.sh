#!/bin/sh

# Ensure that the requirements file for installing the project on ReadTheDocs
# is up to date with the requirements from our Pipfile. This is necessary
# because ReadTheDocs does not support installing requirements using pipenv.
#
# See the following issue for details:
# https://github.com/rtfd/readthedocs.org/issues/3181

set -euf

# Generate the expected version of the requirements file
TEMP_REQUIREMENTS="$(mktemp /tmp/sync-requirements.XXXXXX)"
echo "Temporary requirements file: ${TEMP_REQUIREMENTS}"
pipenv lock --requirements > ${TEMP_REQUIREMENTS}
pipenv lock --dev --requirements >> ${TEMP_REQUIREMENTS}

# De-duplicate
cat "${TEMP_REQUIREMENTS}" | sort | uniq > "${TEMP_REQUIREMENTS}"

echo "Finished generating requirements to check against."

# Compare the expected requirements to the actual requirements. If the files
# are not equal, we exit with an error code and tell the user how to update the
# file.
(
  cmp $1 ${TEMP_REQUIREMENTS} || exit 1
  echo "$1 is up to date."
) || (
  echo "$1 is out of sync."
  echo
  echo "Please run:"
  echo "    lock-requirements.sh $1"
  exit 1
)
