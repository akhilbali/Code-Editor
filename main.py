# sudo apt-get install python3-tk
import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.font
from pygments import lex
import pygments.lexers
from pad import Pad
from indent import Indent 

def newfile(event=None):
	pad=Pad(root)
	pad.text.bind('<KeyRelease>',keyreleased)
	tabs.add(pad.frame,text=pad.name.ljust(25))
	padlist.append(pad) 
	if len(padlist)==1:
		enable_menus()
		enable_shortcut()
	tabs.select(len(padlist)-1)

def openfile(event=None):
	file=tkinter.filedialog.askopenfile(mode='r')
	if file!=None:
		pad=Pad(root)
		contents=file.read()
		pad.text.bind('<KeyRelease>',keyreleased)
		pad.text.insert('1.0',contents)
		file.close()
		pad.filepath=file.name
		pad.name=(file.name.split('/'))[-1]
		pad.lexer=pygments.lexers.get_lexer_by_name((pad.name.split('.'))[-1])
		tabs.add(pad.frame,text=pad.name.ljust(25))
		padlist.append(pad)
		if len(padlist)==1:
			enable_menus()
			enable_shortcut()
		tabs.select(len(padlist)-1)
		pad.highlight()
		pad.update_linenumbers()
		Indent(pad.text,pad.name.split('.')[-1])

def savefile(event=None):
	pad=padlist[tabs.index("current")]
	pad.savefile()
	tabs.tab(tabs.index("current"), text=pad.name.ljust(25))

def saveasfile():
	pad=padlist[tabs.index("current")]
	pad.saveasfile()
	tabs.tab(tabs.index("current"), text=pad.name.ljust(25))

def closefile(event=None):
	tab_id=tabs.index("current")
	tabs.forget(tab_id)
	padlist.remove(padlist[tab_id])
	if len(padlist)==0:
		disable_menus()
		disable_shortcut()

def closeAll():
	num_of_tabs=tabs.index("end")
	for i in range(num_of_tabs-1,-1,-1):
		tabs.forget(i)
		padlist.remove(padlist[i])
	disable_menus()
	disable_shortcut()

def editfile(command,event=None):
	try:
		padlist[tabs.index("current")].edit(command)
	except:
		pass

def selectAll(event=None):
	padlist[tabs.index("current")].selectAll()

def increasefontsize(event=None):
	padlist[tabs.index("current")].inc_size()

def decreasefontsize(event=None):
	padlist[tabs.index("current")].dec_size()

def togglelinenumbers():
	label=viewmenu.entrycget(0,'label')
	num_of_tabs=tabs.index('end')
	if label=="Hide Line numbers":
		viewmenu.entryconfig(0,label="Display Line numebrs")
		padlist[tabs.index("current")].hide_line_numbers()
	else:
		viewmenu.entryconfig(0,label="Hide Line numbers")
		padlist[tabs.index("current")].show_line_numbers()

def enable_menus():
	filemenu.entryconfig(2,state=tkinter.ACTIVE)
	filemenu.entryconfig(3,state=tkinter.ACTIVE)
	filemenu.entryconfig(5,state=tkinter.ACTIVE)
	filemenu.entryconfig(6,state=tkinter.ACTIVE)
	editmenu.entryconfig(6,state=tkinter.ACTIVE)
	viewmenu.entryconfig(1,state=tkinter.ACTIVE)

def enable_shortcut():
	root.bind("<Control-s>",savefile)
	root.bind("<Control-w>",closefile)
	root.bind("<Control-a>",selectAll)
	root.bind("<Control-equal>",increasefontsize)
	root.bind("<Control-minus>",decreasefontsize)

def disable_menus():
	filemenu.entryconfig(2,state=tkinter.DISABLED)
	filemenu.entryconfig(3,state=tkinter.DISABLED)
	filemenu.entryconfig(5,state=tkinter.DISABLED)
	filemenu.entryconfig(6,state=tkinter.DISABLED)
	editmenu.entryconfig(6,state=tkinter.DISABLED)
	viewmenu.entryconfig(1,state=tkinter.DISABLED)

def disable_shortcut():
	root.unbind("<Control-s>")
	root.unbind("<Control-w>")
	root.unbind("<Control-a>")
	root.unbind("<Control-equal>")
	root.unbind("<Control-minus>")	

def keyreleased(event):
	try:
		padlist[tabs.index("current")].highlight()
		padlist[tabs.index("current")].update_linenumbers()
	except:
		pass
	
def closeApplication(event):
	root.destroy()

def shortcuts(root):
	root.bind("<Control-n>",newfile)
	root.bind("<Control-o>",openfile)	
	root.bind("<Control-q>",closeApplication)
	root.bind("<Control-z>",lambda e: editfile("Undo"))
	root.bind("<Control-r>",lambda e: editfile("Redo"))

root=tkinter.Tk()
tabs=tkinter.ttk.Notebook(root,height=500,width=700)
padlist=[]

menubar=tkinter.Menu(root)

filemenu=tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="New".ljust(20), command=newfile,accelerator="Ctrl+N")
filemenu.add_command(label="Open", command=openfile,accelerator="Ctrl+O")
filemenu.add_command(label="Save", command=savefile,accelerator="Ctrl+S",state=tkinter.DISABLED)
filemenu.add_command(label="SaveAs", command=saveasfile,state=tkinter.DISABLED)
filemenu.add_separator()
filemenu.add_command(label="Close File", command=closefile,accelerator="Ctrl+W",state=tkinter.DISABLED)
filemenu.add_command(label="Close All files",command=closeAll,state=tkinter.DISABLED)
filemenu.add_separator()
filemenu.add_command(label="Quit",command=root.destroy,accelerator="Ctrl+Q") 
menubar.add_cascade(label="File ", menu=filemenu)

editmenu=tkinter.Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo".ljust(15), command=lambda: editfile("Undo"),accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", command=lambda: editfile("Redo"),accelerator="Ctrl+R")
editmenu.add_separator()
editmenu.add_command(label="Copy", command=lambda: editfile("Copy"),accelerator="Ctrl+C")
editmenu.add_command(label="Cut", command=lambda: editfile("Cut"),accelerator="Ctrl+X")
editmenu.add_command(label="Paste", command=lambda: editfile("Paste"),accelerator="Ctrl+V")
editmenu.add_command(label="Select All",command=selectAll,accelerator="Ctrl+A",state=tkinter.DISABLED)
menubar.add_cascade(label="Edit", menu=editmenu)

viewmenu=tkinter.Menu(menubar, tearoff=0)
fontsize=tkinter.Menu(viewmenu, tearoff=0)
viewmenu.add_command(label="Hide line numbers",command=togglelinenumbers)
fontsize.add_command(label="Larger", command=increasefontsize,accelerator="Ctrl+=")
fontsize.add_command(label="Smaller", command=decreasefontsize,accelerator="Ctrl+-")
viewmenu.add_cascade(label="Font Size",menu=fontsize,state=tkinter.DISABLED)
menubar.add_cascade(label="View ", menu=viewmenu)

shortcuts(root)
root.config(menu=menubar)
tabs.pack(fill=tkinter.BOTH,expand=True)
root.title("Code Editor")
root.mainloop()