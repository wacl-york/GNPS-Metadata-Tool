import tkinter as tk
from tkinter import filedialog as fd
from os import listdir
from os.path import isfile, join
from PIL import ImageTk, Image
import yaml
import csv

window = tk.Tk()
window.geometry('1200x700')
window.title('Metadata Tool')

window.columnconfigure(0, weight=1, minsize=200)
window.columnconfigure(1, weight=0, minsize=400)

for r in range(2):
    window.rowconfigure(r, weight=1, minsize=50)

lower_frame = tk.Frame(
    master=window
)

side_frame = tk.Frame(
    master=window
)

preview_frame = tk.Frame(
    master=window
)

toolbar_frame = tk.Frame(
    master=window
)

grid_canvas = tk.Canvas(
    master=preview_frame,
    height=200,
    width=700
)

entry_frame = tk.Frame(
    master=grid_canvas
    )

vscroll = tk.Scrollbar(
    master=preview_frame,
    orient='vertical',
    command=grid_canvas.yview
)

hscroll = tk.Scrollbar(
    master=preview_frame,
    orient='horizontal',
    command=grid_canvas.xview
)

preview = tk.Label(master=preview_frame,
                   text="""Select one of the buttons above to start creating
a metadata file""",
                   anchor='nw'
                   )

fieldName = tk.Entry(master=side_frame)
fieldDefault = tk.Entry(side_frame)
fieldNameLabel = tk.Label(text='Field to add', master=side_frame)
fieldDefaultLabel = tk.Label(text='Default value', master=side_frame)

# Opens logo in a PIL format so it can be resized
logo = Image.open('wacl.png')
logo_resized = logo.resize((350, 250))
# Resized photo is used to create a new object tkinter will accept
logo_photo_image = ImageTk.PhotoImage(logo_resized)
logo_label = tk.Label(master=window, image=logo_photo_image)
# Creates a window for the cells in the table to be displayed on
grid_canvas.create_window((0, 0), window=entry_frame, anchor='nw')

grid = [[]]
filepath = ''


def adjustScrollRegion():
    """
    Updates grid_canvas so that users can scroll
    through the entirety of the available cells

    Sets the canvas dimensions to accurately reflect the cells present in
    the grid, so that the scrollbars are placed next to the cells. The scroll
    region is also adjusted to include all of the cells.
    """

    # Needed to keep the canvas up to date with the latest changes
    entry_frame.update_idletasks()

    # Determines the correct dimensions to assign to the canvas
    # based on the cells included, maxing out at set values.
    if len(grid[0]) > 4:
        canvas_width = 700
    else:
        canvas_width = len((grid[0]) * grid[0][0].winfo_width())

    if len(grid) > 9:
        canvas_height = 200
    else:
        canvas_height = len(grid) * grid[0][0].winfo_height()

    # Reconfigures grid_canvas accordingly
    grid_canvas.config(scrollregion=grid_canvas.bbox("all"),
                       width=canvas_width,
                       height=canvas_height
                       )


def showInstructions():
    """
    Displays instructions for using the tool in a popup window

    Upon clicking the "Help" button, a new window is created, inside of which
    is a label containing the instructions,and a button, which will close
    the window when clicked.

    """
    popupWindow = tk.Tk()
    popupWindow.geometry('450x300')
    popupWindow.title('Instructions')
    label = tk.Label(popupWindow, text="""Instructions for use:
1. Put all the files you wish to create metadata
for into one folder, then select this folder
2. The files within this folder will appear in the preview.
From here you can add fields by either importing a
config file containing all the fields. Alternatively you
can add fields individually by entering the name of
the field and optionally a default value
3. From here you can modify the values as necessary
4. Click the "Save as .txt" button to finalise the folder
If you encounter any issues you can report them at""")
    label.pack()
    link = tk.Text(popupWindow, height=1)
    link.insert(1.0, 'https://github.com/wacl-york/GNPS-Metadata-Tool/issues')
    link.pack()

    def focusText(event):
        link.config(state='normal')
        link.focus()
        link.config(state='disabled')

    link.bind('<Button-1>', focusText)
    closeButton = tk.Button(popupWindow,
                            text='Close',
                            command=popupWindow.destroy
                            )
    closeButton.pack()
    popupWindow.mainloop()


