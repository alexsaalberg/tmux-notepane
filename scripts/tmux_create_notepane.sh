#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

main() {
	echo "$CURRENT_DIR/makepane.py"
	python3 "$CURRENT_DIR/makepane.py"
}
echo "test1"
main
