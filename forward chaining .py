class Fait:
  def __init__(self,key, operande , value):
    self.key = key
    self.operande = operande
    self.value = value
  def __str__(self):
      return(self.key+self.operande+self.value)
  def __repr__(self):
    return self.__str__()
  def __eq__(self,fait):
        if fait is None: return False
        return (self.key==fait.key and self.value==fait.value and self.operande==fait.operande)
class Regle:
  def __init__(self,premise,conclusion,number):
    self.premise = premise
    self.conclusion = conclusion
    self.number = number
  

   
import re
import sys
# importing tkinter and tkinter.ttk 
# and all their functions and classes 
from tkinter import *
from tkinter.ttk import *

# importing askopenfile function 
# from class filedialog 


def getAppliableRules(Rules,Facts,rulestate):
   regles_applicables=[] 
   factDicts={}
   for f in Facts:
       factDicts[f.key]=f    
   for r in Rules:
       i=0
       acceptedPremise=True 
       while i< len(r.premise) :
           acceptedPremise=False
           x=factDicts.get(r.premise[i].key)
           if x != None :
               if r.premise[i].operande == "=" :
                   if str(x) == str(r.premise[i]) :
                       acceptedPremise=True
               else:
                   acceptedPremise= eval(x.value+r.premise[i].operande+r.premise[i].value)
           else:
               break;
           i=i+1
           if acceptedPremise == False :
               break
       if acceptedPremise :
           if rulestate[r.number] == 0 :
               regles_applicables.append(r)
           
   return sorted(regles_applicables,key=lambda x: x.number)

def notFait(fait):
    if fait.operande == "=":
        if fait.value=="Vrai":
            operande="="
            value="Faux"
        elif fait.value=="Faux":
            operande="="
            value="Vrai"
        else:
            value=fait.value
            operande="!="
    elif fait.operande == "!=":
        if fait.value=="Vrai":
            operande="="
            value="Vrai"
        elif fait.value=="Faux":
            operande="="
            value="Faux"
        else:
            value=fait.value
            operande="="
    elif fait.operande==">":
        value=fait.value
        operande="<="
    elif fait.operande=="<":
        value=fait.value
        operande=">="
    elif fait.operande==">=":
        value=fait.value
        operande="<"
    elif fait.operande=="<=":
        value=fait.value
        operande=">"
    return Fait(fait.key,operande,value)

def ReadFile(fileHandler=None) :
    
    test=False
    Rules=[]
    Facts=[]
    if fileHandler == None :
        fileHandler =  open (r"C:\Users\pc\Desktop\TP AI\méteorologies.txt")
    else:
        fileHandler = open(fileHandler,"r")

    j=0;
    while True:
        line = fileHandler.readline()
        if not line :
            break;
        if line.strip()=="":
            test=True
        try:
            if test==False :
                pattern = re.compile("((?P<parm6>(((\w+)+\s){1,}))(?P<parm9>(=|<|>|<=|>=|!=|==))((?P<parm8>(\s((\w|[1-9]|-|\")+)){1,})))")
                match= pattern.match(line.strip());
                Facts.append(Fait(match.group("parm6"),match.group("parm9"),match.group("parm8"))) 
               
    
            else:
               if line.strip()!="" :
                   alors=line.strip().split("alors")
                   si=alors[0].split("si ");
                   premises=re.split("\set|&\s",si[1])
                   conclusion=alors[1].split("=")
                   premise=[]
                   for e in premises :
                       pattern = re.compile("(^\s?(?P<parm6>((((\w+)+\s)){1,}))(?P<parm9>(=|<|>|<=|>=|!=|==))((?P<parm8>(\s((\w|[1-9]|-|\")+)){1,})))")
                       match= pattern.match(e);
                       premise.append(Fait(match.group("parm6"),match.group("parm9"),match.group("parm8")))
    
                      
                   pattern = re.compile("(^\s?(?P<parm6>((((\w+)+\s)){1,}))(?P<parm9>(=|<|>|<=|>=|!=|==))((?P<parm8>(\s((\w|[1-9]|-|\")+)){1,})))")
                   match= pattern.match(alors[1]);
                   Rules.append(Regle(premise,Fait(match.group("parm6"),match.group("parm9"),match.group("parm8")),j));
                   j=j+1
                  
            
        except :
                match = None
        
    
    return (Rules, Facts)
    
        
    
       



