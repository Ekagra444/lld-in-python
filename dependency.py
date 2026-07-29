# The weakest relationship.
# Object merely uses another.
# Doesn't store it.
class Printer:
    def printText(self, txt:str):
        print(txt)
class Editor:
    def __init__(self):
        pass
    def takeInput(self,txt:str):
        self.txt = txt 
    def printUserInput(self,printer:"Printer"):
        printer.printText(self.txt)
OfficePrinter = Printer()
Notepad = Editor()
Notepad.takeInput("hi there printing this text...")
Notepad.printUserInput(OfficePrinter)
        

