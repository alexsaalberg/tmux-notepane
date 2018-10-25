# Tmux Notepane

![screenshot](/screen.png)

`tmux-notepane` opens `~/.note/<CURRENT_PROGRAM>.note` in vim when the user hits a binding. 

*Important: Unlike most tmux plugins, tmux-notepane requires python and libtmux (see installation instructions below)*

### Description

It's meant to be user for quick personal notetaking of often-forgotten shortcuts/commands/options. It can be though of as a 'personal manpage' of sorts.

Tmux-notepane was written with the use of [libtmux](https://github.com/tmux-python/libtmux), so python is a requirement.

It has only been tested on OSX. Information about use/bugs on other platforms is appreciated!

### Key Bindings

- `Prefix + N` opens/closes a notepane

### Use

1. Hit the binding to open a document specific to the current program (bash, vim, etc.)

    - By default the path to this document is `~/.note/<PROGRAM>.note`
    
2. Write whatever you want to remember or have reference to in the document

3. Hit the binding again to close the document. (You don't have to worry about saving, that will be done automatically)

4. Open the document again later when you need reference to whatever information you just recorded

### Requirements

- `tmux 1.9` or higher

- Python3 (2.7 might work, but is untested)

- [libtmux](https://github.com/tmux-python/libtmux)

### Installation with [Tmux Plugin Manager](https://github.com/tmux-plugins/tpm) (recommended)

Install [libtmux](https://github.com/tmux-python/libtmux)

    $ [sudo] pip install libtmux

Add plugin to the list of TPM plugins in `.tmux.conf`:

    set -g @plugin 'alexsaalberg/tmux-notepane'

Hit `prefix + I` to fetch the plugin and source it. You should now be able to
use the plugin.

### Manual Installation

Install [libtmux](https://github.com/tmux-python/libtmux)

    $ [sudo] pip install libtmux

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

