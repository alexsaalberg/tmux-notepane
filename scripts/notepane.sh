#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

main() {
	python3 "$CURRENT_DIR/toggle_notepane.py" 
}
main 
