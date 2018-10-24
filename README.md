# Tmux Notepane

![screenshot](/screen.png)

`tmux-notepane` opens `~/.note/<CURRENT_PROGRAM>.note` in vim when the user hits a binding. 

### Description

It's meant to be user for quick personal notetaking of often-forgotten shortcuts/commands/options. It can be though of as a 'personal manpage' of sorts.

Tmux-notepane was written with the use of [libtmux](https://github.com/tmux-python/libtmux), so Python is a requirement.

It has only been tested on OSX. Information about use/bugs on other platforms is appreciated!

### Requirements

- `tmux 1.9` or higher

- **Python3** (2.7 should work, but the shell-script calls `python3 toggle_notepane.py`)

- [libtmux](https://github.com/tmux-python/libtmux)

### Key Bindings

- `Prefix + N` opens/closes a notepane

### Installation with [Tmux Plugin Manager](https://github.com/tmux-plugins/tpm) (recommended)

Add plugin to the list of TPM plugins in `.tmux.conf`:

    set -g @plugin 'alexsaalberg/tmux-notepane'

Hit `prefix + I` to fetch the plugin and source it. You should now be able to
use the plugin.

### Manual Installation

Clone the repo:

    $ git clone https://github.com/alexsaalberg/tmux-notepane ~/clone/path

Add this line to the bottom of `.tmux.conf`:

    run-shell ~/clone/path/tmux_notepane.tmux

Reload TMUX environment:

    # type this in terminal
    $ tmux source-file ~/.tmux.conf

You should now be able to use the plugin.

### Other Tmux Stuff

- [tmux-sidebar](tmux-plugins/tmux-sidebar) 
    - Inspiration for tmux-notepane
    - Also provided reference for how to create a plugin for Tmux (including using variables to save state)

