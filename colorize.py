import re
from tkinter import *
from collections import deque
 
 
class Text_highlighter:
    def __init__(self , Text):
        self.text = Text
        self.text.tag_config("orange", foreground = "orange")
        self.text.tag_config("blue", foreground = "blue")
        self.text.tag_config("purple", foreground = "purple")
        self.text.tag_config("green", foreground = "green")
        self.text.tag_config("red", foreground = "red")

        self.text.tag_config('you', foreground='blue' , background = 'yellow' ,
                                bgstipple = 'gray25',)
        
        self.text.tag_config('gpt', foreground='green' , background = 'gray',
                                )

        self.text.tag_config("gray_background", background = "#454242")

 
        self.tags = ["blue", "orange", "purple", "red" , "green"]

        
 
        self.wordlist = [ ["class", "def", "for", "if", "else","num" ,"or", "elif","import", "from", "as", "break", "while"],
                          ["int", "string", "float", "bool",'or' , "__init__" ,"print", "return", "del", "True", "False"],
                          ["pygame", "tkinter", "sys", "os", "mysql" ,],
                          ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0" ,"="]]
 

        #---------
 
    def tagHighlight(self):
        start = "0.0"
        end = "end"
         
        for mylist in self.wordlist:
            num = int(self.wordlist.index(mylist))
 
            for word in mylist:
                self.text.mark_set("matchStart", start)
                self.text.mark_set("matchEnd", start)
                self.text.mark_set("SearchLimit", end)
 
                mycount = IntVar()
                 
                while True:
                    index= self.text.search(word,"matchEnd","SearchLimit", count=mycount, regexp = True)
 
                    if index == "": break
                    if mycount.get() == 0: break
 
                    self.text.mark_set("matchStart", index)
                    self.text.mark_set("matchEnd", f"{index}+{mycount.get()}c")
 
                    preIndex = "%s-%sc" % (index, 1)
                    postIndex = "%s+%sc" % (index, mycount.get())
                     
                    if self.check(index, preIndex, postIndex):
                        self.text.tag_add(self.tags[num], "matchStart", "matchEnd")
                         
    def check(self, index, pre, post):
        letters = [chr(ord('a') + i) for i in range(26)]

        if self.text.get(pre) == self.text.get(index):
            pre = index
        elif self.text.get(pre) in letters:
            return 0

        if self.text.get(post) in letters:
            return 0

        return 1
    
    def scan(self):
        start = "0.0"
        end = "end"
        my_count = IntVar()
    # patterns to search '' brackets and # coments
        regex_patterns = [r'\".*?\"',r'\'.*?\'', r'#.']
    
        for pattern in regex_patterns:
            self.text.mark_set("start_mark", start)
            self.text.mark_set("end_mark", end)
    
            num = regex_patterns.index(pattern)
    
            while True:
                index = self.text.search(pattern, "start_mark", "end_mark", count=my_count, regexp=True)
    
                if index == "":
                    break
                    
                if num == 2:
                    self.text.tag_add(self.tags[4], index, index + " lineend")
                elif num == 0 or num == 1:
                    self.text.tag_add(self.tags[3], index, f"{index}+{my_count.get()}c")

                self.text.mark_set("start_mark", f"{index}+{my_count.get()}c")
 
 
    def getIndex(self, index):
        while True:
            if self.text.get(index) == " ":
                index = "%s+%sc" % (index, 1)
            else:
                return self.text.index(index)
                
    def update(self):
        self.tagHighlight()
        self.scan()
   
 
        