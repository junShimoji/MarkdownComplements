# Markdown complements

This plugin provides functions to complement markdown header inputs or indent up/down.

![gif](https://immense-headland-55656.herokuapp.com/markdownComplements.gif)

## Sublime Text Version

The plugin requires Sublime Text 3.

## Instllation

### MacOS: 

    cd ~/"Library/Application Support/Sublime Text 3/Packages"
    git clone https://github.com/junShimoji/markdowncomplements.git MarkDownComplements

### Setting

There are 3 main functions.

1. markdown_indent_complements
If the line has a header(*,+ or -), it indent down. Else adds a header.

2. markdown_indent_up
If the line has a header(*,+ or -), it indent up. Else does nothing.

3. markdown_new_line
It provides new line with a header.

Use like as follows.

Open Preferences > Key Bindings

    { "keys": ["ctrl+enter"], "command": "markdown_indent_complements" },
    { "keys": ["shift+enter"], "command": "markdown_new_line" },
    { "keys": ["ctrl+shift+enter"], "command": "markdown_indent_up" }