def chainage_avant_avec_conflit(Rules,Facts,but=None):
    FactsPorcess = []
    appliedRuleProcess = []
    rulestate=[0 for i in Rules]
    bfchanged=True
    trace=[]
    butatteint=False
    buta=""
    while bfchanged==True :
        regles_applicables=getAppliableRules(Rules,Facts,rulestate)
        
        if but in Facts :
            buta=" \n le but existe dans la base de fait"
            trace=[]
            break
        if len(regles_applicables) == 0:
            bfchanged=False
        for appliedRule in regles_applicables:
            rulestate[appliedRule.number]=1
            if appliedRule.conclusion in Facts :
                bfchanged=False
            else:
                print(appliedRule.number)
                appliedRuleProcess.append(appliedRule.number)
                trace.append(appliedRule.number)
                bfchanged=True
                if notFait(appliedRule.conclusion) in Facts:
                    sys.exit('§LOGIC ERROR§')
                else:
                    Facts.append(appliedRule.conclusion)
                    FactsPorcess.append(appliedRule.conclusion)
                    print(Facts)
            if appliedRule.conclusion == but:
                bfchanged=False
                butatteint=True
                buta =" \n but EST atteint"
                break
            if but != None and butatteint==False :
                buta =" \n but non atteint"
                trace=[]
    print("*********trace***********")
    return buta,trace,Facts,FactsPorcess,appliedRuleProcess

from tkinter import * 
from tkinter import filedialog
import os

class FileImport:
    def __init__(self,parent,title):
        self.parent = parent
        self.title= title
        self.filePath = StringVar() 
        self.filePathInput = Entry(self.parent, textvariable=self.filePath, width=30, state="readonly")
        self.filePathInput.pack()
        self.browseBtn = Button(self.parent, text="open", command=self.browseFile)
        self.browseBtn.pack()
        self.path = ""

    def getParent(self):
        return self.parent

    def getFilePathString(self):
        return self.filePath.get()
    
    def browseFile(self):
        my_filetypes = [('all files', '.*'), ('text files', '.txt')]
        self.filePath.set(
            filedialog.askopenfilenames(parent=self.parent,
                                            initialdir=os.getcwd(),
                                            title=self.title,
                                            filetypes=my_filetypes)
                                            )
        self.path=self.getFilePathString().split('(')[1].split(',')[0];
        
       

class Frame:
    def __init__(self,parent,title,rowV,columnV):
        self.parent = parent
        self.title = title
        self.frame = LabelFrame(self.parent, text=self.title, padx=10, pady=10)
        self.frame.grid(row = rowV, column = columnV, pady = 2,columnspan = 2) 
    
    def getElement(self):
        return self.frame

class Input:
    def __init__(self,parent,initValue,state):
        self.state = state
        self.parent = parent
        self.content = StringVar()
        self.content.set(initValue)
        self.input = Entry(self.parent, textvariable=self.content, width=30, state=self.state)
        self.input.pack()
    
    def setState(self,state):
        self.input.config(state = state)
        return
    def getElement(self):
        return self.input

class RadioList:
    def __init__(self,parent,initValue,modes,inputElement):
        self.MODES = modes
        self.parent = parent
        self.choice = StringVar()
        self.choice.set(initValue)
        self.inputElement = inputElement
        self.randerRadioMenu()

    def showChoice(self):
        choice = int(self.choice.get())
        if(choice==1):
            self.inputElement.getElement().config(state=DISABLED)
        else:
            self.inputElement.getElement().config(state=NORMAL) 

    def randerRadioMenu(self):
        for text, mode in self.MODES:
            r = Radiobutton(self.parent, text=text,
                            variable=self.choice, value=mode, command=self.showChoice)
            r.pack(anchor=W)

window = Tk()
fileImport1 = FileImport(Frame(window,"Bases des connaissance",0,0).getElement(),"Select file")
#fileImport2 = FileImport(Frame(window,"Bases des regles",1,0).getElement() ,"Select file")
goalInput = Input(Frame(window,"But",2,0).getElement(),'',DISABLED) 

radioList = RadioList(
    Frame(window,"Mode",3,0).getElement(),
    "1",
    [
        ("Saturer la base", "1"),
        ("s'arreter si le but est atteint", "2"),
    ],
    goalInput
)


tlog = Text(window,wrap = "word")
tlog.grid(row = 0, column = 2, columnspan = 2, rowspan = 4, padx = 5, pady = 5)

