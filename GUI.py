import tkinter as tk
from tkinter import filedialog as fd 
from os import listdir #import walk instead if files and dirs are important
from os.path import isfile, join
#from Methods import *

window = tk.Tk()
preview = tk.Text()
fieldName = tk.Entry()

preview.insert('1.0', 'Start by selecting a folder containing the files to be uploaded')

preview.pack()


"""
Finds the index before the end of the line to determine where to insert new characters

Iterates through the given line, character by character until it finds a '\n' character,
then returns the index of the character before it

Paranmeters:

    line: Line in the text box to find the index with

Returns:

    index: Index to insert characters into
"""
def getEnd(line):
    completed = False
    char = 0
    current = str(line) + '.' + str(char)
    #Iterates through the line to find the eol character
    while completed == False:
        if preview.get(current) == '\n':
            completed == True
            return char
        else:
            char += 1
            current = str(line) + '.' + str(char)

"""
Returns the number of lines currently in the preview

Counts the number of EOL characters to determine how many lines there are. If the text doesn't end with an EOL character,
that means the user has added another line by themselves without an EOL character, so another line is counted.

Returns:

    lines: No of lines in the text
"""
def getLineNo():
    text = preview.get('1.0', tk.END)
    lines = text.count('\n')
    #Accounts for the possibility that the user has added a line in the preview that doesn't have an EOL character at the end
    if text[-1] != '\n':
        lines += 1
    
    return lines


def addField():
    field = fieldName.get()
    insert = getEnd(1)


def addFiles():
    #Gets the files to add to the preview
    directoryToAdd = fd.askdirectory()
    filesToAdd = [file for file in listdir(directoryToAdd) if isfile(join(directoryToAdd, file))]
    #Adds the files to the preview under the filename column
    preview.delete('1.0', tk.END)
    preview.insert('1.0', 'filename \n')
    lineNo=2
    for eachFile in filesToAdd:
        index = str(lineNo) + '.0'
        preview.insert(index, eachFile)
        lineNo += 1


filesBtn = tk.Button(
    text = 'Select Folder',
    command=addFiles
    )

filesBtn.pack()

fieldBtn = tk.Button(
    text = 'Add field',
    command = getLineNo
    )

fieldBtn.pack()
            

window.mainloop()
