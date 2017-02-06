#This file contains the color configuration for the syntax


import tkinter

def configuration(text):
	text.tag_config("Token.Keyword", foreground="lawn green")
	text.tag_config("Token.Keyword.Constant", foreground="lawn green")
	text.tag_config("Token.Keyword.Reserved", foreground="lawn green")
	text.tag_config("Token.Keyword.Namespace", foreground="lawn green")
	text.tag_config("Token.Keyword.Declaration",foreground="lawn green")
	text.tag_config("Token.Keyword.Type", foreground="cyan")
	text.tag_config("Token.Name.Builtin", foreground="lawn green")
	text.tag_config("Token.Name.Builtin.Pseudo",foreground="medium purple")
	text.tag_config("Token.Literal.Number.Integer",foreground="medium purple")
	text.tag_config("Token.Literal.String",foreground="light goldenrod")
	text.tag_config("Token.Literal.String.Double",foreground="light goldenrod")
	text.tag_config("Token.Literal.String.Single",foreground="light goldenrod")

#	text.tag_config("Token.Operator", foreground="hot pink")
	text.tag_config("Token.Operator.Word", foreground="hot pink")
	
	text.tag_config("Token.Comment", foreground="grey")
	text.tag_config("Token.Comment.Single", foreground="grey")
	text.tag_config("Token.Comment.Multiline", foreground="grey")