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

        for index, item in enumerate(pos):
            ## pre_cursor is a number which represents the previous "\n" location.
            pre_cursor[index] = self.view.line(pos[index]).begin() - 1
            # print("pre_cursor[index]: ",pre_cursor[index])
            ## cursor is a number which represents the end of the line location.
            cursor[index] = self.view.line(pos[index]).end()
            # print("cursor[index]: ",cursor[index])
            previous_line_str[index]   = ''
            previous_header[index]     = ''
            if(pre_cursor[index] >= 0):
                previous_line_str[index]     = self.view.substr(self.view.line(pre_cursor[index]))
                previous_header[index]       = re.search('^\s*[\+|\-|*]', previous_line_str[index])
                if(previous_header[index]):
                    previous_indent_level = previous_header[index].end()
                    # print("previous_indent_level: ",previous_indent_level)
            # print("previous_line_str[index]: ",previous_line_str[index])
            # print("previous_header[index]: ",previous_header[index])
            ## current line's investigation
            current_line_str[index]                = self.view.substr(self.view.line(pos[index]))
            # print("current_line_str[index]: ",current_line_str[index])
            current_header[index]                  = re.search('^\s*[\+|\-|\*]', current_line_str[index])
            ## rule1:  Current line has no header. And previous line has header.
            ## action: Input previous line's same header at indent level.
            if(not current_header[index]) and (previous_header[index]):
                # print("rule1")
                change_line = previous_line_str[index][:previous_indent_level] + " " + current_line_str[index].strip()
                # print("current_line_str[index].strip(): ",current_line_str[index].strip())
                # print("change_line: ",change_line)
                region = sublime.Region(pre_cursor[index] +1, cursor[index])
                ## Don't use "replace" because the area is selected.
                self.view.erase(edit, region)
                self.view.insert(edit, pos[index].a, change_line)
            ## rule2: Previous line and current line have a header.
            ## action: Indent down.
            elif (current_header[index]):
                # print("rule2")
                change_line = "\t"
                self.view.insert(edit, pre_cursor[index] + 1, change_line)
            ## rule3: Previous line and current line have no header.
            ## action: Making a header(*)
            elif (not current_header[index]) and (not previous_header[index]):
                # print("rule3")
                region = sublime.Region(pre_cursor[index] + 1, cursor[index])
                # print("region: "+str(region))
                ## Don't use "replace" because the area is selected.
                self.view.erase(edit, region)
                self.view.insert(edit, pos[index].a, "* " + current_line_str[index].strip())


class MarkdownIndentUpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownIndentUpCommand--------")
        my_tab_translate_tabs_to_spaces = self.view.settings().get('translate_tabs_to_spaces')
        my_tab_size = self.view.settings().get('tab_size')
        # print("my_tab_translate_tabs_to_spaces: ",my_tab_translate_tabs_to_spaces)
        # print("my_tab_size: ",my_tab_size)
        pos                 = self.view.sel()
        ## investigating the begining location of current line
        bgn_cursor           = [0 for i in range(len(pos))]
        current_line_str     = [0 for i in range(len(pos))]
        current_header       = [0 for i in range(len(pos))]

        for index, item in enumerate(pos):
            bgn_cursor[index] = self.view.line(pos[index]).begin()
            current_line_str[index]    = self.view.substr(self.view.line(pos[index]))
            current_header[index]      = re.search('^\s*[\+|\-|*]', current_line_str[index])
            # print("current_line_str: ",current_line_str)
            ## if current line has any header(* or + or -)
            if(current_header[index]):
                current_indent_level = current_header[index].end()
                # print("indent level of current line: ",current_indent_level)
                # print("header type of current line: ",current_header_str)
                ## if translate_tabs_to_spaces is true and the position of the list item doesn't exist at top level, delete spaces of my_tab_size.
                if(my_tab_translate_tabs_to_spaces):
                    if(current_indent_level > my_tab_size):
                        region = sublime.Region(bgn_cursor[index], bgn_cursor[index] + my_tab_size)
                        self.view.erase(edit, region)
                ## if translate_tabs_to_spaces is false and the position of the list item doesn't exist at top level, delete 1 str(=\tª.
                elif(current_indent_level > 1):
                    region = sublime.Region(bgn_cursor[index], bgn_cursor[index] + 1)
                    self.view.erase(edit, region)


class MarkdownNewLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownNewLineCommand--------")
        pos                 = self.view.sel()
        current_line_str     = [0 for i in range(len(pos))]
        current_header       = [0 for i in range(len(pos))]
        current_header_str   = [0 for i in range(len(pos))]
        current_indent_level = [0 for i in range(len(pos))]

        for index, item in enumerate(pos):
            current_line_str[index]     = self.view.substr(self.view.line(pos[index]))
            current_header[index]       = re.search('^\s*[\+|\-|*]', current_line_str[index])
            if(current_header[index]):
                current_indent_level[index]    = current_header[index].end()
                current_header_str[index]      = current_line_str[index][:current_indent_level[index]]
                self.view.insert(edit, pos[index].a, "\n" + current_header_str[index] + " ")


class MarkdownRotateListItem(sublime_plugin.TextCommand):
    def run(self, edit):
        # print("\n-------MarkdownRotateHeaderCommand--------")
        pos                 = self.view.sel()
        # print("len(pos): "+str(len(pos)))
        bgn_cursor          = [0 for i in range(len(pos))]
        cursor              = [0 for i in range(len(pos))]
        current_line_str    = [0 for i in range(len(pos))]
        for index, item in enumerate(pos):
            bgn_cursor[index] = self.view.line(pos[index]).begin()
            cursor[index]     = self.view.line(pos[index]).end()
            current_line_str[index] = self.view.substr(self.view.line(pos[index]))
            if(re.search('^\s*[\*]', current_line_str[index])):
                changed_header = current_line_str[index].replace("*", "+", 1)
            elif(re.search('^\s*[\+]', current_line_str[index])):
                changed_header = current_line_str[index].replace("+", "-", 1)
            elif(re.search('^\s*[\-]', current_line_str[index])):
                changed_header = current_line_str[index].replace("-", "*", 1)
            region = sublime.Region(bgn_cursor[index], cursor[index])
            self.view.replace(edit, region, changed_header)


class OutlineToTableCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        ## array for Header for Table
        header   = []
        ## 2dim array for Data for Table
        content   = [[]]
        ## longest indent level (initial value 1)
        longest_indent_level   = 1
        ## values for changing from array value to strings
        contentline   = ''
        ## dict for convert
        data    = {}
        data["_A"] = set()
        data["_notA"] = set()

        ## Get selected area(sel_area is array.)
        sel_area = self.view.sel()

        ## If selected area doesn't exist or exists two or more areas,
        if (sel_area[0].empty() or len(sel_area) > 1):
            sublime.message_dialog("Select any area.")
        ## If selected area exists one area,
        else:
            ## Input the values of selected area to "regien_text".
            region_text = self.view.substr(sel_area[0])
            ## Split to array with '\n'.
            arry_data = region_text.split('\n')

        # print (arry_data)

        ##### Make MdTableHeaders ######
        ## Make h1 instance as TableHeader object.
        h1                      = MdTableHeaders(arry_data)
        ## Extract longest indent level.
        longest_indent_level    = h1.calc_indent_level()
        ## Extract header values as arry.
        header                  = h1.get_header_element()
        ## Extract header values as characters with '|'
        header_line             = h1.add_header_separator(header)
        # print ("longest_indent_level: " + str(int(longest_indent_level)))
        # print ("----header--- \n" + str(header))
        # print ("header_line: \n" + header_line)

        ##### Make Contents #####
        # Make c1 instance as MdTableContents object.
        c1              = MdTableContents(longest_indent_level, arry_data)
        content         = c1.make_content_element()
        contentline     = c1.add_content_separator(content)

        ## Rewrite selected area
        self.view.replace(edit, sel_area[0], header_line + contentline)


