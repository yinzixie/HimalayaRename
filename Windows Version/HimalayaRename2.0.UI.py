#!/user/bin/python
# -*- coding: utf-8 -*-
import json
import re
import os

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory,askopenfilenames
import tkinter.messagebox
import ctypes

#隐藏控制台
whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)

version = "HimalayaRename2.0.UI" 
author = "------2018.12.31xyz"
updata_file = "HimalayaRename_UpdateLog.txt"
help_document = "Help_Document.txt"
on_process = False #处理中
illegal_Char = re.compile(r"[/\\:*?\"<>|]")
illegal_Charfor_path = re.compile(r"[*?\"<>|,]")

def selection():
    tkinter.messagebox.showinfo(title='Hi', message='hahahaha') 
    
def start_process():
   
    JsonFileNameList = jsonpath.get()        
    
    dirname = str(directory.get())
    dirname = dirname.replace("/","\\")
    dirname = re.sub(illegal_Charfor_path,"",dirname)  
    
    ext = str(extension.get())

    choose = int(choice.get())
    
    if(ext == "" or dirname == "" or JsonFileNameList == "" or choose == 0):
        if(JsonFileNameList == ""):
            tkinter.messagebox.showerror(title="Parameter error",message="请选择正确的Json文件!")
        if(dirname == ""):
            tkinter.messagebox.showerror(title="Parameter error",message="请选择正确的目录!")
        if(ext == ""):   
            tkinter.messagebox.showerror(title="Parameter error",message="请选择操作的文件类型!")
        if(choose == 0):   
            tkinter.messagebox.showerror(title="Parameter error",message="请选择操作类型!")    
    else:
        JsonFileName = re.split(r"[('*',)]",JsonFileNameList)[2]
        JsonFileName = JsonFileName.replace("/","\\")
        JsonFileName = re.sub(illegal_Charfor_path,"",JsonFileName)
        
        subwindow = tk.Tk()
        subwindow.title("Processing")
        subwindow.geometry('1000x300')
        yscrolly = tk.Scrollbar(subwindow)
        yscrolly.pack(side=tk.RIGHT, fill=tk.Y)
        xscrolly = tk.Scrollbar(subwindow,orient='horizontal')
        xscrolly.pack(side=tk.BOTTOM, fill=tk.X)
        
        processlist = tk.Listbox(subwindow,yscrollcommand=yscrolly.set,xscrollcommand=xscrolly.set,width=500,height=280)
        processlist.pack()
        
        #有这个命令移动bar才能有功能
        yscrolly.config(command=processlist.yview)
        xscrolly.config(command=processlist.xview)                
        
        try:    
                Fjson = open(JsonFileName,"r",encoding = "utf-8")
        except OSError as err:
                tkinter.messagebox.showerror(title="OS error",message=format(err))
        else:    
                load_list = json.load(Fjson)
                
                #close file
                Fjson.close()
                                        
                try:
                    os.chdir(dirname)
                except OSError as err:
                    tkinter.messagebox.showerror(title="OS error",message=format(err))
                else:    
                    #rename
                    for i in range(len(load_list)):
                        try:
                            oldname = str(load_list[i]["id"]) + ext
                            newname = str(load_list[i]["title"]) + ext
                        
                            newname = re.sub(illegal_Char,"",newname)
                        except:
                            tkinter.messagebox.showerror(title="OS error",message="错误的Json文件!")
                            break
                        else:    
                            #avoid same filename clash
                            try:
                                if (choose == 1):                                                                            
                                    
                                    if(os.path.isfile(newname)):
                                        newname = str(load_list[i]["title"]) + str(load_list[i]["id"]) + ".m4a"
                                        newname = re.sub(illegal_Char,"",newname)
                                        
                                        #print('\033[1;31;40m')
                                        listattention = "ATTENTION!发现重名文件：尝试强制更改，更改后此文件将无法使用自动复原进行恢复"
                                        processlist.insert(tk.END,listattention)
                                        #print('\033[0m')
                                        try:
                                            os.rename(oldname,newname)
                                        except OSError as err:
                                            listerror = "OS error: {0}".format(err)
                                            processlist.insert(tk.END,listerror)
                                        else:
                                           listprocess = "强制更改完成:"+oldname+"-->"+newname
                                           processlist.insert(tk.END,listprocess) 
                                    else:
                                            os.rename(oldname, newname)
                                        
                                else:
                                    os.rename(newname, oldname)
                            except OSError as err:
                                listerror = "OS error: {0}".format(err)
                                processlist.insert(tk.END,listerror)                            
                                
                            else:
                                if(choose == 1):                           
                                    listprocess = oldname+"--->"+newname
                                else:
                                    listprocess = newname+"--->"+oldname
                                    
                                processlist.insert(tk.END,listprocess)
                            
        listprocess = "!!!!!!!!!!!!!!!!!!!!!!!!!Finshed!!!!!!!!!!!!!!!!!!!!!!!!!"
        processlist.insert(tk.END,listprocess)
        
                 
def selectjsonPath():
    path_ = askopenfilenames()
    jsonpath.set(path_)
    
def selectdirectory():
    path_ = askdirectory()
    directory.set(path_) 

    
