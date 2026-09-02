#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
output_dir="$repo_root/dist"

mkdir -p "$output_dir"

for role in owner-management marketing-sales developer product finance operations recruiter-hr academic; do
  git -C "$repo_root" archive \
    --format=zip \
    --output="$output_dir/toolfit-$role.zip" \
    "HEAD:roles/$role"
done

printf 'Built role ZIPs in %s\n' "$output_dir"
