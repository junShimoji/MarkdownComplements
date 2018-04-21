import sublime
import sublime_plugin
import re
# import logging


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

        # ヘッダ用の配列
        header   = []
        i_header = []
        # コンテンツ用の二次元配列
        content   = [[]]
        i_content = [[]]
        # 最長インデントレベル(初期値は1)
        longest_indent_level   = 1
        i_longest_indent_level = 1
        # 配列を文字列化する時に使う変数
        contentLine   = ''
        i_contentLine = ''
        # コンバート用の辞書(連想配列)
        data    = {}
        data["_A"] = set()
        data["_notA"] = set()

        # 選択範囲(の開始と終了位置)を取得(複数箇所を選択できるからsel_areaは配列になる)
        sel_area = self.view.sel()

        # 選択箇所が無かった場合、または2箇所以上あった場合
        if (sel_area[0].empty() or len(sel_area) > 1):
            sublime.message_dialog("Select any area.")
        # 選択箇所が1箇所だった場合
        else:
            # 選択範囲を文字列用の変数に格納
            region_text = self.view.substr(sel_area[0])
            # 改行ごとに配列に変更
            arry_data = region_text.split('\n')

        # ヘッダ部分の処理
        h1                   = Headers(arry_data)
        longest_indent_level = h1.calcIndentLevel()
        header               = h1.getHeaderElement()
        headerLine           = h1.addHeaderSeparator(header)
        print ("longest_indent_level: " + str(int(longest_indent_level)))
        print ("----header---")
        print (header)
        print ("headerLine: \n" + headerLine)

        # コンテンツ部分の処理
        c1 = Contents(longest_indent_level,arry_data)
        content = c1.makeContentElement()
        contentLine = c1.addContentSeparator(content)

        ## 1st columnの情報を収集
        data["_A"] = c1.getColumnAElement()
        print (data["_A"])
        ## 1st column以外の情報を収集
        data["_notA"] = c1.getColumnNotAElement()
        print (data["_notA"])
        ## A以外の要素で作られた辞書を取得
        data = c1.getDataDictionary()

        for i in data["_notA"]:
            data[i] = []
            print("i: "+i)
            print(data[i])

        for p in data["_A"]:
            for m in data["_notA"]:
                if(m in data[p]):
                    print("_notA: " + m + " _A: "+p)
                    data[m].append(p)

        # 最大column数を検索
        for m in data["_notA"]:
            if (len(data[m]) >= i_longest_indent_level):
                print ("len(data[m]): " + str(len(data[m])))
                i_longest_indent_level = len(data[m]) +1  
        print ("i_longest_indent_level: " + str(i_longest_indent_level))

        # ヘッダ行の作成
        i_header.append('社員名')
        for p in range(i_longest_indent_level):
            i_header.append('')
        # 配列にデリミタをたして文字列化
        i_headerLine = '|' + '|'.join(i_header) + '\n'
        # セパレータを加える
        for i in range(0,i_longest_indent_level):
            i_headerLine += '|-'
        i_headerLine += '|\n'
        print("------i_header--------")
        print(i_header)
        print("------i_headerLine--------")
        print(i_headerLine)
        
        # データの作成
        it = 0
        for m in data["_notA"]:
            i_content.append([])
            it += 1
            i_content[it].append(m)
            for p in data[m]:
                i_content[it].append(p)
        i_content.pop(0)

        # 二次元配列の数を全て同じ数にする。
        for i in range(0,len(i_content)):
            for j in range(0,int(i_longest_indent_level - len(i_content[i]))):
                i_content[i].append('')
        print("------i_content--------")
        print(i_content)

        # 配列を文字列化(デリミタは「|」)
        for i in range(0,len(i_content)):
            i_contentLine += '|' + '|'.join(i_content[i]) + '|\n'
            i_contentLine += '|稼働種別' + '|\n'
            i_contentLine += '|稼働率' + '|\n'
            i_contentLine += '|' + '|\n'

        print("---i_contentLine----\n"+str(i_contentLine))


        # インバース処理
        i1 = Inverse(header)
        i1.test()
        # print (data)


        # 選択領域の置き換え
        self.view.replace(edit,sel_area[0],headerLine+contentLine)
        # self.view.insert(edit,sel_area[0].end(),"\n\n"+str(i_headerLine)+str(i_contentLine))
        # コンバード表の書き足し