def addFiles():
    """
    Adds all files in a folder to a directory

    Uses tkinter fileDialog for the user to specify a directory. All files
    in this directory are collated into a list. Tkinter entry widgets are then
    added to grid in their own list, representing a horizontal line of cells
    with each one using a filename from the list collected as it's text. These
    entries are then placed using the grid geometry manager, creating a table
    of entries.
    """
    global grid
    global filepath
    # Gets the files to add to the preview
    filepath = fd.askdirectory()
    # Checks that the directory provided is valid
    if len(filepath) > 1:
        grid = [[]]
        preview.grid_forget()
        filesToAdd = [file for file in listdir(filepath)
                      if isfile(join(filepath, file))]
        grid[0].append(tk.Entry(master=entry_frame))
        grid[0][0].insert(0, 'filename')
        grid[0][0].grid(row=0, column=0)
        row = 1
        # Creates an Entry object in grid, which corresponds
        # to it's position in the the preview, which is then
        # placed in the appropriate spot using the .grid method
        for eachFile in filesToAdd:
            grid.append([])
            grid[row].append(tk.Entry(master=entry_frame))
            grid[row][0].insert(0, eachFile)
            grid[row][0].grid(row=row, column=0)
            row += 1

        # Makes the necessary changes to the UI to allow work to continue
        fieldBtn['state'] = tk.NORMAL
        submitBtn['state'] = tk.NORMAL
        importBtn['state'] = tk.NORMAL
        vscroll.grid(row=0, column=1, sticky='NS')
        hscroll.grid(row=1, column=0, sticky='EW')
        adjustScrollRegion()


def openFile():
    """
    Allows the user to specify a metadata file to open, reads in the file, then
    displays it's contents in the table

    Uses tkinter's fileDialog package to get a valid text file to open. Using
    python's csv library and by specifying a tab as a delimiter, this file can
    be read. For each line in the file, a list is added to grid, and a new
    entry widget is created for each element in the file. These are then
    placed in the table in the same respective position as in the files

    """
    global grid
    global filepath
    filePath = fd.askopenfilename(filetypes=(("Metadata file", "*.tsv"),))
    # Ensures the filepath provided is valid
    if filePath != '':
        preview.grid_forget()
        grid = []
        # Reads in the metadata file to edit
        with open(filePath) as file:
            tsv_file = csv.reader(file, delimiter="\t")
            row_no = 0
            # Created a representation of a line
            for line in tsv_file:
                grid.append([])
                field_no = 0
                # Creates an entry widget containing the data element and
                # places it in the table
                for field in line:
                    grid[row_no].append(tk.Entry(master=entry_frame))
                    grid[row_no][field_no].insert(0, field)
                    grid[row_no][field_no].grid(row=row_no, column=field_no)
                    field_no += 1

                row_no += 1

        # Updates the UI accordingly
        fieldBtn['state'] = tk.NORMAL
        submitBtn['state'] = tk.NORMAL
        importBtn['state'] = tk.NORMAL
        vscroll.grid(row=0, column=1, sticky='NS')
        hscroll.grid(row=1, column=0, sticky='EW')
        filepath = filepath[0:filepath.rfind('/')]
        try:
            adjustScrollRegion()
        except:
            grid = []
            # Creates a popup window to let the user know that
            # their file has successfully been saved
            errorWindow = tk.Tk()
            errorWindow.title('Error')
            label = tk.Label(errorWindow, text='Your file is in the wrong format')
            label.pack()

            closeButton = tk.Button(errorWindow,
                                    text='Close',
                                    command=errorWindow.destroy
                                    )

            closeButton.pack()
            errorWindow.mainloop()
            


def addField():
    """
    Adds a new field to the grid

    Appends a new entry containing the field name to the first list and the
    default value to subsequent lists. These entries are then added to
    the preview frame using the grid method in the position corresponding to
    it's location in the 2d list
    """
    # Gets the values to use to create the field and clears the entry widgets
    field = fieldName.get()
    default = fieldDefault.get()
    fieldName.delete(0, tk.END)
    fieldDefault.delete(0, tk.END)

    # Adds a entry widget for the new field header to the first list
    grid[0].append(tk.Entry(master=entry_frame))
    grid[0][-1].insert(0, 'ATTRIBUTE_'+field)
    grid[0][-1].grid(row=0, column=len(grid[0])-1)

    # Adds an entry widget to the table in all
    # subsequent rows containing the default value
    row_no = 1
    for each_line in range(len(grid)-1):
        grid[row_no].append(tk.Entry(master=entry_frame))
        grid[row_no][-1].insert(0, default)
        grid[row_no][-1].grid(row=row_no, column=len(grid[row_no]) - 1)
        row_no += 1

    adjustScrollRegion()


