import tkinter as tk
from tkinter import filedialog as fd
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
from PIL import ImageTk, Image
import yaml
import csv

window = tk.Tk()
#window.configure(background='black')
window.geometry('1200x700')
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

toolbar_frame = tk.Frame(
    master = window
    )

logo_frame = tk.Frame(
    master=window,
    width=10,
    height=10
    )

grid_canvas = tk.Canvas(
    master = preview_frame,
    height = 200,
    width = 700
    )

entry_frame = tk.Frame(
    master = grid_canvas
    )

grid_canvas.create_window((0, 0), window=entry_frame, anchor='nw')

vscroll = tk.Scrollbar(master = preview_frame, orient = 'vertical', command = grid_canvas.yview)
hscroll = tk.Scrollbar(master = preview_frame, orient = 'horizontal', command = grid_canvas.xview)
preview = tk.Label(master = preview_frame, text = 'Select one of the buttons above to start creating a metadata file', anchor = 'nw')
fieldName = tk.Entry(master=side_frame)
fieldDefault = tk.Entry(side_frame)
fieldNameLabel = tk.Label(text='Field to add', master=side_frame)
fieldDefaultLabel = tk.Label(text='Default value', master=side_frame)
preview.grid(row=0, column=0)
#entry_frame.bind("<Configure>", grid_canvas.configure(scrollregion=grid_canvas.bbox("all")))

#Opens logo in a PIL format so it can be resized
logo = Image.open('wacl.png')
logo_resized = logo.resize((350, 250))
#Resized photo is used to create a new object tkinter will accept
logo_photo_image = ImageTk.PhotoImage(logo_resized)
logo_label = tk.Label(master = window, image = logo_photo_image)

noOfFiles = 0
grid = [[]]

def adjustScrollRegion():
    entry_frame.update_idletasks()
    
    if len(grid[0]) > 4:
        #Constant assigned from experience
        canvas_width = 700
    else:
        canvas_width = len((grid[0]) * grid[0][0].winfo_width())

    if len(grid) > 9:
        canvas_height = 200
    else:
        canvas_height = len(grid) * grid[0][0].winfo_height()
    
    grid_canvas.config(scrollregion=grid_canvas.bbox("all"), width = canvas_width, height = canvas_height)
    
    


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
Displays instructions for using the tool in a popup window

Upon clicking the "Help" button, a new window is created, inside of which is a label containing the instructions,
and a button, which will close the window when clicked.

"""
def showInstructions():
    popupWindow = tk.Tk()
    popupWindow.title('Instructions')
    label = tk.Label(popupWindow, text = 'Instructions for use: \n 1. Put all the files you wish to create metadata \n for into one folder, then select this folder \n 2. The files within this folder will appear in the preview. \n From here you can add fields by either \n importing a config file containing all \n the fields. Alternatively you can add fields \n individually by entering the name of the field  \n and optionally a default value \n 3. From here you can modify the values as necessary \n 4. Click the "Save as .txt" button to finalise the folder')
    label.pack()
    closeButton = tk.Button(popupWindow, text = 'Close', command = popupWindow.destroy)
    closeButton.pack()
    popupWindow.mainloop()


"""
Adds all files in a folder to a directory

Uses tkinter fileDialog for the user to specify a directory. All files in this directory are collated into a list, which is then
iteratively added to each line.
"""
def addFiles():
    global noOfFiles
    global grid
    noOfFiles = 0
    #Gets the files to add to the preview
    directoryToAdd = fd.askdirectory()
    #Checks that the directory provided is valid
    if len(directoryToAdd) > 1:
        grid = [[]]
        preview.grid_forget()
        filesToAdd = [file for file in listdir(directoryToAdd) if isfile(join(directoryToAdd, file))]
        grid[0].append(tk.Entry(master = entry_frame))
        grid[0][0].insert(0, 'filename')
        grid[0][0].grid(row=0, column=0)
        row = 1
        #Creates an Entry object in grid, which corresponds to it's position in the the preview,
        #which is then placed in the appropriate spot using the .grid method
        for eachFile in filesToAdd:
            grid.append([])
            grid[row].append(tk.Entry(master = entry_frame))
            grid[row][0].insert(0, eachFile)
            grid[row][0].grid(row = row, column = 0)
            row += 1
        
        fieldBtn['state']=tk.NORMAL
        submitBtn['state']=tk.NORMAL
        importBtn['state']=tk.NORMAL
        vscroll.grid(row=0, column=1, sticky = 'NS')
        hscroll.grid(row=1, column=0, sticky = 'EW')
        adjustScrollRegion()


def openFile():
    global grid
    filePath = fd.askopenfilename(filetypes=(("Metadata file", "*.txt"),))
    if filePath != '':
        preview.grid_forget()
        grid = []
        with open(filePath) as file:
            tsv_file = csv.reader(file, delimiter="\t")
            row_no = 0
            for line in tsv_file:
                grid.append([])
                field_no = 0
                for field in line:
                    grid[row_no].append(tk.Entry(master = entry_frame))
                    grid[row_no][field_no].insert(0, field)
                    grid[row_no][field_no].grid(row=row_no, column = field_no)
                    field_no += 1

                row_no += 1

        fieldBtn['state']=tk.NORMAL
        submitBtn['state']=tk.NORMAL
        importBtn['state']=tk.NORMAL
        vscroll.grid(row=0, column=1, sticky = 'NS')
        hscroll.grid(row=1, column=0, sticky = 'EW')
        adjustScrollRegion()



"""
Adds a new field to the grid

