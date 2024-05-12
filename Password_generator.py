#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random  # random module generate random values
from tkinter import *  # Importing all required modules from tkinter library
from tkinter import messagebox  # messagebox module from tkinter is used for showing messages
import pyperclip  # pyperclip module copy generated password to clipboard

# Creating tkinter window
gui = Tk()
gui.title('Password Generator')
gui.geometry('250x200')
gui.resizable(0, 0)

# Define colors
bg_color = '#0077cc'  # Dark blue
fg_color = '#ffffff'  # White


# Function to generate password
def process():
    length = int(string_pass.get())  # Getting the password length from user input

    # Defining character sets for password generation
    lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    special = ['@', '#', '$', '%', '&', '*']
    all = lower + upper + num + special

    # Generating random password using selected characters
    ran = random.sample(all, length)
    password = "".join(ran)

    # Displaying generated password in a message box and copying it to clipboard
    messagebox.showinfo('Result', 'Your password {} \n\nPassword copied to clipboard'.format(password))
    pyperclip.copy(password)

# Creating a string variable to hold the password length entered by user
string_pass = StringVar()

# Adding background color to tkinter window 
gui.configure(bg=bg_color)

# Creating label and entry field for password length input
label = Label(gui, text="Password Length", bg=bg_color, fg=fg_color).pack(pady=10)
txt = Entry(gui, textvariable=string_pass).pack()

# Creating button to trigger password generation process
btn = Button(gui, text="Generate", command=process, bg=bg_color, fg=fg_color).pack(pady=10)

# Running the tkinter event loop
gui.mainloop()


# In[ ]:




