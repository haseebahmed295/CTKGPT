import re
from tkinter import *
from collections import deque
 
 
class Text_hightlighter:
    def __init__(self, master , Text):
        self.master = master
        self.master.option_add("*Font", "Verdana 12")
        self.stack = deque(maxlen = 10)
        self.stackcursor = 0

 
        self.T1 = Text
 
        self.T1.tag_config("orange", foreground = "orange")
        self.T1.tag_config("blue", foreground = "blue")
        self.T1.tag_config("purple", foreground = "purple")
        self.T1.tag_config("green", foreground = "green")
        self.T1.tag_config("red", foreground = "red")

        self.T1.tag_config("gray_background", background = "gray")

 
        self.tags = ["blue", "orange", "purple", "red" , "green"]

        
 
        self.wordlist = [ ["class", "def", "for", "if", "else","num" ,"or", "elif","import", "from", "as", "break", "while"],
                          ["int", "string", "float", "bool",'or' , "__init__" ,"print", "return", "del", "True", "False"],
                          ["pygame", "tkinter", "sys", "os", "mysql"],
                          ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]]
 

        #---------
 
    def tagHighlight(self , start_index, end_index):
        start = start_index
        end = float(int(float(end_index))-1)
         
        for mylist in self.wordlist:
            num = int(self.wordlist.index(mylist))
 
            for word in mylist:
                self.T1.mark_set("matchStart", start)
                self.T1.mark_set("matchEnd", start)
                self.T1.mark_set("SearchLimit", end)
 
                mycount = IntVar()
                 
                while True:
                    index= self.T1.search(word,"matchEnd","SearchLimit", count=mycount, regexp = True)
 
                    if index == "": break
                    if mycount.get() == 0: break
 
                    self.T1.mark_set("matchStart", index)
                    self.T1.mark_set("matchEnd", f"{index}+{mycount.get()}c")
 
                    preIndex = "%s-%sc" % (index, 1)
                    postIndex = "%s+%sc" % (index, mycount.get())
                     
                    if self.check(index, preIndex, postIndex):
                        self.T1.tag_add(self.tags[num], "matchStart", "matchEnd")
                         
    def check(self, index, pre, post):
        letters = [chr(ord('a') + i) for i in range(26)]

        if self.T1.get(pre) == self.T1.get(index):
            pre = index
        elif self.T1.get(pre) in letters:
            return 0

        if self.T1.get(post) in letters:
            return 0

        return 1
    
    def scan(self ,start_index,end_index):
        start = start_index
        end = end_index
        my_count = IntVar()
    # patterns to search '' brackets and # coments
        regex_patterns = [r'\".*?\"',r'\'.*?\'', r'#.']
    
        for pattern in regex_patterns:
            self.T1.mark_set("start", start)
            self.T1.mark_set("end", end)
    
            num = regex_patterns.index(pattern)
    
            while True:
                index = self.T1.search(pattern, "start", "end", count=my_count, regexp=True)
    
                if index == "":
                    break
                    
                if num == 2:
                    self.T1.tag_add(self.tags[4], index, index + " lineend")
                elif num == 0 or num == 1:
                    self.T1.tag_add(self.tags[3], index, f"{index}+{my_count.get()}c")

                self.T1.mark_set("start", f"{index}+{my_count.get()}c")
 
    def indent(self, widget):

        index1 = widget.index("insert")
        index2 = "%s-%sc" % (index1, 1)
        prevIndex = widget.get(index2, index1)
 
        prevIndentLine = widget.index(index1 + "linestart")
        print("prevIndentLine ",prevIndentLine)
        prevIndent = self.getIndex(prevIndentLine)
        print("prevIndent ", prevIndent)
 
 
        if prevIndex == ":":
            widget.insert("insert", "\n" + "     ")
            widget.mark_set("insert", "insert + 1 line + 5char")
 
            while widget.compare(prevIndent, ">", prevIndentLine):
                widget.insert("insert", "     ")
                widget.mark_set("insert", "insert + 5 chars")
                prevIndentLine += "+5c"
            return "break"
         
        elif prevIndent != prevIndentLine:
            widget.insert("insert", "\n")
            widget.mark_set("insert", "insert + 1 line")
 
            while widget.compare(prevIndent, ">", prevIndentLine):
                widget.insert("insert", "     ")
                widget.mark_set("insert", "insert + 5 chars")
                prevIndentLine += "+5c"
            return "break"
 
    def getIndex(self, index):
        while True:
            if self.T1.get(index) == " ":
                index = "%s+%sc" % (index, 1)
            else:
                return self.T1.index(index)
                
    def update(self,code_index):
        self.stackify()
        for start_index,end_index in code_index:
            self.tagHighlight(start_index,end_index)
            self.scan(start_index,end_index)
   
    def stackify(self):
        self.stack.append(self.T1.get("1.0", "end - 1c"))
        if self.stackcursor < 9: self.stackcursor += 1
 
    def insert_code(self ,text_box , part):
        text_box.insert("end", part , 'gray_background')
        