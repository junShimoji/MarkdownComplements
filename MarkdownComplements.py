import sublime
import sublime_plugin
import re

class MarkdownIndentDownCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownIndentDownCommand--------")
        pos = self.view.sel()
        cursor = pos[0].a
        # cursor is a number which represents the location info.
        # print("cursor: ",cursor)
        # investigating the location of previous "\n"
        i = 1
        pre_cursor          = cursor
        previous_line_str   = ''
        previous_header     = ''
        while(True):
            pre_cursor -= 1
            previousChar = self.view.substr(pos[0].a-i)
            if(previousChar == '\n' or pre_cursor < 0):
                break
            i += 1
        # print("previous cursor's location: ",pre_cursor)
        if(pre_cursor >= 0):
            previous_line_str     = self.view.substr(self.view.line(pos[0].a-i))
            previous_header       = re.search('^ *[\+|\-|*]',previous_line_str)
            if(previous_header):
                previous_indent_level = previous_header.end()
                # print("previous_indent_level: ",previous_indent_level)
        # print("previous_header: ",previous_header)
        # print("previous_line_str: ",previous_line_str)
        # print("char num to previous enter(i): ",i)

        # current line's investigation
        current_line_str                = self.view.substr(self.view.line(pos[0].a))
        current_header                  = re.search('^ *[\+|\-|*]',current_line_str)
        # if current line has any header(* or + or -)
        if(current_header):
            current_indent_level    = current_header.end()
            current_header_str      = current_line_str[:current_indent_level]
            print("indent level of current line: ",current_indent_level)
            # print("location of current line's header: ",current_header.end())
            # print("header type of current line: ",current_header_str)

        # following line's investigation
        j = 0
        following_cursor    = cursor
        selfViewSize        = self.view.size()
        selfViewLine        = self.view.line(selfViewSize)
        # print("selfViewLine: ",selfViewLine.a)
        # print("cursor : ",cursor)
        # selfViewLine.a represents last line's location
        if(cursor < selfViewLine.a):
            while(True):
                following_cursor += 1
                afterChar = self.view.substr(pos[0].a+j)
                # print("afterChar: ",afterChar)
                if(afterChar == '\n' or following_cursor == 1000):
                    break
                j += 1
        # print("current_header: ",current_header)
        # print("current_line_str: ",current_line_str)
        # print("char num to next enter(j): ",j)

        ## rule1:  Current line has no header. And previous line has header.
        ## action: Input previous line's same header at indent level.
        if(not current_header) and (previous_header):
            # print("rule1")
            change_line = previous_line_str[:previous_indent_level] + " "
            # print("change_line: ",change_line)
            region = sublime.Region(pos[0].a-i+1, pos[0].a)
            self.view.erase(edit,region)
            self.view.insert(edit,pos[0].a,change_line)

        ## rule2: Previous line and current line have a header.
        ## action: Indent down.
        elif (current_header):
            # print("rule2")
            change_line = "\t"
            self.view.insert(edit,pos[0].a-i+1,change_line)
        ## rule3: Previous line and current line have no header.
        ## action: Making a header(*)
        elif (not current_header) and (not previous_header):
            # print("rule3")
            self.view.insert(edit,pos[0].a-i+1,"* ")

class MarkdownIndentUpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownIndentUpCommand--------")
        pos                 = self.view.sel()
        cursor              = pos[0].a

        # investigating the location of previous "\n"
        i = 1
        pre_cursor = cursor
        while(True):
            pre_cursor -= 1
            previousChar = self.view.substr(pos[0].a-i)
            if(previousChar == '\n' or pre_cursor < 0):
                break
            i += 1
        current_line_str    = self.view.substr(self.view.line(pos[0].a))
        current_header      = re.search('^ *[\+|\-|*]',current_line_str)
        # print("current_line_str: ",current_line_str)
        # print("char num to previous enter: ",i)
        ## if current line has any header(* or + or -)
        if(current_header):
            current_indent_level = current_header.end()
            current_header_str      = current_line_str[:current_indent_level]
            # print("indent level of current line: ",current_indent_level)
            # print("header type of current line: ",current_header_str)

            if(current_indent_level > 4):
                region = sublime.Region(pos[0].a-i+1, pos[0].a-i+5)
                self.view.erase(edit,region)
            else:
                if(current_header_str == "*"):
                    changed_header = current_line_str[0:current_header.end()].replace("*","+")
                elif(current_header_str == "+"):
                    changed_header = current_line_str[0:current_header.end()].replace("+","-")
                elif(current_header_str == "-"):
                    changed_header = current_line_str[0:current_header.end()].replace("-","*")
                region = sublime.Region(pos[0].a-i+1, pos[0].a-i+2)
                self.view.erase(edit,region)
                self.view.insert(edit,pos[0].a-i+2,changed_header)

class MarkdownNewLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownNewLineCommand--------")
        pos                 = self.view.sel()
        cursor              = pos[0].a

        current_line_str        = self.view.substr(self.view.line(pos[0].a))
        current_header          = re.search('^ *[\+|\-|*]',current_line_str)
        current_indent_level    = current_header.end()
        current_header_str      = current_line_str[:current_indent_level]
        # print("indent level of current line: ",current_indent_level)
        # print("location of current line's header: ",current_header.end())
        # print("header type of current line: ",current_header_str)

        if(current_header):
            self.view.insert(edit,pos[0].a,"\n"+current_header_str+" ")