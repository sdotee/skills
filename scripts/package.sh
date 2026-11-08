#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
project_dir=$(dirname "$script_dir")
output_dir="$project_dir/dist"
archive="$output_dir/see-agent-skill.zip"

mkdir -p "$output_dir"
rm -f "$archive"
cd "$project_dir/.claude/skills"
zip -qr "$archive" see -x '*/.DS_Store'
printf 'Created %s\n' "$archive"