class MdTableHeaders:
    def __init__(self, arry):
        self.arry = arry

    # Calcurate intdent level.
    def calc_indent_level(self):
        self.header = []
        self.present_indent_level = 1
        self.longest_indent_level = 1
        self.present_indent_num   = 0
        self.this_row = ''

        ## Extract Header value, column number, indent level.
        for row in self.arry:
            ## Confirm 'rows' first chalacter is '+'.
            is_header = re.search('^ *\+', row)
            ## If 'is header' first chalacter is '+',
            if(is_header):
                ## If 'is_header' location num is larger than 'self.present_indent_num',
                if(int(is_header.end()) > self.present_indent_num):
                    ## Set self.present_indent_num to 'is_header.end() - 1' as location info
                    self.present_indent_num   = is_header.end() - 1
                    ## Set self.present_indent_level
                    self.present_indent_level = int(self.present_indent_num / 4 + 1)
                    ## Delete the characters from the beginning until the '+' character appears.
                    self.this_row = re.sub('^\s{' + str(self.present_indent_num) + '}\+\s', '', row).rstrip('\n')
                    print (str(self.present_indent_level) +"th column is " + self.this_row)
                    ## Check the longest indent level
                    if(self.present_indent_level  > self.longest_indent_level):
                        self.longest_indent_level = self.present_indent_level
                    self.header.append(self.this_row)
        # print ("self.header: "+ str(self.header))
        return self.longest_indent_level

    # Return extracted headers.
    def get_header_element(self):
        return self.header

    # Add Header separator of Markdown
    def add_header_separator(self, arry):
        self.arry = arry
        self.header_line = ''
        ## Concatenate from Array to Charactor whose separator is '|' with join.
        self.header_line = '|' + '|'.join(self.arry) + '|\n'
        ## Make Markdown table separator.
        self.header_line += '|-' * len(self.arry) + '|\n'
        return self.header_line


class MdTableContents:
    def __init__(self, longest_indent_level, arry):
        # 2-dim arry for contents
        self.content = [[]]

        self.arry = arry
        self.present_row = ''
        self.present_indent_level = 1
        self.longest_indent_level = 1
        self.present_indent_num   = 0

    def make_content_element(self):
        self.itt  = 0
        self.cursor_indent_level = 0

        for row in self.arry:
            ## Confirm 'rows' first chalacter is '-'.
            self.present_row  = re.search('^ *\-', row)
            ## Process indent level 1 content as a unit.
            ## If 'is header' first chalacter is '-',
            if(self.present_row):
                self.present_indent_num   = self.present_row.end() - 1
                self.present_indent_level = self.present_indent_num / 4 + 1
                self.this_row = re.sub('^\s{' + str(self.present_indent_num) + '}\-\s', '', row).rstrip('\n')
                print (str(int(self.present_indent_level)) + "th column is " + self.this_row)

                if(self.present_row.end() == 1):
                    # Append array.
                    self.content.append([])
                    self.itt += 1
                    self.content[self.itt].append(self.this_row)

                elif(self.present_row.end() > 1):
                    ## If cursor indent level and present indent level is same,
                    if(self.present_indent_level == self.cursor_indent_level):
                        self.content[self.itt].append(self.this_row)
                    ## If cursor indent level and present indent level is NOT same,
                    elif(self.present_indent_level < self.cursor_indent_level):
                        self.content.append([])
                        self.itt += 1
                        for i in range(1, int(self.present_indent_level)):
                            self.content[self.itt].append('')
                        self.content[self.itt].append(self.this_row)
            # Set cursor to next indent level
            self.cursor_indent_level  = self.present_indent_level + 1
        # Appen the array element to make the all arry number same.
        for i in range(0, len(self.content)):
            for j in range(0, int(self.longest_indent_level - len(self.content[i]))):
                self.content[i].append('')
        self.content.pop(0)
        return self.content

    # Add Body separator of Markdown
    def add_content_separator(self, arry2dm):
        self.contentline = ''
        self.arry2dm = arry2dm

        for i in range(0, len(arry2dm)):
            self.contentline += '|' + '|'.join(arry2dm[i]) + '|\n'

        return self.contentline


class JsDocComplement(sublime_plugin.TextCommand):
    def run(self, edit):
        print("\n-------JsDocComplement--------")
        pos     = self.view.sel()

        for index, item in enumerate(pos):
            current_line_str = self.view.substr(self.view.line(pos[index]))
            result_line = re.search('^\s{0,}\/\*\*$', current_line_str)
            print("current_line_str: " + current_line_str)

            try:
                if(result_line.end()):
                    result_header = re.search('\/\*\*$', current_line_str)
                    print("detected at " + str(result_header.start()))
                    print(current_line_str.replace('/**', ' *'))
                    self.view.insert(edit, pos[index].a, "\n" + current_line_str.replace('/**', ' * \n') + current_line_str.replace('/**', ' */'))
                    self.view.run_command('goto_cursor_pos', {"point_str": pos[index].a -(len(current_line_str) + 1)})
            except AttributeError:
                self.view.insert(edit, pos[index].a, "\t")


class GotoCursorPosCommand(sublime_plugin.TextCommand):
    def run(self, edit, point_str):
        point = int(point_str)
        self.view.sel().clear()
        region = sublime.Region(point)
        self.view.sel().add(region)
        self.view.show(point)
