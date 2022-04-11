#!/bin/bash

LIST=$(git diff --cached --name-only --diff-filter=ACRM)

for file in $LIST
do
    if [ "$file" == ".secrets.toml" ]; then
        echo You cannot commit file \'$file\'. Please reset it and try again.
        exit 1
    fi
done
exit 0
