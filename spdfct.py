#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import pdwarf as pd
import os, sys
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter import filedialog
#Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
from tkinter.messagebox import *
#from tkinter import filedialog  #.askopenfilename()
#from tkinter import simpledialog  #.askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('PDwarF-GUI v1.0')
        self.master.geometry('469x497')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('TFrame1.TLabelframe', font=('宋体',9))
        self.style.configure('TFrame1.TLabelframe.Label', font=('宋体',9))
        self.Frame1 = LabelFrame(self.top, text='Source PDF', style='TFrame1.TLabelframe')
        self.Frame1.place(relx=0.017, rely=0.016, relwidth=0.923, relheight=0.163)

        self.style.configure('TFrame2.TLabelframe', font=('宋体',9))
        self.style.configure('TFrame2.TLabelframe.Label', font=('宋体',9))
        self.Frame2 = LabelFrame(self.top, text='Output Path', style='TFrame2.TLabelframe')
        self.Frame2.place(relx=0.017, rely=0.209, relwidth=0.923, relheight=0.163)

        self.style.configure('TFrame3.TLabelframe', font=('宋体',9))
        self.style.configure('TFrame3.TLabelframe.Label', font=('宋体',9))
        self.Frame3 = LabelFrame(self.top, text='Quality', style='TFrame3.TLabelframe')
        self.Frame3.place(relx=0.017, rely=0.386, relwidth=0.923, relheight=0.292)

        self.style.configure('TFrame4.TLabelframe', font=('宋体',9))
        self.style.configure('TFrame4.TLabelframe.Label', font=('宋体',9))
        self.Frame4 = LabelFrame(self.top, text='Progress', style='TFrame4.TLabelframe')
        self.Frame4.place(relx=0.017, rely=0.708, relwidth=0.923, relheight=0.163)

        self.Label3Var = StringVar(value='LJNT.XYZ')
        self.style.configure('TLabel3.TLabel', anchor='w', font=('宋体',9))
        self.Label3 = Label(self.top, text='LJNT.XYZ', textvariable=self.Label3Var, style='TLabel3.TLabel')
        self.Label3.setText = lambda x: self.Label3Var.set(x)
        self.Label3.text = lambda : self.Label3Var.get()
        self.Label3.place(relx=0.034, rely=0.918, relwidth=0.36, relheight=0.034)

        self.Command1Var = StringVar(value='Start')
        self.style.configure('TCommand1.TButton', font=('宋体',9))
        self.Command1 = Button(self.top, text='Start', textvariable=self.Command1Var, command=self.Command1_Cmd, style='TCommand1.TButton')
        self.Command1.setText = lambda x: self.Command1Var.set(x)
        self.Command1.text = lambda : self.Command1Var.get()
        self.Command1.place(relx=0.58, rely=0.901, relwidth=0.19, relheight=0.05)

        self.Command2Var = StringVar(value='Force Stop')
        self.style.configure('TCommand2.TButton', font=('宋体',9))
        self.Command2 = Button(self.top, text='Force Stop', textvariable=self.Command2Var, command=self.Command2_Cmd, style='TCommand2.TButton')
        self.Command2.setText = lambda x: self.Command2Var.set(x)
        self.Command2.text = lambda : self.Command2Var.get()
        self.Command2.place(relx=0.785, rely=0.901, relwidth=0.19, relheight=0.05)

        self.Command3Var = StringVar(value='Exit')
        self.style.configure('TCommand3.TButton', font=('宋体',9))
        self.Command3 = Button(self.top, text='Exit', textvariable=self.Command3Var, command=self.Command3_Cmd, style='TCommand3.TButton')
        self.Command3.setText = lambda x: self.Command3Var.set(x)
        self.Command3.text = lambda : self.Command3Var.get()
        self.Command3.place(relx=0.392, rely=0.901, relwidth=0.173, relheight=0.05)

        self.Frame3RadioVar = StringVar()
        self.style.configure('TOption5.TRadiobutton', font=('宋体',9))
        self.Option5 = Radiobutton(self.Frame3, text='Level 5', value='Option5', variable=self.Frame3RadioVar, command=self.Option5_Cmd, style='TOption5.TRadiobutton')
        self.Option5.setValue = lambda x: self.Frame3RadioVar.set('Option5' if x else '')
        self.Option5.value = lambda : 1 if self.Frame3RadioVar.get() == 'Option5' else 0
        self.Option5.place(relx=0.037, rely=0.828, relwidth=0.816, relheight=0.117)
        """
        self.Label1Var = StringVar(value='File Choose')
        self.style.configure('TLabel1.TLabel', anchor='w', font=('宋体',9))
        self.Label1 = Label(self.Frame1, text='File Choose', textvariable=self.Label1Var, style='TLabel1.TLabel')
        self.Label1.setText = lambda x: self.Label1Var.set(x)
        self.Label1.text = lambda : self.Label1Var.get()
        self.Label1.place(relx=0.037, rely=0.296, relwidth=0.409, relheight=0.506)
        """
        self.Command4Var = StringVar(value='Select File')
        self.style.configure('TCommand4.TButton', font=('宋体',9))
        self.Command4 = Button(self.Frame1, text='Select File', textvariable=self.Command4Var, command=self.Command4_Cmd, style='TCommand4.TButton')
        self.Command4.setText = lambda x: self.Command4Var.set(x)
        self.Command4.text = lambda : self.Command4Var.get()
        self.Command4.place(relx=0.037, rely=0.296, relwidth=0.335, relheight=0.506)

        self.Command5Var = StringVar(value='Select Output')
        self.style.configure('TCommand5.TButton', font=('宋体',9))
        self.Command5 = Button(self.Frame2, text='Select Output', textvariable=self.Command5Var, command=self.Command5_Cmd, style='TCommand5.TButton')
        self.Command5.setText = lambda x: self.Command5Var.set(x)
        self.Command5.text = lambda : self.Command5Var.get()
        self.Command5.place(relx=0.037, rely=0.296, relwidth=0.335, relheight=0.506)
        """
        self.Frame3RadioVar = StringVar()
        self.style.configure('TLabel2.TLabel', anchor='w', font=('宋体',9))
        self.Label2 = Label(self.Frame4, text='TQDM', textvariable=self.Label2Var, style='TLabel2.TLabel')
        self.Label2.setText = lambda x: self.Label2Var.set(x)
        self.Label2.text = lambda : self.Label2Var.get()
        self.Label2.place(relx=0.037, rely=0.395, relwidth=0.889, relheight=0.407)
        self.Label2.bind('<Button-1>', self.Label2_Button_1)
        """
        self.progress = Progressbar(self.Frame4, orient="horizontal", length=400, mode="determinate")
        self.progress.pack()
        self.progress["value"] = 0
        self.progress["maximum"] = 100




        self.style.configure('TOption1.TRadiobutton', font=('宋体',9))
        self.Option1 = Radiobutton(self.Frame3, text='Level 1', value='Option1', variable=self.Frame3RadioVar, command=self.Option1_Cmd, style='TOption1.TRadiobutton')
        self.Option1.setValue = lambda x: self.Frame3RadioVar.set('Option1' if x else '')
        self.Option1.value = lambda : 1 if self.Frame3RadioVar.get() == 'Option1' else 0
        self.Option1.place(relx=0.037, rely=0.166, relwidth=0.816, relheight=0.117)

        self.style.configure('TOption2.TRadiobutton', font=('宋体',9))
        self.Option2 = Radiobutton(self.Frame3, text='Level 2', value='Option2', variable=self.Frame3RadioVar, command=self.Option2_Cmd, style='TOption2.TRadiobutton')
        self.Option2.setValue = lambda x: self.Frame3RadioVar.set('Option2' if x else '')
        self.Option2.value = lambda : 1 if self.Frame3RadioVar.get() == 'Option2' else 0
        self.Option2.place(relx=0.037, rely=0.331, relwidth=0.816, relheight=0.117)

        self.style.configure('TOption3.TRadiobutton', font=('宋体',9))
        self.Option3 = Radiobutton(self.Frame3, text='Level 3', value='Option3', variable=self.Frame3RadioVar, command=self.Option3_Cmd, style='TOption3.TRadiobutton')
        self.Option3.setValue = lambda x: self.Frame3RadioVar.set('Option3' if x else '')
        self.Option3.value = lambda : 1 if self.Frame3RadioVar.get() == 'Option3' else 0
        self.Option3.place(relx=0.037, rely=0.497, relwidth=0.816, relheight=0.117)

        self.style.configure('TOption4.TRadiobutton', font=('宋体',9))
        self.Option4 = Radiobutton(self.Frame3, text='Level 4', value='Option4', variable=self.Frame3RadioVar, command=self.Option4_Cmd, style='TOption4.TRadiobutton')
        self.Option4.setValue = lambda x: self.Frame3RadioVar.set('Option4' if x else '')
        self.Option4.value = lambda : 1 if self.Frame3RadioVar.get() == 'Option4' else 0
        self.Option4.place(relx=0.037, rely=0.662, relwidth=0.816, relheight=0.117)



class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        super().__init__(master)

    def Command1_Cmd(self, event=None):
        print("Command1_Cmd")
        pass

    def Command2_Cmd(self, event=None):
        print("Command2_Cmd")
        pass

    def Command3_Cmd(self, event=None):
        print("Command3_Cmd")
        exit()
        pass

    def Option5_Cmd(self, event=None):
        print("Option5_Cmd")
        level = 5

    def Label2_Button_1(self, event=None):
        print("Label2_Button_1")
        pass

    def Option3_Cmd(self, event=None):
        print("Option3_Cmd")
        level = 3

    def Label4_Button_1(self, event=None):
        print("Label4_Button_1")
        pass
    def Option4_Cmd(self, event=None):
        level = 4
        pass
    def Option2_Cmd(self, event=None):
        level = 2
        pass
    def Option1_Cmd(self, event=None):
        level = 1
        pass
    def Command4_Cmd(self, event=None):
        print("Command4_Cmd")
        sourcePath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    def Command5_Cmd(self, event=None):
        SavePath = filedialog.asksaveasfilename(filetypes=[("PDF files", "*.pdf")])
        print("Command5_Cmd")
if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()

