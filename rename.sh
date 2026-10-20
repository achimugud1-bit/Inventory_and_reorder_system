#!/usr/bin/env bash
# rename.sh — put your teammates' real names on their folders & files.
# Usage (from the project root):
#   ./rename.sh name2 name3 name4 name5 name6 name7
# Example:
#   ./rename.sh cynthia nnamdi amaka ibrahim chidera emeka
set -e
cd "$(dirname "$0")"
i=2
for new in "$@"; do
  old="member$i"
  if [ -d "members/$old" ] && [ "$old" != "$new" ]; then
    mv "members/$old" "members/$new"
    grep -rl "members/$old" . --exclude=rename.sh 2>/dev/null | xargs -r sed -i "s|members/$old|members/$new|g"
    grep -rl "\"$old\"" . --exclude=rename.sh 2>/dev/null | xargs -r sed -i "s|\"$old\"|\"$new\"|g"
    grep -rl "OWNER: $old" . 2>/dev/null | xargs -r sed -i "s|OWNER: $old|OWNER: $new|g"
    grep -rl "owner: <b>$old</b>" . 2>/dev/null | xargs -r sed -i "s|owner: <b>$old</b>|owner: <b>$new</b>|g"
    grep -rl "written by $old" . 2>/dev/null | xargs -r sed -i "s|written by $old|written by $new|g"
    echo "✔ member$i → $new"
  fi
  i=$((i+1))
done
echo "✔ done. test with: python3 run.py"
