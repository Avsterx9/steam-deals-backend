#!/bin/bash

SCRIPT_PATH=$(realpath "$0")
ROOT_PATH=$(dirname "$(dirname "$SCRIPT_PATH")")
echo "Project path read as $ROOT_PATH"

if [ -f "$ROOT_PATH/.secrets.toml" ]; then
  echo "File '.secrets.toml' found. Skipping..."
elif [ -f "$ROOT_PATH/.secrets.toml.in" ] ; then
  echo "File '.secrets.toml.in' found. Renaming to '.secrets.toml'."
  cp "$ROOT_PATH/.secrets.toml.in" "$ROOT_PATH/.secrets.toml"
else
  echo "File '.secrets.toml' or '.secrets.toml.in' was not found. Do you have them in your root path?"
fi
