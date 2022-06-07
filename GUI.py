import tkinter as tk
from tkinter import filedialog as fd 
from os import listdir #import walk instead if files and dirs are important
from os.path import isfile, join
import xml.etree.ElementTree as ET
#from Methods import *

window = tk.Tk()
window.title('Metadata Tool')
preview = tk.Text()
fieldName = tk.Entry()
fieldDefault = tk.Entry()
fieldNameLabel = tk.Label(text='Field to add')
fieldDefaultLabel = tk.Label(text='Default value')

preview.insert('1.0', 'Start by selecting a folder containing the files to be uploaded')
preview.pack()

noOfFiles = 0


"""
Finds the index before the end of the line to determine where to insert new characters

Iterates through the given line, character by character until it finds a '\n' character,
then returns the index of the character before it

Parameters:

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

"""
Adds a new field to the preview

Adds a field name to the top line and the default value to subsequent lines. All lines after the first are checked to find
the end of the line, allowing the default value to be inserted in the correct place.
"""
def addField():
    field = fieldName.get()
    default = fieldDefault.get()
    fieldName.delete(0, tk.END)
    fieldDefault.delete(0, tk.END)
    insertIndex = getEnd(1)
    locationToInsert = '1.' + str(insertIndex)
    preview.insert(locationToInsert, ', ATTRIBUTE_'+field)
    #Adds the default value to the end of each line except the first
    for each_line in range(noOfFiles):
        lineNo = each_line + 2 #One to account for the line with the field names, one to account for the fact that lines are not zero-indexed
        insertIndex = getEnd(lineNo)
        preview.insert(str(lineNo) + '.' + str(insertIndex), ', ' + default)
        
"""
Adds all files in a folder to a directory

Uses tkinter fileDialog for the user to specify a directory. All files in this directory are collated into a list, which is then
iteratively added to each line.
"""
def addFiles():
    global noOfFiles
    #Gets the files to add to the preview
    directoryToAdd = fd.askdirectory()
    filesToAdd = [file for file in listdir(directoryToAdd) if isfile(join(directoryToAdd, file))]
    #Adds the files to the preview under the filename column
    preview.delete('1.0', tk.END)
    preview.insert('1.0', 'filename\n')
    lineNo=2
    for eachFile in filesToAdd:
        index = str(lineNo) + '.0'
        preview.insert(index, eachFile + '\n')
        lineNo += 1
        noOfFiles += 1
    
    fieldBtn['state']=tk.NORMAL
    submitBtn['state']=tk.NORMAL
    filesBtn['state']=tk.DISABLED
    importBtn['state']=tk.NORMAL


def submit():
    path = fd.asksaveasfilename(defaultextension=".txt", filetypes=(("text file", "*.txt"),))
    #Ensures a valid path has been selected, and that the user hasn't clicked cancel
    if path != '':
        #Ensures the file is saved as a .txt, rather than anything else
        if path.find('.') != -1:
            path = path[0:path.find('.')]
            path += '.txt'
            
        fileContents = preview.get('1.0', tk.END)
        preview.delete('1.0', tk.END)
        fileContents = fileContents.replace(',', '\t')
        writeFile = open(path, 'w')
        writeFile.write(fileContents)
        writeFile.close()


"""
Reads in an xml file and adds the fields it contains to the preview

User selects a file, which is then parsed to get two lists containing the names
and default values of each field. These two lists are then iterated through to
add all the fields to the preview in the same manner as addFiles()
"""
def importConfig():
    #User selects config file
    configPath = fd.askopenfilename()
    #Config file is read
    tree = ET.parse(configPath)
    root=tree.getroot()
    names = []
    for name in root.iter('name'):
        names.append(name.text)

    values = []
    for value in root.iter('default'):
        values.append(value.text)
        
    #Preview is updated according to config file
    for each_field in range(len(names)):
        field = names[each_field]
        default = values[each_field]
        insertIndex = getEnd(1)
        locationToInsert = '1.' + str(insertIndex)
        preview.insert(locationToInsert, ', ATTRIBUTE_' + field)
        #Adds the default value to the end of each line except the first
        for each_line in range(noOfFiles):
            lineNo = each_line + 2 #One to account for the line with the field names, one to account for the fact that lines are not zero-indexed
            insertIndex = getEnd(lineNo)
            preview.insert(str(lineNo) + '.' + str(insertIndex), ', ' + default)


filesBtn = tk.Button(
    text = 'Select Folder',
    command=addFiles
    )

filesBtn.pack()

fieldBtn = tk.Button(
    text = 'Add field',
    command = addField,
    state = 'disabled'
    )

submitBtn = tk.Button(
    text = 'Submit',
    command = submit,
    state = 'disabled'
    )

importBtn = tk.Button(
    text = 'Import config',
    command = importConfig,
    state = 'disabled'
    )

fieldBtn.pack()
fieldNameLabel.pack()
fieldName.pack()
fieldDefaultLabel.pack()
fieldDefault.pack()
importBtn.pack()
submitBtn.pack()

window.mainloop()
