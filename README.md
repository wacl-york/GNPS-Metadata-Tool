# MetadataTool
<b>Usage</b>

To use the tool, download the program from the release on the right.

Collate all the .mzML files you wish to create metadata for into one folder.

Start the tool, create a new metadata file and select the folder with your .mzML
files.

Either import a .yaml config file or add fields manually describing your files.
These will have a default value which you can modify.

When you are satisfied with the file, you can save it, and it will be ready
for use on GNPS.


<b>Development</b>

When working on linux you will need to install tkinter by running

<i>sudo apt-get install python3-tk</i>

in the terminal. Tkinter comes as default with the windows distribution of Python so no extra work is needed to develop on that platform

You will also need to install Pillow for displaying the WACL logo, which can be done by running

<i>python3 -m pip install --upgrade Pillow</i>

This needs to be done for either distribution of Python

The code can be compiled into an .exe using auto-py-to-exe. The following options were used
<i>
Onefile mode

Windows-based

Add wacl.png as an additional file
</i>