# ヘッダ処理クラス
class Headers:
    def __init__(self,arry):
        self.arry = arry

    # インデントレベルの最大値を計算・ヘッダの抽出
    def calcIndentLevel(self):
        self.header = []
        self.present_indent_level = 1
        self.longest_indent_level = 1
        self.present_indent_num   = 0
        self.this_row = ''

        for row in self.arry:
            isHeader = re.search('^ *\+',row)
            if(isHeader):
                if(int(isHeader.end()) > self.present_indent_num):
                    self.present_indent_num   = isHeader.end() - 1
                    self.present_indent_level = self.present_indent_num/4+1
                    self.this_row = re.sub('^\s{'+str(self.present_indent_num)+'}\+\s','',row).rstrip('\n')
                    print (str(self.present_indent_level) +" column is " + self.this_row)
                    if(self.present_indent_level >= self.longest_indent_level):
                        self.longest_indent_level = self.present_indent_level
                    self.header.append(self.this_row)
        return self.longest_indent_level

    # 抽出したヘッダを返す
    def getHeaderElement(self):
        return self.header

    # ヘッダ行のしきり作成して文字列化
    def addHeaderSeparator(self,arry):
        self.arry = arry
        self.headerLine = ''

        self.headerLine = '|' + '|'.join(self.arry) + '|\n'
        for i in self.arry:
            self.headerLine += '|-'
        self.headerLine += '|\n'

        return self.headerLine

# コンテンツ処理クラス
class Contents:
    def __init__(self,longest_indent_level,arry):
        # データ用の辞書(連想配列)を作成
        self.data    = {}
        self.content = [[]]

        self.arry = arry
        self.isData = ''
        self.present_indent_level = 1
        self.longest_indent_level = 1
        self.present_indent_num   = 0

    def makeContentElement(self):
        self.data["_A"] = set()
        self.data["_notA"] = set()
        self.mainkey = ""
        self.this_row = ''
        self.itt  = 0
        self.contentLine = ''

        for row in self.arry:
            # インデントレベルの確認
            self.isData  = re.search('^ *\-',row)
            if(self.isData):
                self.present_indent_num   = self.isData.end()-1
                self.present_indent_level = self.present_indent_num/4+1
                # インデントレベル1の処理
                if self.present_indent_level == 1:
                    self.this_row = re.sub('^\s{'+str(self.present_indent_num)+'}\-\s','',row).rstrip('\n')
                    self.data["_A"].add(self.this_row)
                    self.mainkey = self.this_row
                    self.data[self.mainkey] = []
                    # print (str(int(present_indent_level)) + " column is " + this_row)
                    # 動的に二次元配列を作る。content[0]は最後に捨てる。
                    self.content.append([])
                    self.itt += 1
                    self.content[self.itt].append(self.this_row)

                # インデントレベル2以降の処理
                else:
                    self.this_row = re.sub('^\s{'+str(self.present_indent_num)+'}\-\s','',row).rstrip('\n')
                    # print (str(int(present_indent_level)) + " column is " + this_row)
                    if self.present_indent_level == self.cursor_indent_level:
                        self.content[self.itt].append(self.this_row)
                    elif self.present_indent_level < self.cursor_indent_level:
                        # レベル1でなくカーソルがあっていない場合は新しい配列要素を作る
                        self.content.append([])
                        self.itt += 1
                        for i in range(1,int(self.present_indent_level)):
                            self.content[self.itt].append('')
                        self.content[self.itt].append(self.this_row)

                    self.data[self.mainkey].append(self.this_row)
                    self.data["_notA"].add(self.this_row)

                self.cursor_indent_level  = self.present_indent_level +1

        # 二次元配列の数を全て同じ数にする。
        for i in range(0,len(self.content)):
            for j in range(0,int(self.longest_indent_level - len(self.content[i]))):
                self.content[i].append('')
        # 二次元配列の最初の捨て要素を捨てる
        self.content.pop(0)

        return self.content

    def getColumnAElement(self):
        return self.data["_A"]

    def getColumnNotAElement(self):
        return self.data["_notA"]

    def getDataDictionary(self):
        return self.data

    # 配列のデリミタを「|」にして文字列化
    def addContentSeparator(self,arry2dm):
        self.contentLine = ''
        self.arry2dm = arry2dm

        for i in range(0,len(arry2dm)):
            self.contentLine += '|' + '|'.join(arry2dm[i]) + '|\n'

        return self.contentLine

class Inverse:
    def __init__(self,arry):
        self.arry = arry

    def test(self):
        pass
        print ("hoge,fuga")