def submit():
    """
    Creates an output text file from the table supplied by the user.

    Uses a filedialog to determine the filepath where the output file
    will be created. The filepath is vaidated to ensure it has the
    correct file extension, and if it is not suitable the correct file
    extension is added.

    """
    global filepath
    
    path = fd.asksaveasfilename(defaultextension=".tsv",
                                filetypes=(("tab-seperated file", "*.tsv"),),
                                initialdir=filepath)
    # Ensures a valid path has been selected, and that
    # the user hasn't clicked cancel
    if path != '':
        # Ensures the file is saved as a .txt, rather than anything else
        if path.find('.') != -1:
            path = path[0:path.find('.')]
            path += '.tsv'

            # Creates a file to write into
            writeFile = open(path, 'w')
            index = ''
            line_number = 0
            for each_line in grid:
                line_number += 1
                # Writes each element in each line to the file.
                # Where the element is the start of the new line, no tab is
                # added otherwise a tab is added before every element
                new_line = True
                for each_field in each_line:
                    if new_line:
                        new_line = False
                        writeFile.write(each_field.get())
                    else:
                        writeFile.write('\t')
                        writeFile.write(each_field.get())

                # Prevents a new line from being added at the end of the file
                if line_number < len(grid):
                    writeFile.write('\n')

                # Changes the value of index for the next line as appropriate
                if index == '':
                    index = 0
                else:
                    index += 1

            writeFile.close()

            # Creates a popup window to let the user know that
            # their file has successfully been saved
            feedbackWindow = tk.Tk()
            feedbackWindow.title('File saved')
            label = tk.Label(feedbackWindow, text='File saved successfully')
            label.pack()

            closeButton = tk.Button(feedbackWindow,
                                    text='Close',
                                    command=feedbackWindow.destroy
                                    )

            closeButton.pack()
            feedbackWindow.mainloop()


def importConfig():
    """
    Reads in a yaml file and adds the fields it contains to the preview

    User selects a file, which is then parsed to get two lists containing
    the names and default values of each field. These two lists are then
    iterated through to add all the fields to the grid in the same manner
    as addFiles()
    """
    # User selects config file
    configPath = fd.askopenfilename(filetypes=(("YAML file", "*.yaml"),))
    if configPath != '':
        # Config file is read
        with open(configPath) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        names = []
        values = []
        # Iterates through each entry in the config file, adds
        # each element in each entry to the lists as a string
        for each_field in data['fields']:
            if type(each_field['Name']) != str:
                names.append(str(each_field['Name']))
            else:
                names.append(each_field['Name'])

            if type(each_field['Default']) != str:
                values.append(str(each_field['Default']))
            else:
                values.append(each_field['Default'])

        for each_field in range(len(names)):
            # Creates an entry widget for the field
            # name in the first list in grid
            field = names[each_field]
            default = values[each_field]
            grid[0].append(tk.Entry(master=entry_frame))
            grid[0][-1].insert(0, 'ATTRIBUTE_'+field)
            grid[0][-1].grid(row=0, column=len(grid[0])-1)
            row_no = 1
            # Creates entry widgets in all subsequent lists in grid containing
            # the default value provided
            for each_line in range(len(grid)-1):
                grid[row_no].append(tk.Entry(master=entry_frame))
                grid[row_no][-1].insert(0, default)
                grid[row_no][-1].grid(row=row_no, column=len(grid[row_no]) - 1)
                row_no += 1

        adjustScrollRegion()


filesBtn = tk.Button(
    text='Create new metadata file',
    command=addFiles,
    master=toolbar_frame
    )

openBtn = tk.Button(
    text='Open metadata file',
    command=openFile,
    master=toolbar_frame
    )

fieldBtn = tk.Button(
    text='Add field',
    command=addField,
    state='disabled',
    master=side_frame
    )

submitBtn = tk.Button(
    text='Save as .tsv',
    command=submit,
    state='disabled',
    master=lower_frame
    )

importBtn = tk.Button(
    text='Import config',
    command=importConfig,
    state='disabled',
    master=lower_frame
    )

instructionsBtn = tk.Button(
    text='Help',
    master=toolbar_frame,
    command=showInstructions
    )

# Places all the frames in the correct position
toolbar_frame.grid(row=0, column=0, sticky='NESW')
preview_frame.grid(row=1, column=0, sticky='NESW')
grid_canvas.grid(row=0, column=0)
grid_canvas.grid_rowconfigure(0, weight=1)
grid_canvas.grid_columnconfigure(0, weight=1)
lower_frame.grid(row=2, column=0)
side_frame.grid(row=1, column=1)

# Places widgets in the root window
preview.grid(row=0, column=0)
logo_label.grid(row=2, column=1, sticky='NESW')

# Configures widgets as necessary
grid_canvas.configure(yscrollcommand=vscroll.set)
grid_canvas.configure(xscrollcommand=hscroll.set)
preview_frame.grid_propagate(False)

# lower frame
importBtn.grid(row=1, column=0)
submitBtn.grid(row=2, column=0)

# side frame
fieldNameLabel.grid(row=0, column=0)
fieldName.grid(row=1, column=0)
fieldDefaultLabel.grid(row=2, column=0)
fieldDefault.grid(row=3, column=0)
fieldBtn.grid(row=4, column=0)

# toolbar frame
filesBtn.grid(row=0, column=0)
openBtn.grid(row=0, column=1)
instructionsBtn.grid(row=0, column=2)

window.mainloop()
