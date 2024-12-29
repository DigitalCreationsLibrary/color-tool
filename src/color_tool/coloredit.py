import tkinter as tk
from tkinter import INSERT, END
import re

def rgbToHex(r,g,b):
    colorVal = "#{0:02x}{1:02x}{2:02x}".format(r, g, b).upper()
    return colorVal

def hexToRgb(hex):
    h = hex.lstrip('#')
    colorVal= tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return colorVal


class ColorFrame(tk.Frame):
    def __init__(self, master=None, colorValue=((243,233,220),"#F3E9DC"),width=200,height=150):
        tk.Frame.__init__(self,master,bg=colorValue[1],width=width,height=height)
        self.color = colorValue
        
    def updateTheColor(self,colorValue):
        self.color = colorValue
        self.config(bg=self.color[1])

class StateEntry(tk.Entry):
        def __init__(self, master=None,typeC=1,rank=0):
            tk.Entry.__init__(self, master, bg="#ffffff",font=("Arial",12),width=12,)
            self.state=1
            self.rank=rank
            self.typeC=typeC
            self.stateColors = ["#BE5674","#ffffff"]
            self.bind('<FocusOut>',lambda e,ind=self.rank: self.master.updateColorValues(ind))
            self.delete(0,END)
            self.insert(END, self.master.values[rank])
            self.updateState(self.state)
        
        def updateState(self,state):
                self.state = state
                self.config(bg=self.stateColors[self.state])
                
        def validColors(self):
            correct=1
            if self.typeC:

                hexa_code = re.compile(r'^#([a-fA-F0-9]{6})$')
                
                correct = bool(re.match(hexa_code, self.get()))
                
            else:      
                rgb_code = re.compile(r'^[0-9]+$')                
                correct = bool(re.match(rgb_code, self.get()))  
                if correct:        
                    correct = int(self.get())>0 and int(self.get())<256
            self.updateState(correct)
            return correct
        
        def setColor(self,color):
            self.delete(0,END)
            self.insert(0,color)
            


class EditFrame(tk.Frame):
    def __init__(self, master=None, labels=["The Label"],values=["#F3E9DC"],typeC=1):
        tk.Frame.__init__(self, master, bg="#01295F")
        self.master = master
        self.numEdits=len(labels)
        self.edits=[]
        self.labels=labels
        self.values=values
        self.labelsW=[]
        self.typeC = typeC
        self.editState=1
        self.widgets()

  
    def updateColorValues(self,i):
            stateEdit = self.edits[i]
            self.values[i]= stateEdit.get()
            correct= self.master.updateOverallState()
            if correct:
                self.master.updateColor(self.typeC)
    
    def setEditColors(self,colorValues):
        self.values= colorValues
        for i in self.edits:
            i.setColor(self.values[i.rank])
        

    def widgets(self):
        for i in range(self.numEdits):
            aText = StateEntry(self,self.typeC,i)
            aLabel = tk.Label(self)
            aLabel.config(text=self.labels[i],fg="#F3E9DC", bg="#01295F",font=("Arial",12,'bold'))
            aLabel.grid(row=i, column=0, padx=10, pady=10,sticky="nw") 
            aText.grid(row=i, column=1, padx=10, pady=10,sticky='ne') 
            self.edits.append(aText)
            self.labelsW.append(aLabel)
            
    def updateEditState(self):
        correct =1
        for i in self.edits:
            correct = correct and i.validColors()
        self.editState = correct
        return correct
        
          
    
class ColorEditor(tk.Frame):
    def __init__(self, master=None,width=500,height=180,colorValue=((243,233,220),"#F3E9DC")):
        tk.Frame.__init__(self, master, bg="#D282A6",width=width,height=height)
        # self.grid_propagate(0)
        self.master = master
        self.colorValue = colorValue
        self.theColor = ColorFrame(self,self.colorValue)
        self.theColor.grid(row=0,column=0,padx=10,pady=20,rowspan=2)
        self.overallState=1
        self.widgets()
        
    def updateColor(self,typeC):
        rgbValues = tuple([int(col) for col in self.rgbEdits.values])
        hexValue = self.hexEdits.values[0]

        r,g,b = self.rgbEdits.values
        if typeC:
            rgbValues = hexToRgb(hexValue)
            self.rgbEdits.setEditColors(list(rgbValues))
            
        else:
            hexValue = rgbToHex(int(r),int(g),int(b))
            self.hexEdits.setEditColors([hexValue])

        self.colorValue = tuple([rgbValues,hexValue])
        self.theColor.updateTheColor(self.colorValue)
        
    def widgets(self):
        rgbLabels= ["Red","Green","Blue"]
        rgbValues=[self.colorValue[0][i] for i in range(3)]
        self.rgbEdits = EditFrame(self,rgbLabels,rgbValues,0)
        self.rgbEdits.grid(row=0, column=1, padx=5, pady=5,sticky='ne') 
        hexLabels= ["Hex"]
        hexValues=[self.colorValue[1]]
        self.hexEdits = EditFrame(self,hexLabels,hexValues,1)
        self.hexEdits.grid(row=1, column=1, padx=5, pady=5,sticky='nwse') 
        
    def updateOverallState(self):
        state1= self.rgbEdits.updateEditState()
        state2= self.hexEdits.updateEditState()
        self.overallState = state1 and state2
        return self.overallState
    

class MainW(tk.Tk):
    
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        # self.geometry("530x220+400+100")
        self.config(bg="#F3E9DC")
        self.parent = parent
        self.mainWidgets()

    def mainWidgets(self):
        self.theEditor = ColorEditor(self)
        self.theEditor.grid(row=0, column=0,padx=10,pady=20)

if __name__=="__main__":
    app = MainW(None)
    app.mainloop()        