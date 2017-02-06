#contains the code for the indentation of the text

import tkinter
import re

class Indent:

	def __init__(self,text,syntax):
		self.text=text
		self.syntax=syntax
		self.text.bind("<Return>",self.enter)
		self.text.bind("<braceright>",self.braceright)
		self.text.bind("<braceleft>",self.braceleft)
		self.text.bind("<parenright>",self.parenright)
		self.text.bind("<parenleft>",self.parenleft)
		self.text.bind("<bracketright>",self.bracketright)
		self.text.bind("<bracketleft>",self.bracketleft)
		self.text.bind("<BackSpace>",self.backspace)
		self.text.bind("<quotedbl>",self.quotedbl)
		self.text.bind("<quoteright>",self.singlequote)

	def count_tabs(self,line):
		count=0
		for ch in line:
			if ch=='\t':
				count=count+1
			else:
				break
		return count

	#checks whether the line contains the a keyword after which indentation is needed
	def check_expr(self,line):
		if self.syntax=='py':
			pattern=re.compile(r'^[\s]*(for)|(while)|(if)|(elif)|(else)|(def)|(class)')
		else:
			pattern=re.compile(r'^[\s]*(for)|(while)|(if)|(else if)|(else)')
		result=pattern.search(line)
		if result is None:
			return False
		return True

	def singlequote(self,event):
		prev_char=self.text.get('insert'+'-1c','insert')
		next_char=self.text.get('insert','insert'+'+1c')
		self.text.insert('insert',"'")
		if (prev_char.isspace() or not prev_char) and next_char.isspace():
			temp=self.text.index('insert')
			self.text.insert('insert',"'")
			self.text.mark_set('insert',temp)
		return 'break'

	def quotedbl(self,event):
		prev_char=self.text.get('insert'+'-1c','insert')
		next_char=self.text.get('insert','insert'+'+1c')
		self.text.insert('insert','"')
		if (prev_char.isspace() or not prev_char) and next_char.isspace():
			temp=self.text.index('insert')
			self.text.insert('insert','"')
			self.text.mark_set('insert',temp)
		return 'break'


	def parenright(self,event):
		next_char=self.text.get('insert','insert'+'+1c')
		if next_char==')':
			self.text.mark_set('insert','insert'+'+1c')
			return 'break'	

	def parenleft(self,event):
		self.text.insert('insert',"(")
		next_char=self.text.get('insert','insert'+'+1c')
		if next_char.isspace() or next_char==')':
			temp=self.text.index('insert')
			self.text.insert('insert',')')
			self.text.mark_set('insert',temp)
		return 'break'

	def bracketright(self,event):
		next_char=self.text.get('insert','insert'+'+1c')
		if next_char==']':
			self.text.mark_set('insert','insert'+'+1c')
			return 'break'

	def bracketleft(self,event):
		self.text.insert('insert',"[")
		next_char=self.text.get('insert','insert'+'+1c')
		if next_char.isspace() or next_char==']':
			temp=self.text.index('insert')
			self.text.insert('insert',']')
			self.text.mark_set('insert',temp)
		return 'break'	

	def braceright(self,event):
		next_char=self.text.get('insert','insert'+'+1c')
		if next_char=='}':
			self.text.mark_set('insert','insert'+'+1c')
			return 'break'
		curr_line=self.text.get('insert linestart','insert')
		prev_line=self.text.get('insert'+'-1 lines'+' linestart','insert'+'-1 lines'+' lineend')
		prev_line.rstrip()
		if (self.count_tabs(curr_line)-self.count_tabs(prev_line)==1) and prev_line[-1]=='{':
			self.text.delete('insert linestart')
		elif self.count_tabs(curr_line)==self.count_tabs(prev_line):
			self.text.delete('insert linestart')

	def braceleft(self,event):
		next_char=self.text.get('insert','insert'+'+1c')
		if next_char.isspace() or next_char=='}':
			curr_line=self.text.get('insert linestart','insert lineend')
			prev_line=self.text.get('insert'+'-1 lines'+' linestart','insert'+'-1lines'+' lineend')
			prev_line.rstrip()
			if self.check_expr(prev_line) and prev_line[-1]!=';':
				if (self.count_tabs(curr_line)-self.count_tabs(prev_line)==1):
					self.text.mark_set('insert','insert linestart')
					self.text.insert('insert',"\t"*self.count_tabs(prev_line))
					self.text.insert('insert','{')
			else:
				self.text.insert('insert','{')
			temp=self.text.index('insert')
			self.text.insert('insert','}')
			self.text.mark_set('insert',temp)
		else:
			self.text.insert('insert','{')
		return 'break'

	def enter(self,event):
		self.text.insert('insert','\n')
		idx=self.text.index('insert')
		line=int(idx.split('.')[0])-1
		start="%d.0" % (line)
		end="%d.end" % (line)
		line=self.text.get(start,end)
		count=self.count_tabs(line)
		prev_char=self.text.get('insert'+'-2c','insert'+'-1c')
		next_char=self.text.get('insert','insert'+'+1c')
		self.text.insert("insert",'\t'*count)	
		if prev_char=='{' and next_char=='}':
			self.text.insert('insert',"\t")
			temp=self.text.index('insert')
			self.text.insert('insert',"\n")
			self.text.insert('insert',"\t"*count)
			self.text.mark_set('insert',temp)
		elif prev_char=='{':
			self.text.insert('insert',"\t")
		elif self.check_expr(line) and line[-1]!=';' and self.syntax!='py':
			self.text.insert('insert',"\t")	
		elif self.check_expr(line) and line[-1]!=':' and self.syntax=='py':
			self.text.insert('insert',"\t")
		return 'break'

	def backspace(self,event):
		prev_char=self.text.get('insert'+'-1c','insert')
		next_char=self.text.get('insert','insert'+'+1c')
		if prev_char=='{' and next_char=="}":
			self.text.delete('insert')
		elif prev_char=='[' and next_char==']':
			self.text.delete('insert')
		elif prev_char=='(' and next_char==')':
			self.text.delete('insert')