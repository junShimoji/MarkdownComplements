# Markdown complements

This plugin provides functions to complement markdown header inputs or indent up/down.

![gif](https://immense-headland-55656.herokuapp.com/markdownComplements.gif)

## Sublime Text Version

The plugin requires Sublime Text 3.

## Installation

### MacOS: 

    cd ~/"Library/Application Support/Sublime Text 3/Packages"
    git clone https://github.com/junShimoji/markdowncomplements.git MarkDownComplements

### Windows:

    cd ~/"Library/Application Support/Sublime Text 3/Packages"
    git clone https://github.com/junShimoji/markdowncomplements.git MarkDownComplements

### Settings

There are 4 plug-ins.

1. markdown_indent_down

If the focus line has a header(\*,+ or -), then you can indent down.
If the focus line has no header(\*,+ or -), you can adds a header automatically.

2. markdown_indent_up

If the line has a header(\*,+ or -), it indent up.

3. markdown_new_line

It provides new line with a header.

4. markdown_rotate_header

If a header(\*,+ or -) exists, the header lotates like \* -> + -> - * ....

Use as follows.

Open Preferences > Key Bindings and add as follows

    { "keys": ["ctrl+enter"], "command": "markdown_indent_down" },
    { "keys": ["ctrl+shift+enter"], "command": "markdown_indent_up" },
    { "keys": ["command+enter"], "command": "markdown_new_line" },
    { "keys": ["shift+enter"], "command": "markdown_rotate_header" }


