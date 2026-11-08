#!/usr/bin/env sh
# Install the skill into the generic Agent Skills directory and link it
# into Claude Code's personal skills directory.
#
# Usage: install.sh [AGENTS_SKILLS_DIR] [CLAUDE_SKILLS_DIR]
#   AGENTS_SKILLS_DIR defaults to ~/.agents/skills
#   CLAUDE_SKILLS_DIR defaults to ~/.claude/skills
set -eu

script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
project_dir=$(dirname "$script_dir")
source_dir="$project_dir/.claude/skills/see"
agents_dir=${1:-"$HOME/.agents/skills"}
claude_dir=${2:-"$HOME/.claude/skills"}
target_dir="$agents_dir/see"
link_path="$claude_dir/see"

if [ -e "$target_dir" ] || [ -L "$target_dir" ]; then
  printf 'Refusing to overwrite existing skill: %s\n' "$target_dir" >&2
  exit 1
fi
if [ -e "$link_path" ] || [ -L "$link_path" ]; then
  printf 'Refusing to overwrite existing skill: %s\n' "$link_path" >&2
  exit 1
fi

mkdir -p "$agents_dir" "$claude_dir"
agents_dir=$(CDPATH='' cd -- "$agents_dir" && pwd -P)
claude_dir=$(CDPATH='' cd -- "$claude_dir" && pwd -P)
target_dir="$agents_dir/see"
cp -R "$source_dir" "$target_dir"
printf 'Installed S.EE skill at %s\n' "$target_dir"

if [ "$agents_dir" = "$claude_dir" ]; then
  printf 'Claude Code skills directory already resolves to %s; no link needed\n' "$agents_dir"
  exit 0
fi

ln -s "$target_dir" "$link_path"
printf 'Linked Claude Code skill %s -> %s\n' "$link_path" "$target_dir"
