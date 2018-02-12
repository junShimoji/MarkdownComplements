import sublime
import sublime_plugin
import re

class MarkdownIndentDownCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownIndentDownCommand--------")
        pos = self.view.sel()
        pre_cursor        = [0 for i in range(len(pos))]
        cursor            = [0 for i in range(len(pos))]
        previous_line_str = [0 for i in range(len(pos))]
        previous_header   = [0 for i in range(len(pos))]
        current_line_str  = [0 for i in range(len(pos))]
        current_header    = [0 for i in range(len(pos))]

        for index,item in enumerate(pos):
            ## pre_cursor is a number which represents the previous "\n" location.
            pre_cursor[index] = self.view.line(pos[index]).begin()-1
            # print("pre_cursor[index]: ",pre_cursor[index])
            ## cursor is a number which represents the end of the line location.
            cursor[index] = self.view.line(pos[index]).end()
            # print("cursor[index]: ",cursor[index])
            previous_line_str[index]   = ''
            previous_header[index]     = ''
            if(pre_cursor[index] >= 0):
                previous_line_str[index]     = self.view.substr(self.view.line(pre_cursor[index]))
                previous_header[index]       = re.search('^\s*[\+|\-|*]',previous_line_str[index])
                if(previous_header[index]):
                    previous_indent_level = previous_header[index].end()
                    # print("previous_indent_level: ",previous_indent_level)
            # print("previous_line_str[index]: ",previous_line_str[index])
            # print("previous_header[index]: ",previous_header[index])
            ## current line's investigation
            current_line_str[index]                = self.view.substr(self.view.line(pos[index]))
            # print("current_line_str[index]: ",current_line_str[index])
            current_header[index]                  = re.search('^\s*[\+|\-|\*]',current_line_str[index])
            ## if current line has any header(* or + or -)
            if(current_header[index]):
                current_indent_level    = current_header[index].end()
                current_header_str      = current_line_str[index][:current_indent_level]
                # print("indent level of current line: ",current_indent_level)
                # print("header type of current line: ",current_header_str)
            ## rule1:  Current line has no header. And previous line has header.
            ## action: Input previous line's same header at indent level.
            if(not current_header[index]) and (previous_header[index]):
                # print("rule1")
                change_line = previous_line_str[index][:previous_indent_level] + " "+current_line_str[index].strip()
                # print("current_line_str[index].strip(): ",current_line_str[index].strip())
                # print("change_line: ",change_line)
                region = sublime.Region(pre_cursor[index]+1, cursor[index])
                ## Don't use "replace" because the area is selected.
                self.view.erase(edit,region)
                self.view.insert(edit,pos[index].a,change_line)
            ## rule2: Previous line and current line have a header.
            ## action: Indent down.
            elif (current_header[index]):
                # print("rule2")
                change_line = "\t"
                self.view.insert(edit,pre_cursor[index]+1,change_line)
            ## rule3: Previous line and current line have no header.
            ## action: Making a header(*)
            elif (not current_header[index]) and (not previous_header[index]):
                # print("rule3")
                region = sublime.Region(pre_cursor[index]+1,cursor[index])
                # print("region: "+str(region))
                ## Don't use "replace" because the area is selected.
                self.view.erase(edit,region)
                self.view.insert(edit,pos[index].a,"* "+current_line_str[index].strip())

class MarkdownIndentUpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownIndentUpCommand--------")
        myTabtranslateTabsToSpaces = self.view.settings().get('translate_tabs_to_spaces')
        myTabSize = self.view.settings().get('tab_size')
        # print("myTabtranslateTabsToSpaces: ",myTabtranslateTabsToSpaces)
        # print("myTabSize: ",myTabSize)
        pos                 = self.view.sel()
        ## investigating the begining location of current line
        bgn_cursor           = [0 for i in range(len(pos))]
        current_line_str     = [0 for i in range(len(pos))]
        current_line_header  = [0 for i in range(len(pos))]
        current_header       = [0 for i in range(len(pos))]

        for index,item in enumerate(pos):
            bgn_cursor[index] = self.view.line(pos[index]).begin()
            current_line_str[index]    = self.view.substr(self.view.line(pos[index]))
            current_header[index]      = re.search('^\s*[\+|\-|*]',current_line_str[index])
            # print("current_line_str: ",current_line_str)
            ## if current line has any header(* or + or -)
            if(current_header[index]):
                current_indent_level = current_header[index].end()
                current_header_str      = current_line_str[index][:current_indent_level]
                # print("indent level of current line: ",current_indent_level)
                # print("header type of current line: ",current_header_str)
                ## if translate_tabs_to_spaces is true and the position of the list item doesn't exist at top level, delete spaces of myTabSize.
                if(myTabtranslateTabsToSpaces):
                    if(current_indent_level > myTabSize):
                        region = sublime.Region(bgn_cursor[index], bgn_cursor[index]+myTabSize)
                        self.view.erase(edit,region)
                ## if translate_tabs_to_spaces is false and the position of the list item doesn't exist at top level, delete 1 str(=\tª.
                elif(current_indent_level > 1):
                    region = sublime.Region(bgn_cursor[index], bgn_cursor[index]+1)
                    self.view.erase(edit,region)

class MarkdownNewLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownNewLineCommand--------")
        pos                 = self.view.sel()
        current_line_str     = [0 for i in range(len(pos))]
        current_line_header  = [0 for i in range(len(pos))]
        current_header       = [0 for i in range(len(pos))]
        current_header_str   = [0 for i in range(len(pos))]
        current_indent_level = [0 for i in range(len(pos))]

        for index,item in enumerate(pos):
            current_line_str[index]     = self.view.substr(self.view.line(pos[index]))
            current_header[index]       = re.search('^\s*[\+|\-|*]',current_line_str[index])
            if(current_header[index]):
                current_indent_level[index]    = current_header[index].end()
                current_header_str[index]      = current_line_str[index][:current_indent_level[index]]
                self.view.insert(edit,pos[index].a,"\n"+current_header_str[index]+" ")

class MarkdownRotateListItem(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownRotateHeaderCommand--------")
        pos                 = self.view.sel()
        print("len(pos): "+str(len(pos)))
        bgn_cursor          = [0 for i in range(len(pos))]
        cursor              = [0 for i in range(len(pos))]
        current_line_str    = [0 for i in range(len(pos))]
        for index,item in enumerate(pos):
            bgn_cursor[index] = self.view.line(pos[index]).begin()
            cursor[index]     = self.view.line(pos[index]).end()
            current_line_str[index] = self.view.substr(self.view.line(pos[index]))
            if(re.search('^\s*[\*]',current_line_str[index])):
                changed_header = current_line_str[index].replace("*","+",1)
            elif(re.search('^\s*[\+]',current_line_str[index])):
                changed_header = current_line_str[index].replace("+","-",1)
            elif(re.search('^\s*[\-]',current_line_str[index])):
                changed_header = current_line_str[index].replace("-","*",1)
            region = sublime.Region(bgn_cursor[index], cursor[index])
            self.view.replace(edit,region,changed_header)
