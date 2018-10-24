#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

main() {
	if [ -x "$(command -v python3)" ]; then
		python3 "$CURRENT_DIR/toggle_notepane.py" 
	elif [ -x "$(command -v python)" ]; then
		python "$CURRENT_DIR/toggle_notepane.py"
	else
		echo 'python is required to use tmux-notepane'
	fi
}
main 
