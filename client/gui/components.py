import tkinter as tk
from tkinter import ttk

def create_button(parent, text, command, **kwargs):
    return tk.Button(parent, text=text, command=command, **kwargs)

def create_label(parent, text=None, **kwargs):
    return tk.Label(parent, text=text, **kwargs)

def create_option_menu(parent, variable, options):
    return tk.OptionMenu(parent, variable, *options)

def create_treeview(parent, columns):
    tree = ttk.Treeview(parent, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    return tree