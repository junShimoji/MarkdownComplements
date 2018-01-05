import sublime
import sublime_plugin
import re

class MarkdownIndentDownCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownIndentDownCommand--------")
        pos = self.view.sel()
        ## pre_cursor is a number which represents the previous "\n" location.
        pre_cursor = self.view.line(pos[0]).begin()-1
        # print("pre_cursor: ",pre_cursor)
        ## cursor is a number which represents the end of the line location.
        cursor = self.view.line(pos[0]).end()
        # print("cursor: ",cursor)
        previous_line_str   = ''
        previous_header     = ''
        if(pre_cursor >= 0):
            previous_line_str     = self.view.substr(self.view.line(pre_cursor))
            previous_header       = re.search('^ *[\+|\-|*]',previous_line_str)
            if(previous_header):
                previous_indent_level = previous_header.end()
                # print("previous_indent_level: ",previous_indent_level)
        # print("previous_header: ",previous_header)
        # print("previous_line_str: ",previous_line_str)
        ## current line's investigation
        current_line_str                = self.view.substr(self.view.line(pos[0]))
        current_header                  = re.search('^ *[\+|\-|*]',current_line_str)
        ## if current line has any header(* or + or -)
        if(current_header):
            current_indent_level    = current_header.end()
            current_header_str      = current_line_str[:current_indent_level]
            # print("indent level of current line: ",current_indent_level)
            # print("header type of current line: ",current_header_str)
        ## rule1:  Current line has no header. And previous line has header.
        ## action: Input previous line's same header at indent level.
        if(not current_header) and (previous_header):
            # print("rule1")
            change_line = previous_line_str[:previous_indent_level] + " "+current_line_str.strip()
            # print("change_line: ",change_line)
            region = sublime.Region(pre_cursor+1, pos[0].a)
            ## Don't use "replace" because the area is selected.
            self.view.erase(edit,region)
            self.view.insert(edit,pos[0].a,change_line)
        ## rule2: Previous line and current line have a header.
        ## action: Indent down.
        elif (current_header):
            # print("rule2")
            change_line = "\t"
            self.view.insert(edit,pre_cursor+1,change_line)
        ## rule3: Previous line and current line have no header.
        ## action: Making a header(*)
        elif (not current_header) and (not previous_header):
            # print("rule3")
            region = sublime.Region(pre_cursor+1,cursor)
            # Don't use "replace" because the area is selected.
            self.view.erase(edit,region)
            self.view.insert(edit,pos[0].a,"* "+current_line_str.strip())

class MarkdownIndentUpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownIndentUpCommand--------")
        myTabSize = self.view.settings().get('tab_size')
        pos                 = self.view.sel()
        # investigating the begining location of current line
        bgn_cursor = self.view.line(pos[0]).begin()
        current_line_str    = self.view.substr(self.view.line(pos[0]))
        current_header      = re.search('^ *[\+|\-|*]',current_line_str)
        # print("current_line_str: ",current_line_str)
        ## if current line has any header(* or + or -)
        if(current_header):
            current_indent_level = current_header.end()
            current_header_str      = current_line_str[:current_indent_level]
            # print("indent level of current line: ",current_indent_level)
            # print("header type of current line: ",current_header_str)
            if(current_indent_level > myTabSize):
                region = sublime.Region(bgn_cursor, bgn_cursor+myTabSize)
                self.view.erase(edit,region)

class MarkdownNewLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownNewLineCommand--------")
        pos                 = self.view.sel()
        current_line_str        = self.view.substr(self.view.line(pos[0]))
        current_header          = re.search('^ *[\+|\-|*]',current_line_str)
        if(current_header):
            current_indent_level    = current_header.end()
            current_header_str      = current_line_str[:current_indent_level]
            self.view.insert(edit,pos[0].a,"\n"+current_header_str+" ")

class MarkdownRotateListItem(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownRotateHeaderCommand--------")
        pos                 = self.view.sel()
        bgn_cursor          = self.view.line(pos[0]).begin()
        cursor              = self.view.line(pos[0]).end()
        current_line_str    = self.view.substr(self.view.line(pos[0]))
        if(re.search('^ *[\*]',current_line_str)):
            changed_header = current_line_str.replace("*","+",1)
        elif(re.search('^ *[\+]',current_line_str)):
            changed_header = current_line_str.replace("+","-",1)
        elif(re.search('^ *[\-]',current_line_str)):
            changed_header = current_line_str.replace("-","*",1)
        region = sublime.Region(bgn_cursor, cursor)
        self.view.replace(edit,region,changed_header)