def show_helpinformation():
    helpwindow = tk.Tk()
    helpwindow.title("Help Information")
    helpwindow.geometry('600x210')
    try:    
        helpwindow.iconbitmap('help.ico')
    except:
        pass
    yscrolly = tk.Scrollbar(helpwindow)
    yscrolly.pack(side=tk.RIGHT, fill=tk.Y)
    xscrolly = tk.Scrollbar(helpwindow,orient='horizontal')
    xscrolly.pack(side=tk.BOTTOM, fill=tk.X)
     
    text1 = tk.Text(helpwindow,yscrollcommand=yscrolly.set,xscrollcommand=xscrolly.set)    
    text1.pack()
    yscrolly.config(command=text1.yview)
    xscrolly.config(command=text1.xview)
    try:
        with open(help_document) as f:
            for each_line in f:
                text1.insert(tk.INSERT,each_line)

        text1.config(state=tk.DISABLED)    
        
    except OSError as reason:
        text1.insert(tk.INSERT,"帮助信息丢失！")
        text1.config(state=tk.DISABLED)
    
def show_version():
    versionwindow = tk.Tk()
    versionwindow.title("Version Information")
    versionwindow.geometry('600x210')
    try:    
        versionwindow.iconbitmap('Logo_FX.ico')
    except:
        pass
    
    label = tk.Label(versionwindow,text = "当前版本："+version)
    label.pack()
    
    yscrolly = ttk.Scrollbar(versionwindow)
    yscrolly.pack(side=tk.RIGHT, fill=tk.Y)
    xscrolly = ttk.Scrollbar(versionwindow,orient='horizontal')
    xscrolly.pack(side=tk.BOTTOM, fill=tk.X)
    
    text1 = tk.Text(versionwindow,yscrollcommand=yscrolly.set,xscrollcommand=xscrolly.set)    
    text1.pack()
    yscrolly.config(command=text1.yview)
    xscrolly.config(command=text1.xview)
    try:
        with open(updata_file) as f:
            for each_line in f:
                text1.insert(tk.INSERT,each_line)
        text1.insert(tk.INSERT,"\n\n")
        text1.insert(tk.INSERT,author)        
        text1.config(state=tk.DISABLED)    
        
    except OSError as reason:
        text1.insert(tk.INSERT,"版本信息丢失！")
        text1.insert(tk.INSERT,"\n\n")
        text1.insert(tk.INSERT,author)
        text1.config(state=tk.DISABLED)

mainwindow = tk.Tk()
mainwindow.title(version)

#禁用拉伸
mainwindow.resizable(width = False, height = False)

#得到屏幕长宽
sw = mainwindow.winfo_screenwidth()
sh = mainwindow.winfo_screenheight()
#UI长宽
ww = 380
wh = 185
#偏移量
x = (sw-ww) / 2
y = (sh-wh) / 2
#设置UI大小以及处于屏幕的位置
mainwindow.geometry("%dx%d+%d+%d" %(ww,wh,x,y))

#设置窗口图标
try:
    mainwindow.iconbitmap('1.ico')
except:
    pass
        
jsonpath = tk.StringVar()
directory = tk.StringVar()
choice = tk.IntVar()
extension = tk.StringVar()

choice.set(1)
#菜单
menubar = tk.Menu(mainwindow)
#空菜单单元
helpmenu = tk.Menu(menubar,tearoff = 0)
versionmenu = tk.Menu(menubar,tearoff = 0)

menubar.add_cascade(label = "Version",menu = versionmenu)
menubar.add_cascade(label = "Help",menu = helpmenu)
#menubar.add_command(label='Exit', command= exit())

##在`File`中加入`New`的小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
##如果点击这些单元, 就会触发`do_job`的功能
versionmenu.add_command(label='Version Information', command=show_version)
helpmenu.add_command(label='Help Document', command=show_helpinformation)

menubar.add_separator()
mainwindow.config(menu = menubar)

ttk.Label(mainwindow,text = "Json文件路径:").grid(row = 0, column = 0)
jsonfilepath = tk.Entry(mainwindow, textvariable = jsonpath).grid(row = 0, column = 1)
ttk.Button(mainwindow, text = "路径选择", command = selectjsonPath).grid(row = 0, column = 2)

ttk.Label(mainwindow,text = "目录路径:").grid(row = 1, column = 0)
dirpath = tk.Entry(mainwindow, textvariable = directory).grid(row = 1, column = 1)
ttk.Button(mainwindow, text = "目录选择", command = selectdirectory).grid(row = 1, column = 2)

operationfram = ttk.Frame(mainwindow).grid(row = 2)

ttk.Label(operationfram,text = "选择操作:").grid(row = 2, column = 0)

radiobutton1 = ttk.Radiobutton(operationfram,
                             text='Rename',
                             variable=choice, 
                             value=1)
radiobutton1.grid(row=2, column=1, padx=10, pady=10)

radiobutton2 = ttk.Radiobutton(operationfram,
                             text='Revocation',
                             variable=choice, 
                             value=2).grid(row=2, column=2, padx=10, pady=10)

extensionfram = ttk.Frame(mainwindow).grid(row = 3)

ttk.Label(extensionfram,text = "选择操作的文件类型:").grid(row = 3, column = 0)

extbox = tk.StringVar()
extbox = ttk.Combobox(mainwindow, textvariable=extension)
extbox['values'] = ('.m4a', '.mp3','.wma','.wav','.ape','.flac','.aac','.ac3','.mmf','.amr','.m4r','.ogg','.wavpack','.mp2')
extbox.grid(column=1, row=3,columnspan=2)
extbox.current(0)  #设置初始显示值，值为元组['values']的下标

'''
exbutton1 = tk.Radiobutton(extensionfram,
                             text='m4a',
                             variable=extension, 
                             value='.m4a').grid(row=3, column=1, padx=10, pady=10)
 
exbutton2 = tk.Radiobutton(extensionfram,
                             text='mp3',
                             variable=extension, 
                             value='.mp3').grid(row=3, column=2, padx=10, pady=10)
'''
button = ttk.Button(mainwindow,
              text = "Start",
              width = 10,
              command = start_process).grid(row=5, column=1, padx=10, pady=10)

mainwindow.mainloop()    