from utility import *
from pygments import lex
import pygments.lexers
from indent import Indent 


class Pad:

	def __init__(self,root):
		self.frame=tkinter.Frame(root)
		self.fontsize=13
		self.text=tkinter.Text(self.frame,cursor="arrow",undo=True)
		self.name="Untitled"
		self.filepath="Untitled"
		self.content=""
		self.linecount=0
		self.lexer=None
		self.linenumbers=tkinter.Text(self.frame,cursor="arrow")
		self.yscroll=tkinter.Scrollbar(self.frame)
		self.xscroll=tkinter.Scrollbar(self.frame,orient=tkinter.HORIZONTAL)
		self.pack_widgets()
		self.text.focus_force()
		self.update_linenumbers()

	def pack_widgets(self):
		self.set_scroll_options()
		self.set_options_text()
		self.set_options_linenumbers()
		self.yscroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)
		self.xscroll.pack(side=tkinter.BOTTOM,fill=tkinter.X)
		self.linenumbers.pack(side=tkinter.LEFT,fill=tkinter.Y)
		self.text.pack(expand=True,fill=tkinter.BOTH)	

	def set_scrollbar(self,first,last,type=None):
		self.text.yview_moveto(first)
		self.linenumbers.yview_moveto(first)
		self.yscroll.set(first,last)

	def scroll_both(self, *args):
		self.text.yview(*args)
		self.linenumbers.yview(*args)	

	def set_scroll_options(self):
		self.xscroll['command']=self.text.xview_moveto
		self.yscroll['command']=self.scroll_both

	def set_options_text(self):
		font=tkinter.font.Font(family='Consolas',size=self.fontsize)
		self.text['font']=font 							
		self.text['fg']='#fff'							#color of the text
		self.text['bg']='#444444'						#color of the background
		self.text['insertbackground']='#fff'			#color of the insertion cursor
		self.text['tabs']='1.125c'						#width of the tab
		self.text['highlightthickness']=0				#highlight thickness of the border of widget
		self.text['bd']=0								#borderwidth
		self.text['yscrollcommand']=self.set_scrollbar
		self.text['xscrollcommand']=self.xscroll.set

	def set_options_linenumbers(self):
		self.linenumbers['width']=4
		font=tkinter.font.Font(family='Consolas',size=self.fontsize)
		self.linenumbers['font']=font 
		self.linenumbers['fg']='#fff'
		self.linenumbers['bg']='#444444'
		self.linenumbers['highlightthickness']=0
		self.linenumbers['bd']=0
		self.linenumbers['state']=tkinter.DISABLED 			#inactive state of the widget
		self.linenumbers['yscrollcommand']=self.set_scrollbar

	def hide_line_numbers(self):
		self.linenumbers.pack_forget()

	def show_line_numbers(self):
		self.text.pack_forget()
		self.linenumbers.pack(side=tkinter.LEFT,fill=tkinter.Y)
		self.text.pack(expand=True,fill=tkinter.BOTH)

	def saveasfile(self):
		file=tkinter.filedialog.asksaveasfile(mode='w')
		if file!=None:
			contents=self.text.get('1.0',"end"+'-1c')
			file.write(contents)
			file.close()
			self.filepath=file.name
			self.name=(file.name.split('/'))[-1]
			self.lexer=pygments.lexers.get_lexer_by_name((self.name.split('.'))[-1])
			Indent(self.text,self.name.split('.')[-1])

	def savefile(self):
		if self.filepath!="Untitled":
			file=open(self.filepath,'w')
			contents=self.text.get('1.0','end'+'-1c')
			file.write(contents)
			file.close()
		else:
			self.saveasfile()

	def edit(self,command):
		self.text.event_generate("<<"+command+">>")
		self.update_linenumbers()
		self.highlight() 

	def selectAll(self):
		self.text.tag_add("sel",'1.0','end'+'-1c')

	def inc_size(self):
		self.fontsize=self.fontsize+2
		self.text.config(font=tkinter.font.Font(size=self.fontsize))
		self.linenumbers.config(font=tkinter.font.Font(size=self.fontsize))

	def dec_size(self):
		self.fontsize=self.fontsize-2
		self.text.config(font=tkinter.font.Font(size=self.fontsize))
		self.linenumbers.config(font=tkinter.font.Font(size=self.fontsize))

	def update_linenumbers(self):
		last_idx=self.text.index('end')
		num=int(last_idx.split('.')[0])
		if num!=self.linecount:
			position = self.yscroll.get()
			self.linenumbers['state']=tkinter.NORMAL
			self.linenumbers.delete('1.0','end')
			self.linenumbers['width']=len(str(num-1))+1
			for i in range(1,num-1):
				self.linenumbers.insert('insert',str(i)+" ")
				self.linenumbers.insert('insert','\n')
			self.linenumbers.insert('insert',str(num-1)+" ")
			self.linenumbers.tag_add('justify','1.0','end')
			self.linenumbers.tag_config('justify',justify=tkinter.RIGHT)
			self.linenumbers['state']=tkinter.DISABLED
			self.linecount=num
			self.set_scrollbar(position[0],position[1])

	def highlight(self):
		if self.lexer!=None:
			code = self.text.get('1.0','end'+'-1c')
			if code!=self.content:
				taglist=self.text.tag_names()
				for tag in taglist:
					if tag!="sel":
						self.text.tag_remove(tag,'1.0','end')
				self.text.mark_set("range_start",'1.0')
				for token,content in lex(code,self.lexer):
					configuration(self.text)
					print(str(token))
					self.text.mark_set("range_end","range_start + %dc" %len(content))
					self.text.tag_add(str(token),"range_start","range_end")
					self.text.mark_set("range_start","range_end")
				self.content=code