def execute():
    
    FileHandler = fileImport1.path.replace("'",'')
    Rules , Facts = ReadFile(FileHandler)
    but =None 
    #print(re.split("(=|<|>|<=|>=|!=|==)",goalInput.content.get())[0])
    pattern = re.compile("((?P<parm6>(((\w+)+\s){1,}))(?P<parm9>(=|<|>|<=|>=|!=|==))((?P<parm8>(\s((\w|[1-9]|-|\")+)){1,})))")
    if goalInput.content.get() != "" :
        match= pattern.match(goalInput.content.get());
        but = Fait(match.group("parm6"),match.group("parm9"),match.group("parm8"))
    #but = Fait (re.split("(=|<|>|<=|>=|!=|==)",goalInput.content.get())[0],"=",re.split("(=|<|>|<=|>=|!=|==)",goalInput.content.get())[2])
    print (Facts[2])
    print(but)
    buta,trace,Facts,FactsPorcess,appliedRuleProcess  = chainage_avant_avec_conflit(Rules,Facts,but)
    tlog.insert(END,"******Trace******** \n")
    
    tlog.insert(END,str(trace)+"\n")
    tlog.insert(END,buta)
    
def ShowAndSave():
    filelog = open ("Log.txt","a+")
    FileHandler = fileImport1.path.replace("'",'')
    Rules , Facts = ReadFile(FileHandler)
    but =None 
    #print(re.split("(=|<|>|<=|>=|!=|==)",goalInput.content.get())[0])
    pattern = re.compile("((?P<parm6>(((\w+)+\s){1,}))(?P<parm9>(=|<|>|<=|>=|!=|==))((?P<parm8>(\s((\w|[1-9]|-|\")+)){1,})))")
    if goalInput.content.get() != "" :
        match= pattern.match(goalInput.content.get());
        but = Fait(match.group("parm6"),match.group("parm9"),match.group("parm8"))
    #but = Fait (re.split("(=|<|>|<=|>=|!=|==)",goalInput.content.get())[0],"=",re.split("(=|<|>|<=|>=|!=|==)",goalInput.content.get())[2])
    print (Facts[2])
    print(but)
    buta,trace,Facts2,FactsPorcess,appliedRuleProcess = chainage_avant_avec_conflit(Rules,Facts,but)
    for i in range(len(FactsPorcess)):
        tlog.insert(END," +++++++++The Applied Rule is number++++++  \n" + str(appliedRuleProcess[i]) +"\n" )
        filelog.write(" +++++++++The Applied Rule is number++++++  \n" + str(appliedRuleProcess[i]) +"\n" )
        tlog.insert(END," *********The Added Fact is **************  \n" +  str(FactsPorcess[i]) +"\n")
        filelog.write(" *********The Added Fact is **************  \n" +  str(FactsPorcess[i]) +"\n")
    filelog.flush()
    filelog.write("\n \n \n")
    tlog.insert(END,"\n")
    tlog.insert(END,"\n")
    tlog.insert(END,"\n")
    filelog.write("---------FINAL FACTS ------------ \n")
    tlog.insert(END,"---------FINAL FACTS ------------ \n")
    print("looooooooooooooo")
    print(Facts2)
    tlog.insert(END,str(Facts2))
    tlog.insert(END,buta)
    filelog.write(str(Facts2))
    filelog.write(buta)
    filelog.close()
    
def FactFunc():
    
    FileHandler = fileImport1.path.replace("'",'')
    Rules , Facts = ReadFile(FileHandler)
    tlog.insert(END,"......... facts ........ \n")
    tlog.insert(END,str(Facts))
def RuleFunc():
    
    FileHandler = fileImport1.path.replace("'",'')
    Rules , Facts = ReadFile(FileHandler)
    tlog.insert(END,"........ Rules ........ \n")
    for e in Rules:
        tlog.insert(END,"premise :  ")
        tlog.insert(END,e.premise)
        tlog.insert(END,"\n")
        tlog.insert(END,"\n")
        tlog.insert(END,"conclusion :  ")
        tlog.insert(END,e.conclusion)
        tlog.insert(END,"\n")
        tlog.insert(END,"\n")
def ClearTolg():
    
    
    tlog.delete('1.0', END)
    
    

save = Button(window, text="Delete", command=ClearTolg)
save.grid(row = 4, column = 0, pady = 2) 
save = Button(window, text="Rules", command=RuleFunc)
save.grid(row = 4, column = 2, pady = 2) 
save = Button(window, text="Facts", command=FactFunc)
save.grid(row = 4, column = 3, pady = 1) 
save = Button(window, text="Show Process Details & SAVE", command=ShowAndSave)
save.grid(row = 4, column = 4, pady = 1) 
save = Button(window, text="execute", command=execute)
save.grid(row = 4, column = 1, pady = 2) 

window.mainloop()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    