Appends a new entry containing the field name to the first line and the default value to subsequent lists.
These entries are then added to the preview frame using the grid method in the position corresponding to
it's location in the 2d list
"""
def addField():
    field = fieldName.get()
    default = fieldDefault.get()
    fieldName.delete(0, tk.END)
    fieldDefault.delete(0, tk.END)
    grid[0].append(tk.Entry(master = entry_frame))
    grid[0][-1].insert(0, 'ATTRIBUTE_'+field)
    grid[0][-1].grid(row=0, column = len(grid[0])-1)
    row_no = 1
    for each_line in range(len(grid)-1):
        grid[row_no].append(tk.Entry(master = entry_frame))
        grid[row_no][-1].insert(0, default)
        grid[row_no][-1].grid(row=row_no, column = len(grid[row_no]) - 1)
        row_no += 1

    adjustScrollRegion()


def submit():
    path = fd.asksaveasfilename(defaultextension=".txt", filetypes=(("text file", "*.txt"),))
    #Ensures a valid path has been selected, and that the user hasn't clicked cancel
    if path != '':
        #Ensures the file is saved as a .txt, rather than anything else
        if path.find('.') != -1:
            path = path[0:path.find('.')]
            path += '.txt'

            writeFile = open(path, 'w')
            for each_line in grid:
                new_line = True
                for each_field in each_line:
                    if new_line == True:
                        new_line = False
                        writeFile.write(each_field.get())
                    else:
                        writeFile.write('\t')
                        writeFile.write(each_field.get())

                writeFile.write('\n')

            writeFile.close()
            feedbackWindow = tk.Tk()
            feedbackWindow.title('File saved')
            label = tk.Label(feedbackWindow, text = 'File saved successfully')
            label.pack()
            closeButton = tk.Button(feedbackWindow, text = 'Close', command = feedbackWindow.destroy)
            closeButton.pack()
            feedbackWindow.mainloop()
                
                        
                
                    

        """
        fileContents = preview.get('1.0', tk.END)
        fileContents = fileContents.replace(',', '\t')
        writeFile = open(path, 'w')
        writeFile.write(fileContents)
        writeFile.close()
        """

"""
Reads in a yaml file and adds the fields it contains to the preview

User selects a file, which is then parsed to get two lists containing the names
and default values of each field. These two lists are then iterated through to
add all the fields to the grid in the same manner as addFiles()
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
            grid[0].append(tk.Entry(master = entry_frame))
            grid[0][-1].insert(0, 'ATTRIBUTE_'+field)
            grid[0][-1].grid(row=0, column = len(grid[0])-1)
            row_no = 1
            for each_line in range(len(grid)-1):
                grid[row_no].append(tk.Entry(master = entry_frame))
                grid[row_no][-1].insert(0, default)
                grid[row_no][-1].grid(row=row_no, column = len(grid[row_no]) - 1)
                row_no += 1

        adjustScrollRegion()
                
        """
        insertIndex = getEnd(1)
        locationToInsert = '1.' + str(insertIndex)
        preview.insert(locationToInsert, ', ATTRIBUTE_' + field)
        #Adds the default value to the end of each line except the first

        #There needs to be two less lines due to the lack of zero-indexing and the first line being irrelevant here
        for each_line in range(preview.get('1.0', tk.END).count('\n') - 2):
            lineNo = each_line + 2 #Similiarly, the working line is increased by two to ensure the first line is skipped
            insertIndex = getEnd(lineNo)
            preview.insert(str(lineNo) + '.' + str(insertIndex), ', ' + default)
        """


filesBtn = tk.Button(
    text = 'Create new metadata file',
    command=addFiles,
    master = toolbar_frame
    )

openBtn = tk.Button(
    text = 'Open metadata file',
    command=openFile,
    master = toolbar_frame
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

instructionsBtn = tk.Button(
    text = 'Help',
    master = toolbar_frame,
    command = showInstructions
    )

toolbar_frame.grid(row=0, column=0, sticky = 'NESW')
preview_frame.grid(row=1, column=0, sticky='NESW')
grid_canvas.grid(row=0, column=0)
grid_canvas.grid_rowconfigure(0, weight=1)
grid_canvas.grid_columnconfigure(0, weight=1)
grid_canvas.configure(yscrollcommand = vscroll.set)
grid_canvas.configure(xscrollcommand = hscroll.set)
preview_frame.grid_propagate(False)
#vscroll.grid(row=0, column=1, sticky = 'NS')
#hscroll.grid(row=1, column=0, sticky = 'EW')
lower_frame.grid(row=2, column=0)
side_frame.grid(row=1, column=1)
logo_label.grid(row=2, column=1, sticky='NESW')

#lower frame
importBtn.grid(row=1, column=0)
submitBtn.grid(row=2, column=0)

#side frame
fieldNameLabel.grid(row=0, column=0)
fieldName.grid(row=1, column=0)
fieldDefaultLabel.grid(row=2, column=0)
fieldDefault.grid(row=3, column=0)
fieldBtn.grid(row=4, column=0)

#toolbar frame
filesBtn.grid(row=0, column=0)
openBtn.grid(row=0, column=1)
instructionsBtn.grid(row=0, column=2)

#imageLabel.pack()

window.mainloop()
