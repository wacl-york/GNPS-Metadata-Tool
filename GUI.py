import tkinter as tk
from tkinter import filedialog as fd
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import yaml

window = tk.Tk()
window.geometry('1700x700')
window.title('Metadata Tool')

window.columnconfigure(0, weight=1, minsize=200)
window.columnconfigure(1, weight=0, minsize=400)

for r in range(2):
    window.rowconfigure(r, weight=1, minsize=50)

lower_frame = tk.Frame(
    master = window
    )

side_frame = tk.Frame(
    master=window
    )

preview_frame = tk.Frame(
    master=window
    )

scroll = tk.Scrollbar(master = preview_frame, orient='horizontal')
scroll.grid(row=1, column=0, sticky='EW')#pack(side=tk.BOTTOM, fill='x')
preview = tk.Text(master = preview_frame, wrap=tk.NONE, xscrollcommand=scroll.set)
fieldName = tk.Entry(master=side_frame)
fieldDefault = tk.Entry(side_frame)
fieldNameLabel = tk.Label(text='Field to add', master=side_frame)
fieldDefaultLabel = tk.Label(text='Default value', master=side_frame)
instructionsLabel = tk.Label(text='Instructions for use: \n 1. Put all the files you wish to create metadata \n for into one folder, then select this folder \n 2. The files within this folder will appear in the preview. \n From here you can add fields by either \n importing a config file containing all \n the fields. Alternatively you can add fields \n individually by entering the name of the field  \n and optionally a default value \n 3. From here you can modify the values as necessary \n 4. Click the "Save as .txt" button to finalise the folder')
instructionsLabel.bind('<Configure>', lambda e: instructionsLabel.config(wraplength=instructionsLabel.winfo_width()))
preview.insert('1.0', 'Start by selecting a folder containing the files to be uploaded')
preview.grid(row=0, column=0)#ack(fill='both', expand=True)
scroll.config(command=preview.xview)
    
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
    for each_line in range(preview.get('1.0', tk.END).count('\n') - 2):
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
    noOfFiles = 0
    #Gets the files to add to the preview
    directoryToAdd = fd.askdirectory()
    if directoryToAdd != ():
        preview.grid_forget()
        filesToAdd = [file for file in listdir(directoryToAdd) if isfile(join(directoryToAdd, file))]
        grid = [[]]
        grid[0].append(tk.Entry(master = preview_frame))
        grid[0][0].insert(0, 'filename')
        grid[0][0].grid(row=0, column=0)
        row = 1
        for eachFile in filesToAdd:
            grid.append([])
            grid[row].append(tk.Entry(master = preview_frame))
            grid[row][0].insert(0, eachFile)
            grid[row][0].grid(row = row, column = 0)
            row += 1
        
        fieldBtn['state']=tk.NORMAL
        submitBtn['state']=tk.NORMAL
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
    configPath = fd.askopenfilename(filetypes=(("YAML file", "*.yaml"),))
    if configPath != '':
        #Config file is read
        with open(configPath) as f:
            data=yaml.load(f, Loader=yaml.FullLoader) 
    
        names = []
        values = []
        for each_field in data['fields']:
            if type(each_field['Name']) != str:
                names.append(str(each_field['Name']))
            else:
                names.append(each_field['Name'])

            if type(each_field['Default']) != str:
                values.append(str(each_field['Default']))
            else:
                values.append(each_field['Default'])
            
        #Preview is updated according to config file
        for each_field in range(len(names)):
            field = names[each_field]
            default = values[each_field]
            insertIndex = getEnd(1)
            locationToInsert = '1.' + str(insertIndex)
            preview.insert(locationToInsert, ', ATTRIBUTE_' + field)
            #Adds the default value to the end of each line except the first

            #There needs to be two less lines due to the lack of zero-indexing and the first line being irrelevant here
            for each_line in range(preview.get('1.0', tk.END).count('\n') - 2):
                lineNo = each_line + 2 #Similiarly, the working line is increased by two to ensure the first line is skipped
                insertIndex = getEnd(lineNo)
                preview.insert(str(lineNo) + '.' + str(insertIndex), ', ' + default)


filesBtn = tk.Button(
    text = 'Select Folder',
    command=addFiles,
    master = lower_frame
    )

fieldBtn = tk.Button(
    text = 'Add field',
    command = addField,
    state = 'disabled',
    master = side_frame
    )

submitBtn = tk.Button(
    text = 'Save as .txt',
    command = submit,
    state = 'disabled',
    master = lower_frame
    )

importBtn = tk.Button(
    text = 'Import config',
    command = importConfig,
    state = 'disabled',
    master = lower_frame
    )

preview_frame.grid(row=0, column=0, sticky='NESW')
lower_frame.grid(row=1, column=0)
side_frame.grid(row=0, column=1)

#lower frame
filesBtn.grid(row=0, column=0)
importBtn.grid(row=1, column=0)
submitBtn.grid(row=2, column=0)

#side frame
fieldNameLabel.grid(row=0, column=0)
fieldName.grid(row=1, column=0)
fieldDefaultLabel.grid(row=2, column=0)
fieldDefault.grid(row=3, column=0)
fieldBtn.grid(row=4, column=0)

instructionsLabel.grid(row=1, column=1)

window.mainloop()
