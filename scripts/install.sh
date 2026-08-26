#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_dir=$(dirname "$script_dir")
source_dir="$project_dir/.claude/skills/see"
skills_dir=${1:-"$HOME/.claude/skills"}
target_dir="$skills_dir/see"

mkdir -p "$skills_dir"
if [ -e "$target_dir" ]; then
  printf 'Refusing to overwrite existing skill: %s\n' "$target_dir" >&2
  exit 1
fi

cp -R "$source_dir" "$target_dir"
printf 'Installed S.EE skill at %s\n' "$target_dir"
