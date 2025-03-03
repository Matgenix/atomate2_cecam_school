#!/bin/bash
set -e

# Check if PROJECTNAME is defined. Mandatory. Error if missing
if [ -z "${PROJECTNAME}" ]; then
    echo "ERROR: PROJECTNAME environment variable must be defined"
    echo "Please set PROJECTNAME in your .env file"
    exit 1
fi

mkdir -p "${HOME}/.jfremote"

# Replace environment variables in the template
envsubst < "/tmp/jfremote_template.yaml" > "${HOME}/.jfremote/${PROJECTNAME}.yaml"

exec "$@"