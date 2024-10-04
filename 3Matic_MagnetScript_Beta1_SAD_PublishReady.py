# Created on 6/19/24 by Samir Dabit
# This Publish-Ready version was created on 10/4/24 by Samir Dabit
# Last update on 10/4/24 by Samir Dabit
# This is the automatic magnet-placing script.

# Beta 1 is the first beta release.
""" ChangeLog:
    | Added Bug list window.
    | Bug fixes
"""

# Tip   : Ctrl+K Ctrl+0 collapses all collapsables.
# Notes : I use the terms 'entity' and 'part' interchangeably.
#         'return' does not work normally when using Tkinter. I used global variables to get around it.

# EventTypes numbers
#        > ComboboxSelect = 35
#        > Keypress = 2
#        > mouse ButtonPress = 4

""" Known issues:
    - Finding parts based on name. There should be a safer way to do this in a revision.
    - Double click smth gives 2 points when indicates
    - When Ctrl+Z during moving object, and then try to undo, it breaks.
"""

""" TODO: Current Task (everything everywhere all the time)
        [* means completed]

        important Tasks:

        Other Tasks:
        (R) Delete cut planes after they are used?
        (C) Revise Pseudocode to be more accurate & easier to read.
        (D) Reorganize methods.
        (P) Add decorators to methods
"""

import trimatic 

import os
# Tkinter is Python's Native GUI interface.
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

"""=-=-=-=-=-=-= Tkinter Online Resources =-=-=-=-=-=-= 
    :Sources: https://www.tutorialspoint.com/taking-input-from-the-user-in-tkinter
              https://www.geeksforgeeks.org/python-gui-tkinter/
"""

""" *.*.*.* Global Variables *.*.*.* 
"""

""" Coordinates for cutting magnets.
    An exteral script by SD was used to determine
     the proper coordinates for each magnet. 
"""
# Mini:
global miniNormalVector, miniOrigin
miniNormalVector = (0,0,1)                      # Set normal vector.
miniOrigin = (0, 0, -1.8873)                    # Set origin.
# Small:
global smallNormalVector, smallOrigin
smallNormalVector = (0,0,1)                     # Set normal vector.
smallOrigin = (16.005, 0, -1.8873)              # Set origin.
# Medium:
global mediumNormalVector, mediumOrigin
mediumNormalVector = (0.0081, 0.0795, -0.9968)
mediumOrigin = (52.8740, 27.3056, 10.3033)
# Large:
global largeNormalVector, largeOrigin
largeNormalVector = (0,0,1)                     # Set normal vector.
largeOrigin = (42.7814, 0, 0)                   # Set origin.

""" Standard Fonts for Tkinter GUI.
"""
global titleFont, subtitleFont, bodyFont
titleFont=('Arial', 12, 'bold')
subtitleFont=('Arial', 10, 'italic')
bodyFont=('Arial', 10)

global global_numCutPlanes
global_numCutPlanes = 0

global global_prevWindowX, global_prevWindowY
global_prevWindowX = 0
global_prevWindowY = 0

global global_currentRunNum
global_currentRunNum = 0

global global_currentHousingSet
global_currentHousingSet = None
# *.*.* End Global Variables *.*.*

# =-=-=-=-=-=-==-=-=-=-=-=-= ALL METHODS =-=-=-=-=-=-==-=-=-=-=-=-=
""" Imports Heart Model for testing.
    | return: void
"""
def ImportHeartModel(filePath_global):
    fileEnding = r"X\X\X"
    path = filePath_global + fileEnding
    trimatic.open_project(path)

""" Finds a valid file path to use for the magnet STL files.
"""
def InitializeFileVariables():
    trimatic.suspend_progress()

    filePath1 = r"X:"
    filePath2 = r'X:\X\X'
    filePath3 = r'\\X\X\X\X'
    filePath4 = r'\\X\X\X\X'

    # Create filePathArray. Make sure that all 3 file paths are in the array b4 running.
    filePathsArray = [filePath1, filePath2, filePath3, filePath4]
    # filePathsArray = [filePath2]

    # Check filepath text file on local desktop
    main_drive = os.path.splitdrive(os.environ['SystemDrive'])[0]
    applicationPath = os.path.dirname(main_drive + "\\")

    saveDirectoryName = "3Matic_ScriptSaveFiles"
    saveDirectoryPath = os.path.join(applicationPath, saveDirectoryName)

    saveFileName = "MagnetWizard_SaveFile.txt"
    saveFilePath = os.path.join(saveDirectoryPath, saveFileName)

    # If savefile exists, append each line to filePathsArray
    if os.path.exists(saveDirectoryPath):
        print("Save file already exists.")
        try:
            file = open(saveFilePath, "r")
        except:
            print("File not found.")
            file = open(saveFilePath, "w")
            file.close()
            file = open(saveFilePath, "r")

        lines = file.readlines()

        for line in lines:
            filePathsArray.append(line)

    # Try each pre-saved file paths.
    for filePath in filePathsArray:

        # Check if the file path exists.
        if(os.path.exists(filePath)):
            print("File path " + filePath + " exists!")

            # Store the file path, update the global magnet file paths variables.
            global filePath_global
            filePath_global = filePath
            UpdateMagnetFilePaths(filePath)
            return
        
    # If none of the file paths work. ask user for their specific file path.
    AskForFilePathAndUpdate()

    return

""" Create a text file @ saveDirectoryPath to store workingFilePath. 
"""
def CreateFilePathSaveFile(workingFilePath):
    # Check filepath text file on local desktop
    main_drive = os.path.splitdrive(os.environ['SystemDrive'])[0]
    applicationPath = os.path.dirname(main_drive + "\\")

    saveDirectoryName = "3Matic_ScriptSaveFiles"
    saveDirectoryPath = os.path.join(applicationPath, saveDirectoryName)

    saveFileName = "MagnetWizard_SaveFile.txt"
    saveFilePath = os.path.join(saveDirectoryPath, saveFileName)

    # Create directory
    if not os.path.exists(saveDirectoryPath):
        os.makedirs(saveDirectoryPath)
        print(f"Directory {saveDirectoryName} created.")

    print(f"Writing {workingFilePath} to {saveFilePath}")
    file = open(saveFilePath, "a")      # Open savefile
    file.write("\n" + workingFilePath)  # Add working path to end
    file.close()

    return

""" Updates the magnet file paths.
    | param filePath: string
"""
def UpdateMagnetFilePaths(filePath):
    trimatic.suspend_progress()

    # Magnet Files
    global magnetMini, magnetSmall, magnetMedium, magnetLarge
    magnetMini      = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Mini Magnet B 3.2mmx1.59mm.stl"
    magnetSmall     = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Small Magnet B 6.35mmx1.59mm.stl"
    magnetMedium    = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Medium Magnet 6.35mmx2.54mm.stl"
    magnetLarge     = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Large Magnet A 6.35mmx5.08mm.stl"

    # Magnet Housings
     # Mini
    global magnetMiniHousingA,   magnetMiniHousingB     # Minis
    magnetMiniHousingA = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Mini Housing A.stl"
    magnetMiniHousingB = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Mini Housing B.stl"

     # Smalls
    global magnetSmallHousingA,  magnetSmallHousingB    # Smalls
    magnetSmallHousingA = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Small Housing A.stl"
    magnetSmallHousingB = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Small Housing B.stl"

     # Mediums
    global magnetMediumHousingA, magnetMediumHousingB   # Mediums
    magnetMediumHousingA = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Medium Housing A.stl"
    magnetMediumHousingB = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Medium Housing B.stl"

     # Larges
    global magnetLargeHousingA,  magnetLargeHousingB    # Larges
    magnetLargeHousingA = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Large Housing A.stl"
    magnetLargeHousingB = filePath + r"\3. Technical\Scripting\STLs_DoNotTouch\Magnets\Large Housing B.stl"

    return

""" Creates Tkinter Window. Asks the user to input a their X file path.
"""
def AskForFilePathAndUpdate():
    trimatic.suspend_progress()

    # Initialize Tkinter root
    winPath = tk.Tk()
    winPath.title('Magnet Wizard')
    winPath.attributes('-topmost', True)
    # winPath.focus_set() # Focuses on window.
    winPath.geometry(f"315x120+{global_prevWindowX}+{global_prevWindowY}")
    winPath.resizable(False, False)

    top_frame = Frame(winPath, width=315, height=60)
    top_frame.grid(row=0, padx=5)
    middle_frame = Frame(winPath, width=315, height=60)
    middle_frame.grid(row=1, pady=10)
    bottom_frame = Frame(winPath, width=315)
    bottom_frame.grid(row=2)

    textEntry_var = tk.StringVar()
    textEntry_var.set("X:\...")

    winPath.submittable = False
    winPath.filePath = ""

    """ If a valid file path is given, save it to the filepath save file. Otherwise, keep asking for a file path.
    """
    def submit():
        # Check if file path exists.
        # Keep asking user to input until the file path is valid.

        # Check if file exists already.
        if (winPath.submittable):
            # If true, return file path name.
            print("A file path has been successfully found: " + winPath.filePath)

            global filePath_global
            filePath_global = winPath.filePath

            UpdateMagnetFilePaths(filePath_global)
            CreateFilePathSaveFile(winPath.filePath) # Testing

            UpdateWindowSpawnCoords(winPath)
            winPath.destroy()
            return
        else: 
            # If false, force user to input again.

            # Tell user to enter a valid file path.
            if (textEntry_var.get() == ""):
                print("Enter a file path.")
            else:
                print(textEntry_var.get() + " is not a valid file path.")

            # Update display.
            winPath.geometry("315x150")
            invalidLabel.config(text="Invalid File Path")
            return

    """ Exits Wizard
    """
    def quit():
        ExitWizard(winPath)

    def checkForSubmit():
        # Strip space off beginning and end
        currFilePath_stripped = textEntry_var.get().strip()
        
        # Delete all trailing periods.
        currFilePath_stripped = currFilePath_stripped.rstrip(".")

        # Check each file path that could be input
        filePathEnding = r"\X\X\X\X"
        currentString = ""
        for char in filePathEnding[::-1]:
            currentString += char
            testPath = currFilePath_stripped + currentString[::-1]
            # print(testPath)
            if os.path.exists(testPath) and testPath.endswith(filePathEnding):
                generalDrive = testPath.split(filePathEnding)[0]
                print(generalDrive)
                winPath.filePath = generalDrive
                winPath.submittable = True
                break
            else:
                winPath.filePath = ""
                winPath.submittable = False

        print(f"filepath: {winPath.filePath}")
        
        # Update UI
        if (winPath.submittable):
            sub_btn.config(bg='lime green')
        else:
            sub_btn.config(bg='light gray')
        return

    def on_textbox_input(event):
        winPath.after(1, checkForSubmit)
        return
    
    def on_hotkey_enter(event):
        checkForSubmit()
        submit()
        return

    # Text labels and Buttons
    textLabel = tk.Label(top_frame, text = "Enter your file path.", font=('Arial', 12, 'bold'))
    descriptionLabel = tk.Label(top_frame, text = "Copy your file path for the general location.", font=('Arial', 10, 'italic'))
    filePath_Entry = tk.Entry(top_frame, text = "X:\...", textvariable=textEntry_var, width=30)

    sub_btn = tk.Button(middle_frame, text = 'Submit', command = submit, background = 'light gray')
    quit_btn = tk.Button(middle_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2')

    invalidLabel = tk.Label(bottom_frame, text = "", font=('Arial', 12), fg="red")

    # Set locations
    textLabel.grid(row=0)
    descriptionLabel.grid(row=1)
    filePath_Entry.grid(row=2)

    sub_btn.grid(row=0, column=0, padx=15)
    quit_btn.grid(row=0, column=1, padx=15)

    invalidLabel.grid(row=0)

    filePath_Entry.bind('<ButtonRelease>', on_textbox_input)
    filePath_Entry.bind('<KeyRelease>', on_textbox_input)
    winPath.bind('<Return>', on_hotkey_enter)

    winPath.protocol("WM_DELETE_WINDOW", quit)

    winPath.mainloop()

    return

""" Creates Tkinter Window. Asks the user to input the desired amount of magnets of each size.
    | return: magnetNumMini
    | rtype : global int
    | 
    | return: magnetNumSmall
    | rtype : global int
    | 
    | return: magnetNumMedium
    | rtype : global int
    | 
    | return: magnetNumLarge
    | rtype : global int
    | 
    | return: magnetNumTotal
    | rtype : global int
"""
def AskForSizeInput():
    trimatic.suspend_progress()

    # Initializes Tkinter root
    winSize = tk.Tk()

    # Sets geometry (width x height)
    winSize.geometry(f"285x285+{global_prevWindowX}+{global_prevWindowY}")

    winSize.attributes('-topmost', True)
    # winSize.focus_set() # Focuses on window.

    # Set Title
    winSize.title('Magnet Wizard')
    winSize.resizable(False, False)

    menubutton_frame = Frame(winSize)
    menubutton_frame.grid(row=0)
    top_frame = Frame(winSize, width=285)
    top_frame.grid(row=1)
    middle_frame = Frame(winSize, width=285)
    middle_frame.grid(row=2, pady=10)
    bottom_frame = Frame(winSize, width=285)
    bottom_frame.grid(row=3)

    # Variables
    magnetSize_Mini_var   = tk.IntVar()
    magnetSize_Small_var  = tk.IntVar()
    magnetSize_Medium_var = tk.IntVar()
    magnetSize_Large_var  = tk.IntVar()

    winSize.submittable = False

    def submit():
        if not winSize.submittable:
            print("Unable to submit.")
            return
        
        saveMagnetNums()

        # Prevents the user from continuing with the script unless the following conditions are met.
        if magnetNumTotal <= 0: print("[ERROR] Unable to continue:\n    Please input magnet numbers.")
        else:                   NextMainWindow(winSize)

    def quit():
        ExitWizard(winSize)

    def skip():
        global global_isMagnetImportSkipped
        global_isMagnetImportSkipped = True
        saveMagnetNums()
        NextMainWindow(winSize)
        return

    def isPosInt(string):
            if string.isdigit():
                if int(string) > 0:
                    return True
            else: 
                return False

    def checkForSubmit():
        # IMPORTANT LINE
        print(f"Updated value: {S1.get()}")

        mini = S1.get()
        small = S2.get()
        medium = S3.get()
        large = S4.get()

        miniStr = str(mini)
        smallStr = str(small)
        mediumStr = str(medium)
        largeStr = str(large)

        # Edge case: when backspace is clicked, it adds a backspace char at the end before deleting.
        #       > need to simulate deletion if this happens.
        #       > account for 'Delete' key

        # Check if at least one digit is positive int
        if isPosInt(miniStr) or isPosInt(smallStr) or isPosInt(mediumStr) or isPosInt(largeStr):
            print("Submittable!")
            winSize.submittable = True
            sub_btn.config(bg='lime green') # Make submit button green
        else: 
            print("Not submittable!")
            winSize.submittable = False
            sub_btn.config(bg='light gray') # Make submit button gray
        return

    def on_spinbox_change(event):
        winSize.after(1, checkForSubmit())
        return
    
    def on_spinbox_arrow():
        winSize.after(1, checkForSubmit())
        return

    def saveMagnetNums():
        global magnetNumMini
        if S1.get().isdigit():  magnetNumMini = int(S1.get())
        else:                   magnetNumMini = 0

        global magnetNumSmall
        if S2.get().isdigit():  magnetNumSmall = int(S2.get())
        else:                   magnetNumSmall = 0

        global magnetNumMedium
        if S3.get().isdigit():  magnetNumMedium = int(S3.get())
        else:                   magnetNumMedium = 0

        global magnetNumLarge
        if S4.get().isdigit():  magnetNumLarge = int(S4.get())
        else:                   magnetNumLarge = 0

        global magnetNumTotal
        magnetNumTotal = magnetNumMini + magnetNumSmall + magnetNumMedium + magnetNumLarge
        return

    def on_hotkey_enter(event):
        checkForSubmit()
        submit()

    # Label & Entry
    SetupMenubuttons(winSize)

        # Size of magnets?
    title_label = tk.Label(top_frame, text = 'Magnet Sizes',  font=('Arial', 12, 'bold'))
    subtitle_label = tk.Label(top_frame, text = 'Enter the amount of each magnet size you want.', font=('Arial', 10, 'italic'))


    S1Label = tk.Label(middle_frame, text = "Mini\n3.2 x 1.59 [mm]", font=('Arial', 10, 'bold'))
    S2Label = tk.Label(middle_frame, text = "Small\n6.35 x 1.59 [mm]", font=('Arial', 10, 'bold'))
    S3Label = tk.Label(middle_frame, text = "Medium\n6.35 x 2.54 [mm]", font=('Arial', 10, 'bold'))
    S4Label = tk.Label(middle_frame, text = "Large\n6.35 x 5.08 [mm]", font=('Arial', 10, 'bold'))
    S1 = tk.Spinbox(middle_frame, from_=0, to_=999999999, textvariable = magnetSize_Mini_var, font=('Arial', 12), command=on_spinbox_arrow, width=10)
    S2 = tk.Spinbox(middle_frame, from_=0, to_=999999999, textvariable = magnetSize_Small_var, font=('Arial', 12), command=on_spinbox_arrow, width=10)
    S3 = tk.Spinbox(middle_frame, from_=0, to_=999999999, textvariable = magnetSize_Medium_var, font=('Arial', 12), command=on_spinbox_arrow, width=10)
    S4 = tk.Spinbox(middle_frame, from_=0, to_=999999999, textvariable = magnetSize_Large_var, font=('Arial', 12), command=on_spinbox_arrow, width=10)
    
        # Submit button
    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'light gray')

        # Quit Button
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2')

    # skip_btn = tk.Button(bottom_frame, text = 'Skip →', command = skip, background = 'goldenrod2')
    
    # Setting Locations
    title_label.grid(row=0)
    subtitle_label.grid(row=1)

    S1Label.grid(row=1, column=0)
    S1.grid(row=1, column=1)
    S2Label.grid(row=2, column=0)
    S2.grid(row=2, column=1)
    S3Label.grid(row=3, column=0)
    S3.grid(row=3, column=1)
    S4Label.grid(row=4, column=0)
    S4.grid(row=4, column=1)

    sub_btn.grid(row=7, column=0, padx=15)
    quit_btn.grid(row=7, column=1, padx=15)
    # skip_btn.grid(row=7, column=2, padx=15)

    # Binds
    S1.bind('<KeyRelease>', on_spinbox_change)
    S2.bind('<KeyRelease>', on_spinbox_change)
    S3.bind('<KeyRelease>', on_spinbox_change)
    S4.bind('<KeyRelease>', on_spinbox_change)

    S1.bind('<ButtonRelease>', on_spinbox_change)
    S2.bind('<ButtonRelease>', on_spinbox_change)
    S3.bind('<ButtonRelease>', on_spinbox_change)
    S4.bind('<ButtonRelease>', on_spinbox_change)

    winSize.bind('<Return>', on_hotkey_enter)

    winSize.protocol("WM_DELETE_WINDOW", quit)

    # Loop until closed
    winSize.mainloop()

""" Creates Tkinter Window. Asks user if they want housings around the magnet.
    | param size      : int
    | param currentNum: int
    | param totalNum  : int
    | 
    | return: magnetHousing
    | rtype : global boolean
"""
def AskForHousingInput(size, currentNum, totalNum):
    trimatic.suspend_progress()

    # Print to console
    print("Please click 'Submit' to select housing option.")

    # Initializes Tkinter root
    # global winHousing   # Global b/c close when all magnets are done (outside of this function).
    winHousing = tk.Tk()

    # Global so that I can change it back to False before every loop.
    global magnetHousing
    magnetHousing = False

    # Make Window Stay on Top
    winHousing.attributes('-topmost', True)
    # winHousing.focus_set() # Focuses on window.

    # Sets geometry (width x height)
    winHousing.geometry(f"250x150+{global_prevWindowX}+{global_prevWindowY}")

    # Set Title
    winHousing.title('Magnet Wizard')

    winHousing.resizable(False, False)

    # MENU BUTTON
    menubutton_frame = Frame(winHousing)
    menubutton_frame.grid(row=0)
    
    top_frame = Frame(winHousing, width=120, height=60)
    top_frame.grid(row=1, padx=5)
    middle_frame = Frame(winHousing, width=120, height=30)
    middle_frame.grid(row=2, pady=10)
    bottom_frame = Frame(winHousing, width=120, height=30)
    bottom_frame.grid(row=3)

    # Save and return the value.
    def submit():
        global magnetHousing
        magnetHousing = magnetHousing_var.get()
        print("You answered: " + str(magnetHousing))
        NextMainWindow(winHousing)
    
    def quit():
        ExitWizard(winHousing)

    def selectYes():
        yesButton.config(bg='pale green')
        noButton.config(bg='goldenrod2')
        return
    
    def selectNo():
        yesButton.config(bg='goldenrod2')
        noButton.config(bg='salmon')
        return
    
    def on_hotkey_enter(event):
        submit()

    SetupMenubuttons(winHousing)

    title_label = tk.Label(top_frame, text = "Housings", font=('Arial', 12, 'bold'))
    size_label = tk.Label(top_frame, text = "Would you like housings for " + size + " " + str(currentNum) + "/" + str(totalNum) + "?", font=('Arial', 10, 'italic'))

    magnetHousing_var = tk.BooleanVar()

    yesButton = Radiobutton(middle_frame, text = "Yes", variable = magnetHousing_var, value = True, font=('Arial', 10, 'bold'), bg='goldenrod2', command=selectYes)
    noButton = Radiobutton(middle_frame, text = "No", variable = magnetHousing_var, value = False, font=('Arial', 10, 'bold'), bg='goldenrod2', command=selectNo)

    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'lime green')
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2')

    # Set Locations on Grid
    title_label.grid(row=0)
    size_label.grid(row=1)

    yesButton.grid(row=0, column=0, padx=5)
    noButton.grid(row=0, column=1, padx=5)

    sub_btn.grid(row=0, column=0, padx=10)
    quit_btn.grid(row=0, column=1, padx=10)

    winHousing.bind('<Return>', on_hotkey_enter)

    winHousing.protocol("WM_DELETE_WINDOW", quit)

    # Loop until closed
    winHousing.mainloop()

""" Creates Tkinter Window. Asks the user to select a cut plane with 3 options: Dropdown, Manual, and Object Tree.
    Only 'Exit Wizard' and 'Skip' buttons are located in this window. All other buttons are located within the subframe.
"""
def AskForCutPlane():
    trimatic.suspend_progress()
    
    # <><><><><> Initialize variables <><><><><>
    global sizeAndMagNumArr
    [currSize, currNum, totalNum] = sizeAndMagNumArr

    winPlane = tk.Tk()
    winPlane.title('Magnet Wizard')
    winPlane.attributes('-topmost', True)
    # winPlane.focus_set() # Focuses on window.
    winPlane.geometry(f"275x340+{global_prevWindowX}+{global_prevWindowY}") # width x height
    winPlane.resizable(False, False)

    # MENU BUTTON
    menubutton_frame = Frame(winPlane)
    menubutton_frame.grid(row=0)

    title_frame = Frame(winPlane)
    title_frame.grid(row=1)

    button_frame_1 = Frame(winPlane)
    button_frame_1.grid(row=2, pady=10)

    dropdown_frame = Frame(winPlane)
    dropdown_frame.grid(row=3)

    manual_frame = Frame(winPlane)
    manual_frame.grid(row=4)

    object_tree_frame = Frame(winPlane)
    object_tree_frame.grid(row=5)

    button_frame_2 = Frame(winPlane)
    button_frame_2.grid(row=6)

    # Initialize skip variable
    global global_skip_alignment
    global_skip_alignment = False

    # <><><><><> Commands <><><><><>
    def select_dropdown():

        # Hide quit button from the outer frame
        quit_btn.grid_forget()

        if (len(trimatic.get_planes()) == 0):
            print("There are no planes available. Please use the other method.")
            return
            
        option1_btn.config(bg='PaleVioletRed1')
        option3_btn.config(bg='light gray')
        option2_btn.config(bg='light gray')

        # Hide other frame
        manual_frame.grid_forget()
        object_tree_frame.grid_forget()

        dropdown_frame.grid(row=3, pady=10)
        
        winPlane.geometry("300x467")

        AskForFixedPlaneDropdown(winPlane, dropdown_frame)

        return

    def select_manual():

        # Hide quit button from the outer frame
        quit_btn.grid_forget()

        # Recolor option buttons
        option2_btn.config(bg='PaleVioletRed1')
        option1_btn.config(bg='light gray')
        option3_btn.config(bg='light gray')

        # Hide other frame
        dropdown_frame.grid_forget()
        object_tree_frame.grid_forget()

        # Resize outer window
        manual_frame.grid(row=3, pady=10)

        winPlane.geometry("290x527")

        AskForFixedPlanePoints(winPlane, manual_frame)

        return
    
    def select_object_tree():
        
        # Hide quit button from the outer frame
        quit_btn.grid_forget()

        # Recolor option buttons
        option3_btn.config(bg='PaleVioletRed1')
        option1_btn.config(bg='light gray')
        option2_btn.config(bg='light gray')

        # Hide other frame
        dropdown_frame.grid_forget()
        manual_frame.grid_forget()

        # Resize outer window
        object_tree_frame.grid(row=3, pady=10)

        winPlane.geometry("280x492")

        AskForFixedPlaneObjectTree(winPlane, object_tree_frame)

        return

    def quit():
        ExitWizard(winPlane)

    def skip():
        global global_skip_alignment
        global_skip_alignment = True
        NextMainWindow(winPlane)
    
    # <><><><><> Initialize Labels and Buttons <><><><><>
    SetupMenubuttons(winPlane)

    title_label = tk.Label(title_frame, text = "Find Fixed Plane", font=('Arial', 14, 'bold'))
    subtitle_label = tk.Label(title_frame, text = f"Select your preferred method below.\n{currSize} {currNum}/{totalNum}", font=('Arial', 12, 'italic'))

    option1_label = tk.Label(button_frame_1, text = "Select from a dropdown of existing planes.", font=('Arial', 10))
    option1_btn = tk.Button(button_frame_1, text="Dropdown", command = select_dropdown, background='light gray', width=15)
    spacer_label1 = tk.Label(button_frame_1, text = "")
    option2_label = tk.Label(button_frame_1, text = "Manually select 3 points to define a plane.", font=('Arial', 10))
    option2_btn = tk.Button(button_frame_1, text="Manual", command = select_manual, background='light gray', width=15)
    spacer_label2 = tk.Label(button_frame_1, text = "")
    option3_label = tk.Label(button_frame_1, text = "Select a plane from the object tree.", font=('Arial', 10))
    option3_btn = tk.Button(button_frame_1, text="Object Tree", command = select_object_tree, background='light gray', width=15)

    quit_btn = tk.Button(button_frame_2, text = 'Exit Wizard', command = quit, background = 'firebrick2', width=15)
    skip_btn = tk.Button(button_frame_2, text = 'Skip →', command = skip, background = 'goldenrod2')

    # <><><><><> Set Locations on Grid <><><><><>
    title_label.grid(row=0)
    subtitle_label.grid(row=1)

    option1_label.grid(row=0)
    option1_btn.grid(row=1)
    spacer_label1.grid(row=2)
    option2_label.grid(row=3)
    option2_btn.grid(row=4)
    spacer_label2.grid(row=5)
    option3_label.grid(row=6)
    option3_btn.grid(row=7)

    quit_btn.grid(row = 0, column = 0, padx=20, pady=5)
    skip_btn.grid(row = 0, column = 1)

    winPlane.protocol("WM_DELETE_WINDOW", quit)

    winPlane.mainloop()

    return

""" Creates UI in subframe 'frame' of root. User selects a cut plane from a dropdown of all planes in the 3-Matic file.
    | param root : Tkinter window
    | param frame: subframe of root
    |
    | return: globalCutPlane
    | rtype : global Trimatic Plane
"""
def AskForFixedPlaneDropdown(root, frame):
    trimatic.suspend_progress()

    # Initialize variables
    planeList = trimatic.get_planes()

    # Convert list to have names.
    planeNameList = []
    for plane in planeList:
        planeNameList.append(plane.name)

    planeName_var = tk.StringVar()

    frame.submittable = False

    # Frames
    top_frame = Frame(frame)
    top_frame.grid(row=0)

    middle_frame = Frame(frame)
    middle_frame.grid(row=1)

    bottom_frame = Frame(frame)
    bottom_frame.grid(row=2)

    def submit():
        if not frame.submittable:
            print("Unable to submit.")
            return
        
        # This variable aligns with the manual method's var.
        global globalCutPlane
        globalCutPlane = trimatic.find_plane(planeName_var.get())
        NextMainWindow(root)
    
    def quit():
        ExitWizard(root)

    def checkForSubmit(event):
        if combobox.get() in planeNameList:
            frame.submittable = True
            sub_btn.config(bg='lime green') # Make submit button green
            print("Selected plane is valid.")
        else:
            sub_btn.config(bg='light gray') # Make submit button green
            print("Selected plane is not valid.")
        return

    def on_combobox_input(event):
        frame.after(1, checkForSubmit(event))
        return
        
    def on_hotkey_enter(event):
        checkForSubmit(None)
        submit()

    # Initialize Labels and Buttons
    title_label = tk.Label(top_frame, text="Select A Plane", font=('Arial', 12, 'bold'))
    subtitle_label = tk.Label(top_frame, text="Select your fixed plane from the dropdown below.", font=('Arial', 10, 'italic'))

    combobox = ttk.Combobox(middle_frame, values=planeNameList, textvariable=planeName_var, width = 35)
    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'light gray', width=15)
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2', width=15)

    # Set Locations on Grid
    title_label.grid(row=0)
    subtitle_label.grid(row=1, padx=5)

    combobox.grid(row=0)

    sub_btn.grid(row=0, column=0, padx=10, pady=10)
    quit_btn.grid(row=0, column=1, padx=10)

    # Events
    combobox.bind('<KeyRelease>', on_combobox_input)
    combobox.bind('<ButtonRelease>', on_combobox_input)
    combobox.bind('<<ComboboxSelected>>', on_combobox_input)
    combobox.bind('<<FocusIn>>', on_combobox_input)
    combobox.bind('<<MouseScroll>>', on_combobox_input)

    root.bind('<Return>', on_hotkey_enter)

    root.protocol("WM_DELETE_WINDOW", quit)

    frame.mainloop()

    return

""" Creates UI in subframe 'frame' of root. User selects 3 points manually or types coordinates in. A preview plane is created when coordinates are valid.
    | param root : Tkinter window
    | param frame: subframe of root
    |
    | return: globalCutPlane
    | rtype : global Trimatic Plane
"""
def AskForFixedPlanePoints(root, frame):
    trimatic.suspend_progress()

    frame.current_num = 0 # Creates a self-contained variable.
    frame.points_array         = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    frame.points_array_display = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    pointEntry1_var = tk.StringVar()
    pointEntry2_var = tk.StringVar()
    pointEntry3_var = tk.StringVar()

    frame.isEntry1Filled = False
    frame.isEntry2Filled = False
    frame.isEntry3Filled = False

    frame.updatedNumEntry1 = ""
    frame.updatedNumEntry2 = ""
    frame.updatedNumEntry3 = ""

    frame.previewPlaneExists = False

    # Frames
    top_frame = Frame(frame)
    top_frame.grid(row=0)

    middle_frame = Frame(frame)
    middle_frame.grid(row=1)

    bottom_frame = Frame(frame)
    bottom_frame.grid(row=2)

    prevNumArr = []
    prevEntryArr = []

    # Commands
    def submit():
        #if (frame.current_num >= 3):
        if frame.isEntry1Filled and frame.isEntry2Filled and frame.isEntry3Filled:
            print("All points sucessfully selected.")
            NextMainWindow(root)
        else:
            print("Cannot Submit.")
        return

    def quit():
        ExitWizard(root)

    def undo():
        # First, check if undo can run.
        if getNumFilledEntries() == 0:
            print("Cannot undo.")
            return

        # Update number of planes.
        global global_numCutPlanes
        global_numCutPlanes = global_numCutPlanes - 1

        # Delete last element in each array & Store them
        prevNum = prevNumArr.pop()
        prevEntry = prevEntryArr.pop()

        prevEntry.delete(0, "end")   # Clear correct entry field
        prevEntry.insert(0, prevNum) # Insert last entered number

        # Determine which entry field was last updated.
        if prevEntry == pointEntry1:    updateIndex = 0
        elif prevEntry == pointEntry2:  updateIndex = 1
        elif prevEntry == pointEntry3:  updateIndex = 2

        # Clear correct point in saved array.
        frame.points_array[updateIndex] = [0, 0, 0]
        frame.points_array_display[updateIndex] = [0, 0, 0]

        # Update isFilled booleans
        if prevEntry == pointEntry1:
            frame.isEntry1Filled = False
        elif prevEntry == pointEntry2:
            frame.isEntry2Filled = False
        elif prevEntry == pointEntry3:
            frame.isEntry3Filled = False

        # Delete Preview Plane if it exists.
        if frame.previewPlaneExists == True:
            DeleteTrimaticEntity(frame.plane)
            print("Preview plane deleted.")
            frame.previewPlaneExists = False
        
        # Update Window Title
        updateWindowTitle()

        # Update color of undo button if necessary
        if getNumFilledEntries() == 0:
            undo_btn.config(bg='light gray')

        # Make sure submit is grayed out
        sub_btn.config(bg='light gray') # Make sure submit button is grayed out

        # Print to console
        print("Successfully performed undo operation.")

        trimatic.suspend_progress()

    # Prompts user for next point, updates display
    def indicateNextPoint():

        print("Please Indicate coordinate.")
        frame.current_num = frame.current_num + 1
        print(frame.points_array)

        # Prompt user to indicate coordinates, Store coordinates, Update display with coordinates.
        numDecimals = 3
        if (frame.isEntry1Filled == False):
            frame.points_array[0] = trimatic.indicate_coordinate()
            frame.points_array_display[0] = [round(frame.points_array[0][0], numDecimals), round(frame.points_array[0][1], numDecimals), round(frame.points_array[0][2], numDecimals)]
            
            # Saves new num for undo.
            prevNumArr.append(pointEntry1_var.get())
            prevEntryArr.append(pointEntry1)

            pointEntry1.delete(0, "end") # Clear textbox
            pointEntry1.insert(0, frame.points_array_display[0]) # Populate textbox w/new coord.

            frame.isEntry1Filled = True

            undo_btn.config(bg='PaleTurquoise1')

            checkForSubmit()

        elif (frame.isEntry2Filled == False):
            frame.points_array[1] = trimatic.indicate_coordinate()
            frame.points_array_display[1] = [round(frame.points_array[1][0], numDecimals), round(frame.points_array[1][1], numDecimals), round(frame.points_array[1][2], numDecimals)]

            # Saves new num for undo.
            prevNumArr.append(pointEntry2_var.get())
            prevEntryArr.append(pointEntry2)

            pointEntry2.delete(0, "end")
            pointEntry2.insert(0, frame.points_array_display[1])

            frame.isEntry2Filled = True

            checkForSubmit()

        elif (frame.isEntry3Filled == False):
            frame.points_array[2] = trimatic.indicate_coordinate()
            frame.points_array_display[2] = [round(frame.points_array[2][0], numDecimals), round(frame.points_array[2][1], numDecimals), round(frame.points_array[2][2], numDecimals)]

            # Saves new num for undo.
            prevNumArr.append(pointEntry3_var.get())
            prevEntryArr.append(pointEntry3)

            pointEntry3.delete(0, "end")
            pointEntry3.insert(0, frame.points_array_display[2])

            frame.isEntry3Filled = True

            checkForSubmit()

        updateWindowTitle()
        print(frame.points_array)

        trimatic.suspend_progress()

    def isArrayOfNums(entryText):
        # Check if string will split into 3
        splitArr = entryText.split()

        if len(splitArr) != 3:
            return False

        # Check if each index is a float
        for str in splitArr:
            try:
                float(str)
            except:
                return False
            
        return True
        
    def attemptSaveEntry1(event):
        if event.keysym == 'Return':
            print("Enter/Return was pressed.")
        else:
            return

        if isArrayOfNums(pointEntry1_var.get()) == False:
            print("Point 1 has an incorrect amount of coordinates. Each point requires 3 coordinates separated by spaces (X Y Z).")
            return
        
        splitArr = pointEntry1_var.get().split()
        floatArr = []
        for str in splitArr:
            floatArr.append(float(str))
            
        frame.points_array[0] = [floatArr[0], floatArr[1], floatArr[2]]
        frame.points_array_display[0] = frame.points_array[0]

        frame.isEntry1Filled = True

        checkForSubmit()

        undo_btn.config(bg='PaleTurquoise1')

        prevNumArr.append(frame.updatedNumEntry1)
        frame.updatedNumEntry1 = pointEntry1_var.get()

        prevEntryArr.append(pointEntry1)

        updateWindowTitle()

        print("Successfully saved point 1.")

    def attemptSaveEntry2(event):
        if event.keysym == 'Return':
            print("Enter/Return was pressed.")
        else:
            return

        if isArrayOfNums(pointEntry2_var.get()) == False:
            print("Point 2 has an incorrect amount of coordinates. Each point requires 3 coordinates separated by spaces (X Y Z).")
            return
        
        splitArr = pointEntry2_var.get().split()
        floatArr = []
        for str in splitArr:
            floatArr.append(float(str))
            
        frame.points_array[1] = [floatArr[0], floatArr[1], floatArr[2]]
        frame.points_array_display[1] = frame.points_array[1]

        frame.isEntry2Filled = True

        checkForSubmit()

        undo_btn.config(bg='PaleTurquoise1')

        prevNumArr.append(frame.updatedNumEntry2)
        frame.updatedNumEntry2 = pointEntry2_var.get()

        prevEntryArr.append(pointEntry2)

        updateWindowTitle()
        
        print("Successfully saved point 2.")    

    def attemptSaveEntry3(event):
        if event.keysym == 'Return':
            print("Enter/Return was pressed.")
        else:
            return

        if isArrayOfNums(pointEntry3_var.get()) == False:
            print("Point 3 has an incorrect amount of coordinates. Each point requires 3 coordinates separated by spaces (X Y Z).")
            return
        

        splitArr = pointEntry1_var.get().split()
        floatArr = []
        for str in splitArr:
            floatArr.append(float(str))
            
        frame.points_array[2] = [floatArr[0], floatArr[1], floatArr[2]]
        frame.points_array_display[2] = frame.points_array[2]

        frame.isEntry3Filled = True

        checkForSubmit()

        undo_btn.config(bg='PaleTurquoise1')

        prevNumArr.append(frame.updatedNumEntry3)
        frame.updatedNumEntry3 = pointEntry3_var.get()

        prevEntryArr.append(pointEntry3)

        updateWindowTitle()
        
        print("Successfully saved point 3.")

    def checkForSubmit():
        if frame.isEntry1Filled and frame.isEntry2Filled and frame.isEntry3Filled:
            sub_btn.config(bg='lime green') # Make submit button green

            # If a plane already exists, delete it.
            if frame.previewPlaneExists == True:
                DeleteTrimaticEntity(frame.plane) # Only delete when a plane already exists, reduce errors.
                print("Preview plane deleted.")
                frame.previewPlaneExists = False

            # Create preview plane
            frame.plane = CreateTrimaticPlane(frame.points_array)

            # Rename preview plane
            global global_numCutPlanes
            global_numCutPlanes = global_numCutPlanes + 1
            frame.plane.name = "MagnetWizard_CutPlane_" + str(global_numCutPlanes)

            frame.previewPlaneExists = True
            print("Preview plane created.")

            # Set global variable here instead of submit b/c need
            # to check for plane before submission in AskForCutPlane().
            global globalCutPlane
            globalCutPlane = frame.plane
    
    def getNumFilledEntries():
        boolArr = [frame.isEntry1Filled, frame.isEntry2Filled, frame.isEntry3Filled]
        numTrue = boolArr.count(True)

        return numTrue

    # Updates titles depending on how many entries are filled.
    def updateWindowTitle():
        # Get number of filled entries.
        boolArr = [frame.isEntry1Filled, frame.isEntry2Filled, frame.isEntry3Filled]
        numTrue = boolArr.count(True)

        # Now update title.
        if numTrue == 0:    
            insert = "First"
            undo_btn.config(bg='light gray')
        elif numTrue == 1:  insert = "Second"
        elif numTrue == 2:  insert = "Third"
        else: 
            pointNumLabel.config(text = "Finished Selecting Points")
            return

        pointNumLabel.config(text = "Indicate " + insert + " Point")
        return
    
    def on_hotkey_enter(event):
        checkForSubmit()
        submit()

    # Initialize Labels and Buttons
    pointNumLabel = tk.Label(top_frame, text = "Indicate First Point", font=('Arial', 12, 'bold'))
    subtitle_label = tk.Label(top_frame, text = "Select three points to indicate the fixed plane.", font=('Arial', 10, 'italic'))

    pointLabel1 = tk.Label(middle_frame, text = "Point 1: ", font=('Arial', 10))
    pointLabel2 = tk.Label(middle_frame, text = "Point 2: ", font=('Arial', 10))
    pointLabel3 = tk.Label(middle_frame, text = "Point 3: ", font=('Arial', 10))

    pointEntry1 = tk.Entry(middle_frame, textvariable=pointEntry1_var, font=('Arial', 10), width=25)
    pointEntry2 = tk.Entry(middle_frame, textvariable=pointEntry2_var, font=('Arial', 10), width=25)
    pointEntry3 = tk.Entry(middle_frame, textvariable=pointEntry3_var, font=('Arial', 10), width=25)

    indicateNext_btn = tk.Button(bottom_frame, text = 'Indicate Point [i]', command = indicateNextPoint, background = 'gold2', width=15)
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2', width=15)
    undo_btn = tk.Button(bottom_frame, text = "Undo [U]", command=undo, background = 'light gray', width=15)
    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'light gray', width=15)

    # Set Locations on Grid
    pointNumLabel.grid(row=0)
    subtitle_label.grid(row=1, padx=5)

    pointLabel1.grid(row=0, column=0)
    pointLabel2.grid(row=1, column=0)
    pointLabel3.grid(row=2, column=0)

    pointEntry1.grid(row=0, column=1)
    pointEntry2.grid(row=1, column=1)
    pointEntry3.grid(row=2, column=1)

    indicateNext_btn.grid(row=0, column=0, padx=20, pady=5)
    undo_btn.grid(row=0, column=1)
    sub_btn.grid(row=1, column=0)
    quit_btn.grid(row=1, column=1)

    # Bind actions
    pointEntry1.bind('<KeyPress>', attemptSaveEntry1)
    pointEntry2.bind('<KeyPress>', attemptSaveEntry2)
    pointEntry3.bind('<KeyPress>', attemptSaveEntry3)

    """ 
    """
    def on_hotkey_i(event):
        print("hotkey i clicked")
        indicateNextPoint()

        """ 
    """
    
    """
    """
    def on_hotkey_u(event):
        print("hotkey u clicked")
        undo()

    root.bind("i", on_hotkey_i)
    root.bind("I", on_hotkey_i)
    root.bind("u", on_hotkey_u)
    root.bind("U", on_hotkey_u)

    root.bind('<Return>', on_hotkey_enter)

    root.protocol("WM_DELETE_WINDOW", quit)

    # Clicking escape to cancel this operation throws a RuntimeError. 
    # Print this instead to not scare user.
    print("You can cancel escape to cancel operation.")
    try:
        indicateNextPoint() # Run immediately
    except RuntimeError:
        print("Cancelled indication.")

    frame.mainloop()

""" Creates UI in subframe 'frame' of root. User selects a plane from the 3-Matic object tree.
    | param root : Tkinter window
    | param frame: subframe of root
    |
    | return: globalCutPlane
    | rtype : global Trimatic Plane
"""
def AskForFixedPlaneObjectTree(root,frame):
    trimatic.suspend_progress()

    frame.submittable = False
    frame.object = None

    # Frames
    top_frame = Frame(frame)
    top_frame.grid(row=0)

    middle_frame = Frame(frame)
    middle_frame.grid(row=1)

    bottom_frame = Frame(frame)
    bottom_frame.grid(row=2)

    frame.objectTuple = []

    def submit():
        if not frame.submittable:
            print("Unable to submit.")
            return
        
        global globalCutPlane
        globalCutPlane = frame.object

        NextMainWindow(root)
    
    def quit():
        ExitWizard(root)

    def selectFromObjectTree():
        frame.objectTuple = trimatic.get_selection() # obj is a tuple
        
        print(frame.objectTuple)

        checkForSubmit(frame.objectTuple)

        return

    def checkForSubmit(objectTuple):
        if len(objectTuple) <= 0:
            print("Please select a plane in the object tree.")
            return
        elif len(objectTuple) > 1:
            print("Please select one object at a time.")
            return

        planeList = trimatic.get_planes()
        if objectTuple[0] in planeList:
            frame.submittable = True
            frame.object = objectTuple[0]
        else:
            frame.submittable = False

        updateButtonColors()
        updateLabel()
        return
    
    def updateButtonColors():
        if frame.submittable:
            sub_btn.config(bg="lime green")
        else:
            sub_btn.config(bg="light gray")

        return
    
    def updateLabel():
        if frame.submittable:
            plane_name_label.config(text= frame.object.name)
        else:
            plane_name_label.config(text= "Invalid Object")
        return
    
    def on_hotkey_enter(event):
        selectFromObjectTree()
        checkForSubmit(frame.objectTuple)
        submit()

    # Labels & Buttons
    title_label = tk.Label(top_frame, text = 'Select A Plane', font=('Arial', 12, 'bold'))
    subtitle_label = tk.Label(top_frame, text = 'Select your fixed plane from the object tree.', font=('Arial', 10, 'italic'))

    plane_name_label = tk.Label(middle_frame, text = 'Awaiting Object Selection...')
    select_object_btn = tk.Button(middle_frame, text = 'Select Object', command = selectFromObjectTree, bg='cornflower blue', width=15)
    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'light gray', width=15)
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2', width=15)

    # Locations
    title_label.grid(row=0)
    subtitle_label.grid(row=1)

    plane_name_label.grid(row=0)
    select_object_btn.grid(row=1)

    sub_btn.grid(row=0, column=0, padx=10, pady=10)
    quit_btn.grid(row=0, column=1, padx=10)

    root.bind('<Return>', on_hotkey_enter)

    root.protocol("WM_DELETE_WINDOW", quit)

    return

""" Creates Tkinter Window. User selects up to two parts to subtract the current magnet from.
    | param entitiesToExclude: array of trimatic.part
    | param currentMagent:     trimatic.part
    | param sizeAndMagNumArr:  array of string and int
    | 
    | return: global_currentMagnet
    | rtype : global trimatic.part
"""
def AskForSubtractionEntities(entitiesToExclude, currentMagnet, sizeAndMagNumArr):
    # Set up window for input.
    winSubtract = tk.Tk()
    winSubtract.title('Magnet Wizard')
    winSubtract.attributes('-topmost', True)
    # winSubtract.focus_set() # Focuses on window.
    winSubtract.geometry(f"300x280+{global_prevWindowX}+{global_prevWindowY}")
    winSubtract.resizable(False, False)


    [currSize, currNum, totalNum] = sizeAndMagNumArr

    # MENU BUTTON
    menubutton_frame = Frame(winSubtract)
    menubutton_frame.grid(row=0)
    
    top_frame = Frame(winSubtract, width=300, height=40)
    top_frame.grid(row=1)
    middle_frame = Frame(winSubtract, width=300, height=40)
    middle_frame.grid(row=2, pady=10)
    bottom_frame = Frame(winSubtract, width=300, height=40)
    bottom_frame.grid(row=3)

    bottom_skip_frame = Frame(winSubtract)
    bottom_skip_frame.grid(row=4)

    winSubtract.undoable = False
    winSubtract.submittable = False
    winSubtract.is1Valid2Empty = False
    winSubtract.is2Valid1Empty = False

    winSubtract.partNamesList = []

    winSubtract.currentMagnet = currentMagnet
    winSubtract.currentMagnetName = currentMagnet.name

    winSubtract.prevEntity1Name = ""
    winSubtract.prevEntity2Name = ""

    actionList = [] # save actions for undo
    numSubtractionList = [] # pairs with actionList[]

    def submit():
        if not winSubtract.submittable:
            print("Unable to submit.")
            return
        
        subtractCommand(winSubtract.currentMagnet)
        NextMainWindow(winSubtract)
       
    def quit():
        ExitWizard(winSubtract)

    def skip(): 
        global entityName
        entityName = NONE # Signifies a skip        
        NextMainWindow(winSubtract)

    def subtractCommand(currMagnet):
        if not winSubtract.submittable:
            print("Unable to subtract.")
            return
        
        entity1Name = entityNameComboBox1.get()
        entity2Name = entityNameComboBox2.get()

        # Check subtraction cases.
        if winSubtract.is1Valid2Empty or (entity1Name == entity2Name):
            # Only subtract from entity 1
            entity1 = trimatic.find_part(entity1Name)
            subtractEntityList = Subtract(entity1, currMagnet)
            duplicateMagnet         = subtractEntityList[2]
            logSubtraction(subtractEntityList)
            numSubtractionList.append(1)
        elif winSubtract.is2Valid1Empty:
            # Only subtract from entity 2
            entity2 = trimatic.find_part(entity2Name)
            subtractEntityList = Subtract(entity2, currMagnet)
            duplicateMagnet         = subtractEntityList[2]
            logSubtraction(subtractEntityList)
            numSubtractionList.append(1)
        else:
            # Subtract from both entities
            entity1 = trimatic.find_part(entity1Name)
            entity2 = trimatic.find_part(entity2Name)

            # Subtract via duplicates
            subtractEntityList = Subtract(entity1, currMagnet)
            duplicateMagnet         = subtractEntityList[2]
            logSubtraction(subtractEntityList)

            subtractEntityList = Subtract(entity2, duplicateMagnet)
            duplicateMagnet         = subtractEntityList[2]
            logSubtraction(subtractEntityList)

            numSubtractionList.append(2)
    
        winSubtract.currentMagnet = duplicateMagnet
        print(f"duplicateMagnet: {winSubtract.currentMagnet}")

        global global_currentMagnet
        global_currentMagnet = duplicateMagnet # Global magnet for moving objects.

        # Update partNamesList
        updateCombobox()

        sub_btn.config(bg='light gray')
        subtract_btn.config(bg='light gray')

        winSubtract.submittable = False
        winSubtract.undoable = True
        undo_btn.config(bg='PaleTurquoise1')

        return
         
    def undo():
        if not winSubtract.undoable or len(actionList) <= 0:
            print("Unable to undo.")
            return
        
        numSubtracts = numSubtractionList.pop()

        for x in range(0,numSubtracts):
            subtractedPart  = actionList[len(actionList)-1][0]
            duplicatePartName   = actionList[len(actionList)-1][1]

            # delete subtracted part
            trimatic.delete(subtractedPart)

            duplicateMagnet = winSubtract.currentMagnet

            duplicatePart = trimatic.find_part(duplicatePartName)

            # remove duplicate from end of duplicated magnet
            try:
                duplicatePart.name = duplicatePart.name.removesuffix("_duplicate")
            except:
                print("Could not change name of duplicate part. No errors, carry on.")
            
            # remove duplicate from end of duplicated part
            try:
                duplicateMagnet.name = duplicateMagnet.name.removesuffix("_duplicate")
            except:
                print("Could not change name of duplicate magnet. No errors, carry on.")
            
            winSubtract.currentMagnet = duplicateMagnet

            global global_currentMagnet
            global_currentMagnet = duplicateMagnet
            
            actionList.pop()

        if len(actionList) <= 0:
            undo_btn.config(bg='light gray')
                
        updateCombobox()
        checkForSubmit(NONE)

        return
    
    def checkForSubmit(event):
        print(f"current magnet name: {winSubtract.currentMagnet.name}")

        isEntity1Valid = False
        isEntity2Valid = False
        winSubtract.submittable = False
        winSubtract.is1Valid2Empty = False
        winSubtract.is2Valid1Empty = False

        # allPartNameList = trimatic.get_parts()

        # Check if each dropdown has a valid entity.
        if winSubtract.prevEntity1Name in winSubtract.partNamesList:
            entity1 = trimatic.find_part(winSubtract.prevEntity1Name)
            entity1.transparency = 0.0
            winSubtract.prevEntity1Name = ""
        if entityNameComboBox1.get() in winSubtract.partNamesList:
            entity1 = trimatic.find_part(entityNameComboBox1.get())
            winSubtract.prevEntity1Name = entityNameComboBox1.get()
            entity1.transparency = 0.25
            isEntity1Valid = True

        if winSubtract.prevEntity2Name in winSubtract.partNamesList:
            entity2 = trimatic.find_part(winSubtract.prevEntity2Name)
            entity2.transparency = 0.0
            winSubtract.prevEntity2Name = ""
        if entityNameComboBox2.get() in winSubtract.partNamesList:
            entity2 = trimatic.find_part(entityNameComboBox2.get())
            winSubtract.prevEntity2Name = entityNameComboBox2.get()
            entity2.transparency = 0.25
            isEntity2Valid = True


        # Check if at least one dropdown has a valid entity 
        # AND the other has nothing in it.
        if isEntity1Valid and isEntity2Valid:
            winSubtract.submittable = True
        elif isEntity1Valid and entityNameComboBox2.get() == "":
            winSubtract.submittable = True
            winSubtract.is1Valid2Empty = True
        elif isEntity2Valid and entityNameComboBox1.get() == "":
            winSubtract.submittable = True
            winSubtract.is2Valid1Empty = True
        
        # Update UI
        if winSubtract.submittable == True:
            sub_btn.config(bg='lime green') # Make submit button green
            subtract_btn.config(bg='OliveDrab1')
            print("Selected plane is valid.")
        else: 
            sub_btn.config(bg='light gray') # Make submit button green
            subtract_btn.config(bg='light gray')
            print("Selected plane is not valid.")
        return

    def on_combobox_input(event):
        winSubtract.after(1, checkForSubmit(event))

        return

    def on_subtractbtn():
        winSubtract.after(1, subtractCommand(winSubtract.currentMagnet))
        return

    """
    """
    def updateCombobox():
        # Part Frame Items
        partList = trimatic.get_parts()
        print(partList)

        winSubtract.partNamesList = []
        # Adds part names to combobox dropdown
        for x in range(0, len(partList)):
            print(partList[x])
            print(winSubtract.currentMagnet)
            if partList[x] != winSubtract.currentMagnet:
                if partList[x] not in entitiesToExclude: # Only shows non-magnet/housing entities.
                    winSubtract.partNamesList.append(partList[x].name)
        entityNameComboBox1['values'] = winSubtract.partNamesList
        entityNameComboBox2['values'] = winSubtract.partNamesList
        return

    """
    """
    def logSubtraction(subtractEntityList):
        subtractedPart  = subtractEntityList[0]
        duplicatePartName   = subtractEntityList[1].name
        duplicateMagnet = subtractEntityList[2]

        actionList.append([subtractedPart, duplicatePartName, duplicateMagnet])
        return
  
    def selectFromObjectTree():
        objectTuple = trimatic.get_selection()

        if len(objectTuple) <= 0:
            print("Please select a plane in the object tree.")
            return
        
        print(objectTuple)

        validPartList = []
        
        for x in range(0, len(objectTuple)):
            if len(validPartList) == 2:
                break

            currentObject = objectTuple[x]

            if currentObject.name in winSubtract.partNamesList:
                # if currentObject != winSubtract.currentMagnet:
                validPartList.append(currentObject)

        if len(validPartList) <= 0:
            print("No valid objects were selected.")
            return
        
        # Update variables and UI
        entityNameVarArr = [entityName_var1, entityName_var2]

        for entityNameVar in entityNameVarArr:
            for validPart in validPartList:
                if entityNameVar.get() == validPart.name:
                    entityNameVarArr.remove(entityNameVar)
                    validPartList.remove(validPart)

        for x in range(0, len(validPartList)):
            entityNameVarArr[x].set(validPartList[x].name)

        checkForSubmit(None)
        
        return

    def on_hotkey_enter(event):
        checkForSubmit(event)
        submit()

    # Labels, Entries, and Buttons
    SetupMenubuttons(winSubtract)

    title_label = tk.Label(top_frame, text = "Subtraction", font=('Arial', 12, 'bold'))
    subtitle_label = tk.Label(top_frame, text = f"Select which part you would like to subtract from.\n{currSize} {currNum}/{totalNum}", font=('Arial', 10, 'italic'))
    # subtractingEntity_label = tk.Label(middle_frame, text = 'Subtracting\nEntity', font=('Arial', 10, 'bold'))
    # spacer = tk.Label(middle_frame, text="")
    prompt_label1 = tk.Label(middle_frame, text = 'Subtract From:', font=('Arial', 10, 'bold'))
    prompt_label2 = tk.Label(middle_frame, text = 'Subtract From:', font=('Arial', 10, 'bold'))

        # Create ComboBox
    # subtractingEntity_var1 = tk.StringVar()
    # subtractingEntityCombobox = ttk.Combobox(middle_frame, width = 27, textvariable=subtractingEntity_var1)

    entityName_var1 = tk.StringVar()
    entityNameComboBox1 = ttk.Combobox(middle_frame, width = 27, textvariable = entityName_var1)

    entityName_var2 = tk.StringVar()
    entityNameComboBox2 = ttk.Combobox(middle_frame, width = 27, textvariable = entityName_var2)
        # Dropdown Values
    partList = trimatic.get_parts()
    # print(f"partList: {partList} | currentMagnet: {currentMagnet} | entitiesToExclude: {entitiesToExclude}")
    print(partList)
    print(currentMagnet)
    print(entitiesToExclude)
    winSubtract.partNamesList = []
        # This loop simplifies names to be displayed.
    for x in range(0, len(partList)):
        if partList[x] != currentMagnet:
            if partList[x] not in entitiesToExclude: # Only shows non-magnet/housing entities.
                winSubtract.partNamesList.append(partList[x].name)
    entityNameComboBox1['values'] = winSubtract.partNamesList
    entityNameComboBox2['values'] = winSubtract.partNamesList

    subtract_btn = tk.Button(bottom_frame, text = 'Subtract', command=on_subtractbtn, background = 'light gray', width=15)
    undo_btn = tk.Button(bottom_frame, text = "Undo", command=undo, background = 'light gray', width=15)
    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'light gray', width=15)
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2', width=15)
    selectObjects_btn = tk.Button(bottom_skip_frame, text = 'Select Objects', command = selectFromObjectTree, bg='cornflower blue', width=15)
    skip_btn = tk.Button(bottom_skip_frame, text = 'Skip →', command = skip, background = 'goldenrod2')

    # Setting Locations
    title_label.grid(row=0)
    subtitle_label.grid(row=1)

    # subtractingEntity_label.grid(row=0, column=0)
    # subtractingEntityCombobox.grid(row=0, column=1)

    # spacer.grid(row=1)

    prompt_label1.grid(row=2, column=0)
    entityNameComboBox1.grid(row=2, column=1)
    prompt_label2.grid(row=3, column=0)
    entityNameComboBox2.grid(row=3, column=1)

    subtract_btn.grid(row=0, column=0)
    undo_btn.grid(row=0, column=1)
    sub_btn.grid(row=1, column=0, padx=20, pady=5)
    quit_btn.grid(row=1, column=1)

    selectObjects_btn.grid(row=0, pady=5)
    skip_btn.grid(row=1)

    entityNameComboBox1.bind('<KeyRelease>', on_combobox_input)
    entityNameComboBox1.bind('<ButtonRelease>', on_combobox_input)
    entityNameComboBox1.bind('<<ComboboxSelected>>', on_combobox_input)
    entityNameComboBox1.bind('<<MouseWheel>>', on_combobox_input)
    entityNameComboBox1.bind('<<FocusIn>>', on_combobox_input)


    entityNameComboBox2.bind('<KeyRelease>', on_combobox_input)
    entityNameComboBox2.bind('<ButtonRelease>', on_combobox_input)
    entityNameComboBox2.bind('<<ComboboxSelected>>', on_combobox_input)
    entityNameComboBox2.bind('<<MouseWheel>>', on_combobox_input)
    entityNameComboBox2.bind('<<FocusIn>>', on_combobox_input)

    winSubtract.bind('<Return>', on_hotkey_enter)

    winSubtract.protocol("WM_DELETE_WINDOW", quit)

    # Loop until closed
    winSubtract.mainloop()
    return

""" Creates Tkinter Window. User can boolean union any existing housings to any part.
    | param housingList: array of trimatic.part - housings
"""
def AskForHousingUnions(housingList):
    trimatic.suspend_progress()

    winUnion = tk.Tk()
    winUnion.title('Magnet Wizard')
    winUnion.attributes('-topmost', True)
    winUnion.geometry(f"390x360+{global_prevWindowX}+{global_prevWindowY}")
    winUnion.resizable(False, False)

    # MENU BUTTON
    menubutton_frame = Frame(winUnion)
    menubutton_frame.grid(row=0)
    
    # Top Frame
    top_frame = Frame(winUnion)
    top_frame.grid(row=1)

    # Middle Frame
    middle_frame = Frame(winUnion)
    middle_frame.grid(row=2, pady=15)

    # Housings Select Frame
    housing_select_canvas = Canvas(middle_frame, height=120, width=120)
    housing_select_canvas.grid(row=0, column=0, padx=15)

    inner_housing_select_frame = Frame(housing_select_canvas)
    inner_housing_select_frame.pack()

    # scrollbar = tk.Scrollbar(inner_housing_select_frame, orient=tk.VERTICAL, command=housing_select_canvas.yview)
    # scrollbar.grid(sticky="e")

    housing_select_canvas.create_window((0,0), window=inner_housing_select_frame, anchor="nw")
    
    housing_select_title_frame = Frame(inner_housing_select_frame, height=15)
    housing_select_title_frame.grid(row=0)

    # housing_select_canvas.configure(yscrollcommand=scrollbar.set)

    housing_select_checkbuttons_frame = Frame(inner_housing_select_frame, height=100)
    housing_select_checkbuttons_frame.grid(row=1)

    # Part Select Frame
    part_select_frame = Frame(middle_frame)
    part_select_frame.grid(row=0, column=1, padx=15)

    part_select_title_frame = Frame(part_select_frame)
    part_select_title_frame.grid(row=0)

    part_select_dropdown_frame = Frame(part_select_frame)
    part_select_dropdown_frame.grid(row=1)

    # Bottom (button) frame
    buttons_frame = Frame(winUnion)
    buttons_frame.grid(row=3)

    # Top of Buttons frame
    buttons_union_frame = Frame(buttons_frame)
    buttons_union_frame.grid(row=0)

    # Bottom of Buttons frame
    buttons_skip_frame = Frame(buttons_frame)
    buttons_skip_frame.grid(row=1)

    winUnion.submittable = False
    winUnion.undoable = False
    winUnion.isAnyCheckboxSelected = False
    winUnion.isComboboxSubmittable = False
    winUnion.selectedHousings = []
    winUnion.checkbuttonVarList = []
    winUnion.partNamesList = []

    winUnion.isMoveObjectMenuOpen = False
    winUnion.globalCurrentHousingSetNames = []

    winUnion.prevPartName = ""

    global entitiesToExclude

    winUnion.actionList = []

    # Commands
    """ Combines each selected housing to the selected part.
    """
    def union():
        # Checks if all the submission booleans are True.
        # if not (winUnion.isAnyCheckboxSelected or winUnion.submittable or winUnion.isComboboxSubmittable):
        if not winUnion.submittable:
            print("Unable to union.")
            updateButtonColors()
            return
        # BACKUP CHECK - accounts for bug in combobox check
        elif part_combobox_var.get() not in winUnion.partNamesList:
            print("Unable to union.")
            updateButtonColors()
            return

        # Print to console
        print("Attempting to Union: ")
        for housing in winUnion.selectedHousings:
            print("\t" + housing.name + "\n")
        print("To: " + part_combobox_var.get())

        # Find part to combine
        combiningPart = trimatic.find_part(part_combobox_var.get())

        # Remove selected housing from global current housing set if selected
        if global_currentHousingSet != None:
            for housing in winUnion.selectedHousings:
                if housing in global_currentHousingSet:
                    global_currentHousingSet.remove(housing)

        # Remove selected housings from housingList
        for housing in winUnion.selectedHousings:
            housing.transparency = 0.0
            housingList.remove(housing)
            entitiesToExclude.remove(housing)

        unionEntitiesList = UnionHousingToPart(winUnion.selectedHousings, combiningPart)
        logUnion(unionEntitiesList)

        print("Successfully combined all parts.")

        # Update conditional variables.
        winUnion.submittable = False
        winUnion.undoable = True

        # Update entites to exclude
        duplicateHousingList = unionEntitiesList[2]
        for duplicateHousing in duplicateHousingList:
            entitiesToExclude.append(duplicateHousing)

        # Update UI and Lists
        updateCheckboxesAndList()
        updateCombobox()
        updateButtonColors()
        checkForSubmit(NONE)
        resetTransparencies()

        # It seems that there should be a winUnion.selectedHousings = [] here
        # I am unsure if this is safe without it.
        return

    def submit():
        if not winUnion.submittable:
            print("Unable to submit.")
            return

        union()
        NextMainWindow(winUnion)
        return
    
    def quit():
        ExitWizard(winUnion)
    
    def undo():
        global global_currentHousingSet
        if not winUnion.undoable:
            print("Unable to undo.")
            return
        
        recentAction = winUnion.actionList.pop()

        unionedEntity             = recentAction[0]
        duplicateNonUnionedEntityName = recentAction[1]
        duplicateHousingList      = recentAction[2]

        # Undo error when union twice to same part and undo twice on that part. 
        # The previous actionlog does not get updated properly to know that the previous item no longer exists.
        # Loop backwards through 

        DeleteTrimaticEntity(unionedEntity)
        
        print(duplicateNonUnionedEntityName)
        print(duplicateHousingList)
        duplicateNonUnionedEntity = trimatic.find_part(duplicateNonUnionedEntityName)
        
        # Delete unioned entity.
        # trimatic.delete(unionedEntity)

        # Remove suffixes from duplicates.
        try:
            duplicateNonUnionedEntity.name = duplicateNonUnionedEntity.name.removesuffix("_duplicate")

        except:
            print("Could not change name of duplicateNonUnionedEntity. No errors, carry on.")

        for duplicateHousing in duplicateHousingList:
            try:
                duplicateHousing.name = duplicateHousing.name.removesuffix("_duplicate")
                housingList.append(duplicateHousing)
                # Add housing back to currentHousingSet if it's brought back.
                global_currentHousingSet.append(duplicateHousing)
            except:
                print("Could not change name of duplicateHousing. No errors, carry on.")

        if len(winUnion.actionList) <= 0:
            winUnion.undoable = False
            undo_btn.config(bg="light gray")

        # # Testing: Update nonunioned duplicated entity after union
        # for entityIndex in nonUnionedEntityIndicesToUpdate:
        #     winUnion.actionList[entityIndex][1] = duplicateNonUnionedEntity

        winUnion.isAnyCheckboxSelected = False
        updateCheckboxesAndList()
        updateCombobox()
        updateButtonColors()
        checkForSubmit(NONE)

        return

    def skip():
        resetTransparencies()
        NextMainWindow(winUnion)
    
    def checkForSubmit(event):
        
        winUnion.isComboboxSubmittable = False

        # Combobox Check
        if winUnion.prevPartName in winUnion.partNamesList:
            entity = trimatic.find_part(winUnion.prevPartName)
            entity.transparency = 0.0
            winUnion.prevPartName = ""
        if part_combobox.get() in winUnion.partNamesList:
            entity = trimatic.find_part(part_combobox.get())
            winUnion.prevPartName = part_combobox.get()
            entity.transparency = 0.25
            winUnion.isComboboxSubmittable = True

        # Checkbox Check
        # if event == NONE: # Only run when a checkbox is toggled. Reduce load.
        count = 0
        currentNum = 0
        winUnion.selectedHousings = []
        for checkbuttonVar in winUnion.checkbuttonVarList:

            currentHousing = housingList[currentNum]

            # If a checkbutton is on
            if checkbuttonVar.get() == 1:
                winUnion.isAnyCheckboxSelected = True
                count = count + 1
                winUnion.selectedHousings.append(currentHousing)
                print("winUnion appended " + currentHousing.name)
                currentHousing.transparency = 0.25
                print("Checkbutton selected")

            else:
                currentHousing.transparency = 0.0
                
            currentNum = currentNum + 1
            
        # Check if no checkboxes are selected
        if count == 0: 
            winUnion.isAnyCheckboxSelected = False


        # CHECK FOR SUBMIT
        if (winUnion.isAnyCheckboxSelected and winUnion.isComboboxSubmittable):
            winUnion.submittable = True
        else: 
            winUnion.submittable = False

        updateButtonColors()

        return
            
    def on_combobox_input(event):
        winUnion.after(1, checkForSubmit(event))
        return

    def on_checkbox_toggled():
        winUnion.after(1, checkForSubmit(NONE))
        return

    """
    """
    def updateCheckboxesAndList():

        # Destroy old checkboxes
        for checkbox in housing_select_checkbuttons_frame.winfo_children():
            checkbox.destroy()

        winUnion.checkbuttonVarList.clear()
        # Create new checkboxes
        for housing in housingList:
            currentHousing = housing

            # Give each housing the var attribute
            currentHousing.checkbutton_var = tk.IntVar()

            # Can find each button from the housings too
            currentHousing.checkbutton = Checkbutton(housing_select_checkbuttons_frame, text=housing.name, variable=currentHousing.checkbutton_var, onvalue=1, offvalue=0, command=on_checkbox_toggled).grid()

            currentHousing.checkbutton_var.set(0)
            
            # Store each button to a list for checking later
            winUnion.checkbuttonVarList.append(currentHousing.checkbutton_var)
        return

    """
    """
    def updateCombobox():
        # Part Frame Items
        partList = trimatic.get_parts()
        winUnion.partNamesList = []
        # Adds part names to combobox dropdown
        for x in range(0, len(partList)):
                winUnion.partNamesList.append(partList[x].name)
        part_combobox['values'] = winUnion.partNamesList

    def updateButtonColors():
        if winUnion.submittable:
            sub_btn.config(bg='lime green')
            union_btn.config(bg='MediumPurple2')
            print("Selected part is valid.")
        else:
            sub_btn.config(bg='light gray')
            union_btn.config(bg='light gray')
            print("Selected part is not valid.")

        if len(winUnion.actionList) > 0:
            winUnion.undoable = True
            undo_btn.config(bg='PaleTurquoise1')
        else:
            winUnion.undoable = False
            undo_btn.config(bg="light gray")
        return
    
    def on_frame_configure(event):
        housing_select_canvas.configure(scrollregion=housing_select_canvas.bbox("all"))

    def on_mouse_wheel(event):
        housing_select_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def logUnion(unionEntitiesList):
        unionedEntity                 = unionEntitiesList[0]
        duplicateNonUnionedEntityName = unionEntitiesList[1].name
        duplicateHousingList          = unionEntitiesList[2]

        winUnion.actionList.append([unionedEntity, duplicateNonUnionedEntityName, duplicateHousingList])
        print("logging union:")
        print(f"\t{unionEntitiesList}")
        return

    def selectFromObjectTree():
        objectTuple = trimatic.get_selection() # obj is a tuple

        if len(objectTuple) <= 0:
            print("Please select a plane in the object tree.")
            return
        
        print(objectTuple)
        
        allPartsList = trimatic.get_parts()

        for x in range(0, len(objectTuple)):
            currentObject = objectTuple[x]

            # Checks if housing, then if just a part.
            if currentObject in housingList:
                # select this housing
                print("Housing " + currentObject.name + " has been selected.")
                # Apply checkmark properly to housing.

                # Find matching housing from checklist that was selected
                currentNum = 0
                for checkbuttonVar in winUnion.checkbuttonVarList:

                    if housingList[currentNum] == currentObject:

                        # Select checkbox if not already selected
                        if checkbuttonVar.get() == 0:
                            checkbuttonVar.set(1) # update it to be selected
                    
                    currentNum = currentNum + 1

                on_checkbox_toggled()
                
                # Store them properly.
                winUnion.selectedHousings.append(currentObject)

            elif currentObject in allPartsList:
                # select this part
                print("Part " + currentObject.name + " has been selected.")
                # Update variables to store this object. 


                # Update combobox text field.
                part_combobox_var.set(currentObject.name)

        checkForSubmit(NONE)
        return

    def on_hotkey_enter(event):
        # checkForSubmit2(NONE)
        submit()
        
    def resetTransparencies():
        part = trimatic.find_part(part_combobox_var.get())

        if part is not None: part.transparency = 0.0

        for x in range(0, len(winUnion.selectedHousings)):
            winUnion.selectedHousings[x].transparency = 0.0

        return
    
    # Initialize Labels and Buttons
    SetupMenubuttons(winUnion)

    # Top Frame Items
    title_label = tk.Label(top_frame, text = "Union Housings to Part", font=('Arial', 14, 'bold'))
    subtitle_label = tk.Label(top_frame, text = "Select housings & part. Click Union.", font=('Arial', 12, 'italic'))
    
    # Housing Frame Items
    housing_title_label = tk.Label(housing_select_title_frame, text = "Housings", font=('Arial', 12, 'bold'))
    housing_subtitle_label = tk.Label(housing_select_title_frame, text = "Select below.", font=('Arial', 10, 'italic'))

    # Set locations of titles before checkboxes to avoid bugs
    housing_title_label.grid(row=0)
    housing_subtitle_label.grid(row=1)

    # Create a checkbox for each existing housing
    winUnion.checkbuttonList = []
    for housing in housingList:
        # What attributes does each housing need to have?

        currentHousing = housing

        # Give each housing the var attribute
        currentHousing.checkbutton_var = tk.IntVar()

        # Can find each button from the housings too
        currentHousing.checkbutton = Checkbutton(housing_select_checkbuttons_frame, text=housing.name, variable=currentHousing.checkbutton_var, onvalue=1, offvalue=0, command=on_checkbox_toggled).grid()

        # Store each button to a list for checking later
        winUnion.checkbuttonVarList.append(currentHousing.checkbutton_var)
    
    part_title_label = tk.Label(part_select_title_frame, text = "Part", font=('Arial', 12, 'bold'))
    part_subtitle_label = tk.Label(part_select_title_frame, text = "Select below.", font=('Arial', 10, 'italic'))

    part_combobox_var = tk.StringVar()
    part_combobox = ttk.Combobox(part_select_dropdown_frame, textvariable=part_combobox_var, width=30)

    updateCombobox()

    # Set locations of part labels
    part_title_label.grid(row=0)
    part_subtitle_label.grid(row=1)
    part_combobox.grid(row=0)

    # Bottom Frame Items
    union_btn = tk.Button(buttons_union_frame, text = 'Union', command = union, background = 'light gray', width=15)
    quit_btn = tk.Button(buttons_union_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2', width=15)
    undo_btn = tk.Button(buttons_union_frame, text = "Undo", command=undo, background = 'light gray', width=15)
    sub_btn = tk.Button(buttons_union_frame, text = 'Submit', command = submit, background = 'light gray', width=15)

    selectObjects_btn = tk.Button(buttons_skip_frame, text = 'Select Objects', command = selectFromObjectTree, bg='cornflower blue', width=15)
    skip_btn = tk.Button(buttons_skip_frame, text = 'Skip →', command = skip, background = 'goldenrod2')

    # Set Locations on Grid
    title_label.grid(row=0)
    subtitle_label.grid(row=1, padx=5)

    union_btn.grid(row=0, column=0)
    undo_btn.grid(row=0, column=1)
    sub_btn.grid(row=1, column=0, padx=20, pady=5)
    quit_btn.grid(row=1, column=1)

    selectObjects_btn.grid(row=0, pady=5)
    skip_btn.grid(row=1)

    # Bind inputs for selection
    part_combobox.bind('<KeyRelease>', on_combobox_input)
    part_combobox.bind('<ButtonRelease>', on_combobox_input)
    part_combobox.bind('<<ComboboxSelected>>', on_combobox_input)
    part_combobox.bind('<<FocusIn>>', on_combobox_input)
    part_combobox.bind('<<MouseScroll>>', on_combobox_input)

    housing_select_canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    inner_housing_select_frame.bind("<Configure>", on_frame_configure)

    winUnion.bind('<Return>', on_hotkey_enter)

    winUnion.protocol("WM_DELETE_WINDOW", quit)
    
    if global_currentHousingSet != None:
        winUnion.globalCurrentHousingSetNames = [global_currentHousingSet[0].name, global_currentHousingSet[1].name]

    winUnion.mainloop()
    
    return

""" Asks user to select 3 points for the fixed plane. Aligns magnet to fixed plane.
    | param magnet     : trimatic.part
    | param planeMoving: trimatic.plane
    |
    | return: planeArray
    | rtype : array of trimatic.plane
"""
def PromptUserPlanesMagnet(magnet, planeMoving):
    trimatic.suspend_progress()

    # Fixed Entity Plane
    print("Selecting Points for Fixed Entity's Plane:")

    # Ask user to select 3 points.
    #IndicatePointsPopup()

    AskForCutPlane() # Testing

    if global_skip_alignment == True: # This means that the alignment was skipped.
        print("Plane alignment step skipped.")
        return

    planeFixed = globalCutPlane
    
    print("Successfully created Plane on Fixed Entity!")

    # Now get entity to move along. This will move the magnet to the aligned plane.
    trimatic.plane_to_plane_align(planeFixed, planeMoving, magnet)

    # Store both planes in an array to return.
    planeArray = [planeFixed, planeMoving]
    return planeArray

""" Asks user to select 3 points for the fixed plane. Aligns magnet and housings to fixed plane.
    | param magnet     : trimatic.part
    | param planeMoving: trimatic.plane
    | param housingA   : trimatic.part
    | param housingB   : trimatic.part
    |
    | return: planeArray
    | rtype : array of trimatic.plane
"""
def PromptUserPlanesMagnetAndHousing(magnet, planeMoving, housingA, housingB):
    trimatic.suspend_progress()

    # Fixed Entity Plane
    print("Selecting Points for Fixed Entity's Plane:")

    # Ask user to select 3 points.
    AskForCutPlane()

    if global_skip_alignment == True: # This means that the alignment was skipped.
        print("Plane alignment step skipped.")
        return

    planeFixed = globalCutPlane

    print("Successfully created Plane on Fixed Entity!")

    # Now get entity to move along. This will move the magnet to the aligned plane.
    trimatic.plane_to_plane_align(planeFixed, planeMoving, [magnet, housingA, housingB])

    # Store both planes in an array to return.
    planeArray = [planeFixed, planeMoving]
    return planeArray

""" Subtracts one entity from another. Catches errors if they occur.
    | param entity            : trimatic.part
    | param subtracting_entity: trimatic.part
    | 
    | return: entityList
    | rtype : array of trimatic.part
    | return: newEntity
    | rtype : trimatic.part
    | return: duplicate
    | rtype : trimatic.part
"""
def Subtract(entity, subtracting_entity):
    try: 
        print("Duplicating entities before subtraction...")
        
        print("Duplicating subtracted entity.")
        duplicateEntity            = trimatic.duplicate(entity)
        print("Duplicating subtracting entity.")
        duplicateSubtractingEntity = trimatic.duplicate(subtracting_entity) # this is the magnet
        print("Attempting to subtract...")
        newEntity = trimatic.boolean_subtraction(entity, subtracting_entity)

        subtractEntityList = [newEntity, duplicateEntity, duplicateSubtractingEntity]
        
        return subtractEntityList

    except ValueError:
        print("[VALUE ERROR] Could not subtract " + subtracting_entity.name + " from " + entity.name + ".")
    except RuntimeError:
        print("[RUNTIME ERROR] Could not subtract " + subtracting_entity.name + " from " + entity.name + ".")
    except:
        print("[ERROR] Could not subtract " + subtracting_entity.name + " from " + entity.name + ".")
    return

""" Combines all the entities within the provided array.
    | param combining_entities: array of trimatic.part
    | 
    | return: newEntity
    | rtype : trimatic.part
"""
def Union(combining_entities):
    try:
        print("Attempting to union...")
        newEntity = trimatic.boolean_union(combining_entities)
        return newEntity
    except ValueError:
        print("[VALUE ERROR]")
    except RuntimeError:
        print("[RUNTIME ERROR]")
    except:
        print("[ERROR]")
    return

""" Imports magnets of the specified size. Imports housings if specified.
    | param currNum: int
    | param size   : str
    | param housing: boolean
    | 
    | If housing:
    | return: magnet
    | rtype : trimatic.part
    | 
    | If NOT housing:
    | return: partsArray
    | rtype : array of trimatic.part
"""
def ImportMagnetAndHousing(currNum, size, housing):
    if size == "Mini":
        magnetFile   = magnetMini
        housingFileA = magnetMiniHousingA
        housingFileB = magnetMiniHousingB
    elif size == "Small":
        magnetFile   = magnetSmall
        housingFileA = magnetSmallHousingA
        housingFileB = magnetSmallHousingB
    elif size == "Medium":
        magnetFile   = magnetMedium
        housingFileA = magnetMediumHousingA
        housingFileB = magnetMediumHousingB
    else: # Size must be Large
        magnetFile   = magnetLarge
        housingFileA = magnetLargeHousingA
        housingFileB = magnetLargeHousingB

    magnet = trimatic.import_part_stl(magnetFile)
    magnet.name = magnet.name + "_" + str(currNum+1)
    print("Imported " + size + " Magnet #" + str(currNum+1))

    # Import another whole magnet to test for subtraction fix.

    if housing == True: # Import Housings & Rename
        housingA = trimatic.trimatic.import_part_stl(housingFileA)
        housingA.name = housingA.name + "_" + str(currNum+1)
        print("Imported " + size + " Housing A #" + str(currNum+1))

        housingB = trimatic.trimatic.import_part_stl(housingFileB)
        housingB.name = housingB.name + "_" + str(currNum+1)
        print("Imported " + size + " Housing B #" + str(currNum+1))
    
    if housing == True: # Return array if housing is needed.
        partsArray = [magnet, housingA, housingB]
        return partsArray
    else:               # Return only magnet if there is no housing.
        return magnet

""" Creates a new named center-plane based on the magnet size and returns the plane.
    | param size  : string
    | param num   : int
    | 
    | return: ___MagnetCenterPlane1
    | rtype : trimatic.plane
"""
def CreateCenterPlane(size, num):
    # Depending on the size, puts plane in different spot.
    if size == "Mini":
        miniMagnetCutPlane1 = trimatic.create_plane_normal_origin(miniNormalVector, miniOrigin) # Create plane from coordinates (global variables)
        miniMagnetCutPlane1.name = "Mini Magnet Center Plane_" + str(num) + "-1"                   # Rename planes
        return miniMagnetCutPlane1                                                              # Return cut plane.
    elif size == "Small":
        smallMagnetCutPlane1 = trimatic.create_plane_normal_origin(smallNormalVector, smallOrigin)
        smallMagnetCutPlane1.name = "Small Magnet Center Plane_" + str(num) + "-1"
        return smallMagnetCutPlane1
    elif size == "Medium":
        mediumMagnetCutPlane1 = trimatic.create_plane_normal_origin(mediumNormalVector, mediumOrigin)
        mediumMagnetCutPlane1.name = "Medium Magnet Center Plane_" + str(num) + "-1"
        return mediumMagnetCutPlane1
    else: # Size must be Large
        largeMagnetCutPlane1 = trimatic.create_plane_normal_origin(largeNormalVector, largeOrigin)
        largeMagnetCutPlane1.name = "Medium Magnet Center Plane_" + str(num) + "-1"
        return largeMagnetCutPlane1
    return

""" Checks if any entities exist in the 3-matic file.
    | return: boolean
"""
def HasEntities():
    if not trimatic.get_parts():
        print("No entities exist. Magnet Wizard could not start.")
        return False
    return True

""" Asks for and returns a user-specified 3-matic entity.
    | param entitiesToExclude: array of trimatic.part
    |
    | return: entity
    | rtype : trimatic.part
"""
def PromptUserSubtraction(entitiesToExclude, currentMagnet):
    trimatic.suspend_progress()

    AskForSubtractionEntities(entitiesToExclude, currentMagnet)    # Get Entity Name

    if entityName == NONE:
        return [NONE, True]
    else: 
        entityName_local = entityName
    
    print("Entity found: " + entityName_local)        # Testing

    entity = trimatic.find_part(entityName_local)     # Find entity from name.
    return [entity, False]

""" Combines magnet housings to specified 3-matic part.
    | param housingPartA: trimatic.part
    | param housingPartB: trimatic.part
    | 
    | return: newEntity
    | rtype : trimatic.part
"""
def UnionHousingToPart(housings, entity):
    print("in UnionHousingToPart")
    print(housings)

    # Establish entity's name for renaming and saving duplicate part.
    entityName = entity.name

    # Duplicate Part and save.
    print("Duplicating " + entity.name + " before union...")
    duplicateEntity = trimatic.duplicate(entity)

    # Duplicate housings and save them.
    duplicateHousingList = []
    for housing in housings:
        print("Duplicating " + housing.name + " before union...")
        duplicateHousing = trimatic.duplicate(housing)
        duplicateHousingList.append(duplicateHousing) 

    # Array of entities to union
    combining_entities = []
    for housing in housings:                # Append each housing
        combining_entities.append(housing)
    combining_entities.append(entity)       # Append the part

    newEntity = Union(combining_entities)

    newEntity.name = entityName + "_UnionResult"

    duplicateEntity = trimatic.find_part(entityName + "_duplicate")
    unionEntityList = [newEntity, duplicateEntity, duplicateHousingList]

    return unionEntityList

""" Prompts user to select a fixed plane. Aligns necessary parts to it. Contains boolean logic.
    | param housing   : boolean
    | param entityList: array of trimatic.part
"""
def SelectFixedPlaneAndAlign(housing, entitiesToAlign):

    # Decide with method to use based on housing.
    if housing == True:
        # trimatic.suspend_progress()
        magnet = entitiesToAlign[0]
        planeMoving = entitiesToAlign[1]
        housingA = entitiesToAlign[2]
        housingB = entitiesToAlign[3]

        PromptUserPlanesMagnetAndHousing(magnet, planeMoving, housingA, housingB)
    else:
        # trimatic.suspend_progress()
        magnet = entitiesToAlign[0]
        planeMoving = entitiesToAlign[1]
        PromptUserPlanesMagnet(magnet, planeMoving)

    return

""" Imports the desired magnet and returns the lists of entities needed to continue the program.
    | param housing    : boolean
    | param magNum     : int
    | param currentSize: string
    | 
    | return: [entitiesToExclude, entitiesToAlign, housings, currentMagnet]
    | rtype : array of arrays (except currentMagnet)
    | 
    | return: entitiesToExclude
    | rtype : array of trimatic.part
    | 
    | return: entitiesToAlign
    | rtype : array of trimatic.part
    | 
    | return: housings
    | rtype : array of trimatic.part
    | 
    | return: currentMagnet
    | rtype : trimatic.part
"""
def ImportAndReturnEntities(housing, magNum, currentSize):

    global global_currentHousingSet
    # global_currentHousingSet = None
    global_currentHousingSet = []

    global global_currentMagnet
    global_currentMagnet = None

    global global_currentRunNum

    entitiesToExclude = []
    entitiesToAlign = []
    housings = []

    # Create group if not exists
    if trimatic.find_group("Magnet Wizard") is None:
        CreateGroup("Magnet Wizard", None, None)

    magnetWizard_parentFolder = trimatic.find_group("Magnet Wizard")

    # see if this group already exists
    currentSetGroup = CreateGroup(f"{currentSize} Set {magNum+1}.{global_currentRunNum}", None, magnetWizard_parentFolder)

    # Import correct magnet and housing
    if housing == True:
        currentPartsArray = ImportMagnetAndHousing(magNum, currentSize, housing)
        currentMagnet   = currentPartsArray[0]
        currentHousingA = currentPartsArray[1]
        currentHousingB = currentPartsArray[2]

        AddObjectsToGroup(currentSetGroup, currentPartsArray)
                
        entitiesToExclude.append(currentHousingA) # Store current housings for exclusion.
        entitiesToExclude.append(currentHousingB)

        # Global magnets & housings
        global_currentHousingSet = [currentHousingA, currentHousingB]
        global_currentMagnet     = currentMagnet
    else:
        currentMagnet = ImportMagnetAndHousing(magNum, currentSize, housing)

        AddObjectsToGroup(currentSetGroup, currentMagnet)

        # Global magnets & housings
        global_currentHousingSet = None
        global_currentMagnet     = currentMagnet
    
    # Get new center plane
    currentCenterPlane = CreateCenterPlane(currentSize, magNum+1)

    AddObjectsToGroup(currentSetGroup, currentCenterPlane)
            
    # entitiesToExclude.append(currentMagnet)

    # Select plane and align parts.
    if housing == True:
        entitiesToAlign = [currentMagnet, currentCenterPlane, currentHousingA, currentHousingB]
        housings = [currentHousingA, currentHousingB]   # Fill housings array if necessary.
    else:
        entitiesToAlign = [currentMagnet, currentCenterPlane]

    return [entitiesToExclude, entitiesToAlign, housings, currentMagnet]

""" Creates a plane in 3-Matic based on an array of 3 points.
    | param pointsArry : array of float
    | 
    | return: planeFixed
    | rtype : trimatic.plane
"""
def CreateTrimaticPlane(pointsArr):

    # Store coordinates.
    [p1, p2, p3] = pointsArr

    planeFixed = trimatic.analyze.create_plane_3_points(p1, p2, p3)

    return planeFixed

""" Deletes a given trimatic entity within 3-Matic.
    | param entity: trimatic.entity
"""
def DeleteTrimaticEntity(entity):
    trimatic.delete(entity)
    return

""" Updates window coordinates, and closes any extra windows that are tied to the current main window.
"""
def NextMainWindow(root):
    UpdateWindowSpawnCoords(root)
    CloseMoveObjectWindow()
    CloseInfoWindow()
    root.destroy()
    return

""" Exits the program by safely closing all windows that are open. 
"""
def ExitWizard(root):
    CloseMoveObjectWindow()
    CloseInfoWindow()
    CloseBugWindow()
    root.destroy()
    exit()
    return

""" Updates global spawn coordinates for each main window to open at the same coords as the previous window.
"""
def UpdateWindowSpawnCoords(root):
    global global_prevWindowX, global_prevWindowY
    print(f"prevX from {global_prevWindowX} to {root.winfo_x()}")
    global_prevWindowX = root.winfo_x()
    print(f"prevX from {global_prevWindowY} to {root.winfo_y()}")
    global_prevWindowY = root.winfo_y()
    return

""" Saves project. Overwrites the current file.
"""
def SaveProject():
    # Try saving file.
    print("Attempting to save file...")
    try:
        trimatic.file.save_project(None)    # Specifying None saves the file with the same name.
        print("Successfully saved file.")
    except ValueError:
        print("[ERROR] ValueError occured. Unable to save file")
    except RuntimeError:
        print("[ERROR] RuntimeError occured. Unable to save file")
    except:
        print("Unable to save file for some reason.")
    return

""" Creates Tkinter Window. Allow user to move objects in 3-Matic within the program.
"""
def AskForObjectsToMove(mainWindow):
    trimatic.suspend_progress()

    # Must be global to be closed from outside of this method.
    global winMoveObj
    global isWinMoveObjOpen
    global global_currentHousingSet, global_currentMagnet

    winMoveObj = tk.Tk()
    winMoveObj.title('Magnet Wizard')
    winMoveObj.attributes('-topmost', True)
    width = 360
    height = 220
    # winMoveObj.geometry(str(width) + "x" + str(height))
    winMoveObj.geometry(f"360x220+{mainWindow.winfo_x() + mainWindow.winfo_width() + 10}+{mainWindow.winfo_y()}") # width x height
    winMoveObj.resizable(False, False)

    # Frames
    top_frame = Frame(winMoveObj)
    top_frame.grid(row=0)

    middle_frame = Frame(winMoveObj)
    middle_frame.grid(row=1)

    bottom_frame = Frame(winMoveObj)
    bottom_frame.grid(row=2)

    def closeMenu():
        global isWinMoveObjOpen
        isWinMoveObjOpen = False

        winMoveObj.destroy()
        return
    
    def showWarningPopup():
        print("Displaying warning message")
        messagebox.showwarning("Info Popup", "Windows will be hidden. Do not panic.\nClicking 'Escape' will end this operation and bring the windows back.\n\nClick Ok to proceed.")

    def selectObjectsToMove():
        
        objectTuple = trimatic.get_selection()

        if len(objectTuple) <= 0:
            print("Please select at least one object to move.")
            return

        print("Allowing objects to move.")

        showWarningPopup()
        hideWindows()

        # Allows user to move selected objects.
        if len(objectTuple) == 1:
            trimatic.activate_translate_rotate(objectTuple[0])
        else:
            mainEntity = objectTuple[0]
            moveAlongEntities = objectTuple[1:]
            trimatic.activate_translate_rotate(mainEntity, moveAlongEntities)

        showWindows()
        return
    
    def selectCurrentMagnetAndHousings():
        global global_currentHousingSet
        global global_currentMagnet

        housingExists = False
        if global_currentHousingSet is not None: housingExists = True
        magnetExists = False
        if global_currentMagnet is not None: magnetExists = True

        if housingExists and magnetExists:
            print("Allowing current magnet and housing(s) to be moved.")
            showWarningPopup()
            hideWindows()
            trimatic.activate_translate_rotate(global_currentMagnet, global_currentHousingSet)
            showWindows()
        elif magnetExists and not housingExists:
            showWarningPopup()
            hideWindows()
            print("Only a magnet exists, allowing current magnet to be moved.")
            trimatic.activate_translate_rotate(global_currentMagnet)
            showWindows()
        elif housingExists and not magnetExists:
            showWarningPopup()
            hideWindows()
            print("Only housing(s) exists, allowing current housing(s) to be moved.")
            trimatic.activate_translate_rotate(global_currentHousingSet)
            showWindows()
        else:
            print("No magnets or housings exist. Unable to perform operation.")
            currentMagAndHousings_btn.config(bg='light gray')

        return
    
    def hideWindows():
        # Send windows back.
        winMoveObj.lower()
        mainWindow.lower()
        return
    
    def showWindows():
        # Bring windows to front.
        mainWindow.attributes('-topmost', True)
        mainWindow.lift()
        winMoveObj.attributes('-topmost', True)
        winMoveObj.lift()
        return
    
    # Initialize Labels and Buttons
    
    # Labels & Buttons
    title_label = tk.Label(top_frame, text = 'Move Objects', font=('Arial', 12, 'bold'))
    subtitle_label1 = tk.Label(top_frame, text = 'Select objects from object tree or within 3-Matic environment.\nThen click \'Select Objects\' to allow translation & rotation.\nYou must click the \'Escape\' key to stop moving objects.', font=('Arial', 10, 'italic'))

    warning_label = tk.Label(top_frame, text='WARNING: Clicking in this window before \nclicking \'Escape\' may crash 3-Matic.', font=('Arial', 10), fg='red')

    selectObjects_btn = tk.Button(middle_frame, text = 'Select Objects', command = selectObjectsToMove, bg='cornflower blue', width=15)
    currentMagAndHousings_btn = tk.Button(middle_frame, text = 'Current Magnet\n& Housings', command = selectCurrentMagnetAndHousings, background = 'NavajoWhite2', width=15)
    closemenu_btn = tk.Button(bottom_frame, text = 'Close Menu', command = closeMenu, background = 'tan1', width=15)

    title_label.grid(row=0)
    subtitle_label1.grid(row=1)
    warning_label.grid(row=2, pady=10)

    selectObjects_btn.grid(row=0, column=0, padx=20, pady=5)

    currentMagAndHousings_btn.grid(row=0, column=1, padx=20, pady=5)

    closemenu_btn.grid(row=0)

    winMoveObj.mainloop()

    return

""" Attemps to close Move Object Window. This is used when closing every main window.
"""
def CloseMoveObjectWindow():
    try:
        winMoveObj.destroy()
    except:
        print("Unable to close the Move Object window.")
    return

""" Creates Tkinter Window. Displays information about the Magnet Wizard in a pop-up window.
    | param mainWindow: tkinter root
"""
def InfoWindow(mainWindow):
    global winInfo
    winInfo = tk.Tk()

    # Set Title
    winInfo.title('Info Menu')

    # Make Window Stay on Top
    winInfo.attributes('-topmost', True)

    # Sets geometry (width x height)
    winInfo.geometry("285x285")

    winInfo.resizable(False, False)

    top_frame = Frame(winInfo)
    top_frame.grid(row=0)

    middle_frame = Frame(winInfo)
    middle_frame.grid(row=1, padx=10)

    bottom_frame = Frame(winInfo)
    bottom_frame.grid(row=2)

    winInfo.windowNum = 0
    maximum = 7
    minimum = 0

    def closeMenu():
        global isInfoWindowOpen
        isInfoWindowOpen = False
        mainWindow.focus_set()
        winInfo.destroy()
        return
    
    def on_next_btn_clicked():
        winInfo.after(1, next())
        return
    
    def next():
        if winInfo.windowNum == maximum:
            winInfo.windowNum = minimum
        else:
            winInfo.windowNum = winInfo.windowNum + 1

        clearInfoFrame()
        # AnimateWindowGeometry(winInfo, 285, 385)
        updateInfoFrame()
        return
    
    def on_back_btn_clicked():
        winInfo.after(1, back())
        return
    
    def back():
        if winInfo.windowNum == minimum:
            winInfo.windowNum = maximum
        else:
            winInfo.windowNum = winInfo.windowNum - 1

        clearInfoFrame()
        updateInfoFrame()
        return
    
    def updateInfoFrame():
        # Update Page Number
        pageNum_label.config(text=f'Page {winInfo.windowNum + 1} / {maximum + 1}')

        # Change info
        if winInfo.windowNum == 0: InfoWindow_General(winInfo, middle_frame)
        if winInfo.windowNum == 1: InfoWindow_FilePath(winInfo, middle_frame)
        if winInfo.windowNum == 2: InfoWindow_Sizes(winInfo, middle_frame)
        if winInfo.windowNum == 3: InfoWindow_HousingOption(winInfo, middle_frame)
        if winInfo.windowNum == 4: InfoWindow_FixedPlane(winInfo, middle_frame)
        if winInfo.windowNum == 5: InfoWindow_UnionHousing(winInfo, middle_frame)
        if winInfo.windowNum == 6: InfoWindow_Subtraction(winInfo, middle_frame)
        if winInfo.windowNum == 7: InfoWindow_MoveObjects(winInfo, middle_frame)

        return
    
    def clearInfoFrame():
        for widget in middle_frame.winfo_children():
            widget.destroy()
        return
    
    def on_hotkey_left(event):
        winInfo.after(1, back())
        return
    
    def on_hotkey_right(event):
        winInfo.after(1, next())
        return
    
    # Initialize Labels and Buttons
    
    # Labels & Buttons
    title_label = tk.Label(top_frame, text = 'Info Menu', font=('Arial', 14, 'bold'))
    subtitle_label = tk.Label(top_frame, text = 'More information about Magnet Wizard.', font=('Arial', 12, 'italic'))
    spacer_label1 = tk.Label(top_frame, text="-------------------------")

    spacer_label2 = tk.Label(bottom_frame, text="-------------------------")
    pageNum_label = tk.Label(bottom_frame, text=f'Page {winInfo.windowNum + 1} / {maximum + 1}')
    closemenu_btn = tk.Button(bottom_frame, text = 'Close Menu', command = closeMenu, background = 'tan1', width=15)
    next_btn = tk.Button(bottom_frame, text = 'Next →', command = on_next_btn_clicked, background = 'khaki', width=7)
    back_btn = tk.Button(bottom_frame, text = '← Back', command = on_back_btn_clicked, background = 'khaki', width=7)

    title_label.grid(row=1)
    subtitle_label.grid(row=2)
    spacer_label1.grid(row=4)

    spacer_label2.grid(row=0, column=1)
    pageNum_label.grid(row=1, column=1)
    back_btn.grid(row=2, column=0)
    closemenu_btn.grid(row=2, column=1, padx=10, pady=5)
    next_btn.grid(row=2, column=2)

    # Testing hotkey. Delete upon release.
    # def on_hotkey_d(event):
    #     print(f"width: {winInfo.winfo_width()}")
    #     print(f"height: {winInfo.winfo_height()}")
    #     return
    
    # winInfo.bind("d", on_hotkey_d)
    # winInfo.bind("D", on_hotkey_d)

    # Move left hotkeys
    winInfo.bind("<Left>", on_hotkey_left)
    winInfo.bind("a", on_hotkey_left)
    winInfo.bind("A", on_hotkey_left)

    # Move right hotkeys
    winInfo.bind("<Right>", on_hotkey_right)
    winInfo.bind("d", on_hotkey_right)
    winInfo.bind("D", on_hotkey_right)

    winInfo.bind()

    updateInfoFrame()

    winInfo.mainloop()

    return

""" Attempts to close Info Window. This is used when closing every main window.
"""
def CloseInfoWindow():
    try:
        winInfo.destroy()
    except:
        print("Unable to close the Info window.")
    return

""" Creates UI in subframe 'frame' of root. Displays general information about the Magnet Wizard.
"""
def InfoWindow_General(root, frame):
    root.geometry("460x630")
    
    title_subframe = Frame(frame)
    title_subframe.grid(row=0)

    body_subframe = Frame(frame)
    body_subframe.grid(row=1, pady=5)

    title_label = tk.Label(title_subframe, text = 'General Info', font=('Arial', 12, 'bold'))

    generalButtonsText = (
        "General Buttons\n"
        "• Submit: Performs main action & moves to next window.\n"
        "• Skip: Skips to the next window.\n"
        "• Exit Wizard: Closes this program without saving progress.\n"
    )

    menuButtonsText = (
        "Menu Buttons\n"
        "• File:\n"
        "   - Save Project: Saves the 3-Matic project.\n"
        "   - Info: Brings up an info menu (this one).\n"
        "• Actions: \n"
        "   - Move Objects: Allows the user to move objects in 3-Matic\n"
        "                           without closing the Magnet Wizard.\n"
    )

    hotkeyText = (
        "Hotkeys (Some windows have their own)\n"
        "• General:\n"
        "   - Enter/Return: Another way to click submit in any window.\n"
        "   - Toggle Info Menu: F1\n"
        "   - Toggle Move Object Menu: F2\n"
        "• Info Menu:\n"
        "   - Left Arrow/A: Next hotkeys.\n"
        "   - Right Arrow/D: Back hotkeys.\n"
    )

    feedbackText = (
        "Feedback\n"
        "• To submit feedback, navigate to this script's folder in X.\n"
        "• Wihin the Feedback Reports folder, please create a text (.txt) file\n"
        "  following the template in Template.txt."
    )

    generalButtonsLabel = tk.Label(body_subframe, text=generalButtonsText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    menuButtonsLabel = tk.Label(body_subframe, text=menuButtonsText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    hotkeyLabel = tk.Label(body_subframe, text=hotkeyText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    feedbackLabel = tk.Label(body_subframe, text=feedbackText, font=('Arial', 10), justify=tk.LEFT, anchor="w")

    title_label.pack()

    generalButtonsLabel.pack(fill="x", anchor="w")
    menuButtonsLabel.pack(fill="x", anchor="w")
    hotkeyLabel.pack(fill="x", anchor="w")
    feedbackLabel.pack(fill="x", anchor="w")

    frame.mainloop()

    return

""" Creates UI in subframe 'frame' of root. Displays information about the File Path window.
"""
def InfoWindow_FilePath(root, frame):
    root.geometry("430x545")

    title_subframe = Frame(frame)
    title_subframe.grid(row=0)

    body_subframe = Frame(frame)
    body_subframe.grid(row=1,pady=5)

    title_label = tk.Label(title_subframe, text = 'File Path', font=('Arial', 12, 'bold'))

    filePathRequirementsText = (
        "File Path Requirements\n"
        "• Valid File Path: Must be X file path or\n"
        "                         any subpath that leads to X\n"
        "• Restructuring: If the layout of X is restructured,\n"
        "                        the file paths in the program will need to be changed.\n"
        "• Trailing Periods: Trailing periods are not counted because it's \n"
        "                           impossible for files or folders to end with periods.\n"
    )

    howitworksText = (
        "How It Works\n"
        "• Preset Paths: Four preset file paths from the \n"
        "                       X are tried first.\n"
        "• User Input: If no preset paths work, the user will be\n"
        "                   prompted to input their X file path.\n"
        "• Saving Path: Once a valid file path is found, it's\n"
        "                     saved to a text file if not already saved.\n"
    )

    manualPathEntryText = (
        "Save File\n"
        "• File Location: This PC > Windows System Drive > \n"
        "                       3Matic_ScriptSaveFiles > MagnetWizard_SaveFile.txt\n"
        "• Manual Path Entry: To manually add file paths to this text file,\n"
        "                               type one file path on each line."
    )

    filePathReqLabel = tk.Label(body_subframe, text=filePathRequirementsText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    howitworksLabel = tk.Label(body_subframe, text=howitworksText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    manualPathEntryLabel = tk.Label(body_subframe, text=manualPathEntryText, font=('Arial', 10), justify=tk.LEFT, anchor="w")

    title_label.pack()

    filePathReqLabel.pack(fill="x", anchor="w")
    howitworksLabel.pack(fill="x", anchor="w")
    manualPathEntryLabel.pack(fill="x", anchor="w")

    frame.mainloop()

    return

""" Creates UI in subframe 'frame' of root. Displays information about the Sizes selection window.
"""
def InfoWindow_Sizes(root, frame):
    root.geometry("290x345")

    title_subframe = Frame(frame)
    title_subframe.grid(row=0)

    body_subframe = Frame(frame)
    body_subframe.grid(row=1,pady=5)

    title_label = tk.Label(title_subframe, text = 'Magnet Sizes', font=('Arial', 12, 'bold'))

    sizesText = (
        "Sizes\n"
        "• Mini    : 3.20 x 1.58 [mm]\n"
        "• Small   : 6.35 x 1.59 [mm]\n"
        "• Medium  : 6.35 x 2.54 [mm]\n"
        "• Large   : 6.35 x 5.08 [mm]\n"
    )

    generalMagnetInfoText = (
        "Number of Magnets\n"
        "• Minimum: 0\n"
        "• Maximum: 999,999,999 (for each size)"
    )

    sizesLabel = tk.Label(body_subframe, text=sizesText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    generalMagnetInfoLabel = tk.Label(body_subframe, text=generalMagnetInfoText, font=('Arial', 10), justify=tk.LEFT, anchor="w")

    title_label.pack()

    sizesLabel.pack(fill="x", anchor="w")
    generalMagnetInfoLabel.pack(fill="x", anchor="w")

    frame.mainloop()

    return

""" Creates UI in subframe 'frame' of root. Displays information about the Housing Option window.
"""
def InfoWindow_HousingOption(root, frame):
    root.geometry("400x285")

    title_subframe = Frame(frame)
    title_subframe.grid(row=0)

    body_subframe = Frame(frame)
    body_subframe.grid(row=1,pady=5)

    title_label = tk.Label(title_subframe, text = 'Housing Option', font=('Arial', 12, 'bold'))

    backgroundText = (
        "Housing should be imported when a magnet is too large for the\n"
        "desired region OR if the desired region is weak/flimsy."
        )

    optionsText = (
        "Options\n"
        "• Yes: Imports a housing set matching the current magnet's size.\n"
        "• No: Continue without importing magnets."
    )

    backgroundLabel = tk.Label(body_subframe, text=backgroundText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    optionsLabel = tk.Label(body_subframe, text=optionsText, font=('Arial', 10), justify=tk.LEFT, anchor="w")

    title_label.pack()

    backgroundLabel.pack()
    optionsLabel.pack(fill="x", anchor="w")

    frame.mainloop()

    return

""" Creates UI in subframe 'frame' of root. Displays information about the Magnet Wizard.
"""
def InfoWindow_FixedPlane(root, frame):
    root.geometry("400x655")

    title_subframe = Frame(frame)
    title_subframe.grid(row=0)

    body_subframe = Frame(frame)
    body_subframe.grid(row=1,pady=5)

    title_label = tk.Label(title_subframe, text = 'Fixed Plane', font=('Arial', 12, 'bold'))

    backgroundText = (
    "Fixed planes align magnets and housings. This window lets users\n"
    "align the magnet set's midplane to the selected fixed plane.\n"
    "Fixed planes are also called cut planes if used to cut entities.\n"
    )

    dropdownText = (
    "Dropdown\n"
    "• Select a plane from a dropdown of existing planes.\n"
    "• You can also type the plane's name into the dropdown.\n"
    )

    manualText = (
    "Manual\n"
    "• Prompts the user to select a point in the 3-Matic Work Area.\n"
    "   ('Escape' exits the task. (NOT CURRENTLY))\n"
    "• Creates a plane with 3 points, either typed manually or indicated.\n"
    "• The plane is previewed after 3 valid points.\n"

    )

    objectTreeText = (
    "Object Tree\n"
    "• The fastest way to select a plane if you know its location.\n"
    "• First, select a plane in the Work Area or Object Tree.\n"
    "  Then, click the button to select objects.\n"
    )

    submitButtonText = (
    "Buttons\n"
    "• Submit:\n"
    "   - Aligns the magnet set to the selected plane\n"
    "     and moves to the next window.\n"
    "   - Turns green if the plane is valid.\n"
    "• Undo\n"
    "   - Turns blue when selectable.\n"
    "   - Undoes most recent point indication. Does not undo typing."
    )

    backgroundLabel = tk.Label(body_subframe, text=backgroundText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    dropdownLabel = tk.Label(body_subframe, text=dropdownText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    manualLabel = tk.Label(body_subframe, text=manualText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    objectTreeLabel = tk.Label(body_subframe, text=objectTreeText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    submitButtonLabel = tk.Label(body_subframe, text=submitButtonText, font=('Arial', 10), justify=tk.LEFT, anchor="w")

    title_label.pack()

    backgroundLabel.pack()
    dropdownLabel.pack(fill="x", anchor="w")
    manualLabel.pack(fill="x", anchor="w")
    objectTreeLabel.pack(fill="x", anchor="w")
    submitButtonLabel.pack(fill="x", anchor="w")

    frame.mainloop()

    return

""" Creates UI in subframe 'frame' of root. Displays information about the Union Housing window.
"""
def InfoWindow_UnionHousing(root, frame):
    root.geometry("480x400")

    title_subframe = Frame(frame)
    title_subframe.grid(row=0)

    body_subframe = Frame(frame)
    body_subframe.grid(row=1,pady=5)

    title_label = tk.Label(title_subframe, text = 'Fixed Plane', font=('Arial', 12, 'bold'))

    housingsText = (
    "Housings\n"
    "• All current housings are listed on the left in the Housings section.\n"
    )

    partsText = (
    "Parts\n"
    "• All existing parts except housings are shown within the dropdown on the right.\n"
    )

    selectObjects = (
    "Select Objects\n"
    "• First, select at least one object from the object tree and/or the Work Area.\n"
    "• Only valid entities will be accepted. Valid entities include parts.\n"
    "• If a housing is selected, it will select them in the Housings section.\n"
    "• If a part is a selected, it will select that into the Part dropdown.\n"
    "• If multiple valid parts are selected, the last selected part will be used."
    )

    housingsLabel = tk.Label(body_subframe, text=housingsText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    partsLabel = tk.Label(body_subframe, text=partsText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    selectObjectsLabel = tk.Label(body_subframe, text=selectObjects, font=('Arial', 10), justify=tk.LEFT, anchor="w")

    title_label.pack()

    housingsLabel.pack(fill="x", anchor="w")
    partsLabel.pack(fill="x", anchor="w")
    selectObjectsLabel.pack(fill="x", anchor="w")

    frame.mainloop()

    return

""" Creates UI in subframe 'frame' of root. Displays information about the Subtraction window.
"""
def InfoWindow_Subtraction(root, frame):
    root.geometry("480x490")

    title_subframe = Frame(frame)
    title_subframe.grid(row=0)

    body_subframe = Frame(frame)
    body_subframe.grid(row=1,pady=5)

    title_label = tk.Label(title_subframe, text = 'Magnet Subtraction', font=('Arial', 12, 'bold'))

    backgroundText = (
        "Subtracting the magnet from a part is useful because\n"
        "it makes room for a magnet to be placed post-print.\n"
    )

    buttonsText = (
        "Buttons\n"
        "• Subtract\n"
        "   - Subtracts the curent magnet from up to two objects at a time.\n"
        "   - A duplicate magnet is created to use for continued subtractions.\n"
        "   - Housings and Magnets are invalid parts to select for this step.\n"
        "       > Magnet cannot subtract from itself.\n"
        "       > Magnets would not be subtracting from housings.\n"
        "• Undo\n"
        "   - Deletes duplicate objects created from subtraction.\n"
        "   - Undoes most recent subtraction operation\n"
        "• Submit\n"
        "   - Subtracts if possible.\n"
        "   - Moves to next window.\n"
        "   - Select Objects\n"
        "   - Select valid objects from the Object Tree or Work Area then click the button."
    )

    backgroundLabel = tk.Label(body_subframe, text=backgroundText, font=('Arial', 10), justify=tk.LEFT, anchor="w")
    buttonsLabel = tk.Label(body_subframe, text=buttonsText, font=('Arial', 10), justify=tk.LEFT, anchor="w")

    title_label.pack()

    backgroundLabel.pack()
    buttonsLabel.pack(fill="x", anchor="w")

    frame.mainloop()

    return

""" Creates UI in subframe 'frame' of root. Displays information about the Move Objects window.
"""
def InfoWindow_MoveObjects(root, frame):
    root.geometry("455x495")

    title_subframe = Frame(frame)
    title_subframe.grid(row=0)

    body_subframe = Frame(frame)
    body_subframe.grid(row=1,pady=5)

    title_label = tk.Label(title_subframe, text = 'Moving Objects', font=('Arial', 12, 'bold'))

    backgroundText = (
        "While using the program, some regular 3-Matic operations are not possible.\n"
        "This window allows the user to move any objects in 3-Matic.\n"
    )

    warningText = (
        "WARNING\n" 
        "1. When objects are selected to move, all Magnet Wizard windows\n"
        "   will be hidden & a warning messagebox will appear.\n"
        "2. The pop-up will warn you that clicking in any window before\n"
        "   clicking \'Escape\' will crash 3-Matic.\n"
        ""
    )

    buttonsText = (
        "Buttons\n"
        "• Select Objects\n"
        "   - Select the objects you would like to move.\n"
        "   - Then, click 'Select Objects'.\n"
        "• Current Magnet & Housings\n"
        "   - Selects the current magnet and housing set.\n"
        "   - Allows them to be moved in 3-Matic.\n"
        "• Close Menu\n"
        "   - Closes the menu."
    )

    backgroundLabel = tk.Label(body_subframe, text=backgroundText, font=('Arial', 10))
    warningLabel = tk.Label(body_subframe, text=warningText, font=('Arial', 10), fg='red')
    buttonsLabel = tk.Label(body_subframe, text=buttonsText, font=('Arial', 10), justify=tk.LEFT, anchor="w")

    title_label.pack()

    backgroundLabel.pack()
    warningLabel.pack()
    buttonsLabel.pack(fill="x", anchor="w")

    frame.mainloop()

    return

""" Creates Tkinter Window. Displays current known bugs from the feedback folder.
"""
def BugWindow(mainWindow):

    global winBug
    winBug = tk.Tk()

    # Set Title
    winBug.title('Bug Window')

    # Make Window Stay on Top
    winBug.attributes('-topmost', True)

    # Sets geometry (width x height)
    winBug.geometry("410x400")

    winBug.resizable(False, False)

    top_frame = Frame(winBug)
    top_frame.grid(row=0)

    middle_frame = Frame(winBug)
    middle_frame.grid(row=1, padx=10, sticky="nsew")

    bottom_frame = Frame(winBug)
    bottom_frame.grid(row=2)

    bug_window_canvas = Canvas(middle_frame)
    bug_window_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(middle_frame, orient="vertical", command=bug_window_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    inner_bug_window_canvas = Canvas(bug_window_canvas)
    inner_bug_window_canvas.pack()

    bug_window_canvas.create_window((0,0), window=inner_bug_window_canvas, anchor="nw")

    def closeMenu():
        global isBugWindowOpen
        isBugWindowOpen = False
        mainWindow.focus_set()
        winBug.destroy()
        return
    
    def parseFeedback():
        global filePath_global
        # If Feedback Reports Folder exists, open it

        # For every file that is not named Template.txt, parse it and add it to the list to print
        feedbackPath = filePath_global + r'\3. Technical\Scripting\Scripts\3-Matic\FLA\Magnet Wizard\Feedback Reports'

        spacerLine = "=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
        feedbackString = spacerLine + "\n"

        # If folder exists, parse text files
        if os.path.exists(feedbackPath):
            for file_name in os.listdir(feedbackPath):
                
                # Skip template file
                if file_name == "TemplateFeedback.txt":
                    continue

                # Filter only text files
                if file_name.endswith('.txt'):
                    file_path = os.path.join(feedbackPath, file_name)

                    with open(file_path, 'r') as file:

                        # Append each line to the return string
                        for line in file:
                            print(line)
                            feedbackString += line.strip() + "\n"
                        feedbackString += spacerLine + "\n"
        else:
            feedbackString = "No bugs have been found. The feedback folder was not found."

        return feedbackString
    
    def on_mouse_wheel(event):
        bug_window_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_frame_configure(event):
        bug_window_canvas.configure(scrollregion=bug_window_canvas.bbox("all"))
    
    # Initialize Labels and Buttons
    
    # Labels & Buttons
    title_label = tk.Label(top_frame, text = 'Bug List', font=('Arial', 14, 'bold'))
    subtitle_label = tk.Label(top_frame, text = 'Known Bugs', font=('Arial', 12, 'italic'))
    spacer_label1 = tk.Label(top_frame, text="-------------------------")

    feedbackText = parseFeedback()
    feedback_label = tk.Label(inner_bug_window_canvas, text=feedbackText, justify=tk.LEFT, anchor="w", wraplength=350)

    spacer_label2 = tk.Label(bottom_frame, text="-------------------------")
    closemenu_btn = tk.Button(bottom_frame, text = 'Close Menu', command = closeMenu, background = 'tan1', width=15)

    title_label.pack()
    subtitle_label.pack()
    spacer_label1.pack()

    feedback_label.pack()

    spacer_label2.pack()
    closemenu_btn.pack()

    bug_window_canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    inner_bug_window_canvas.bind("<Configure>", on_frame_configure)

    winBug.mainloop()

    return

""" Attempts to close Bug Window. This is used when closing every main window.
"""
def CloseBugWindow():
    try:
        winBug.destroy()
    except:
        print("Unable to close the Bug window.")
    return

""" Creates a group in the 3-Matic object tree to sort parts.
"""
def CreateGroup(groupName, entities, parent_group):

    # The trimatic command accounts for entities & parent_group being None.
    group = trimatic.create_group(groupName, entities, parent_group)

    return group

""" Adds entities to a 3-Matic group in the object tree.
"""
def AddObjectsToGroup(group, entities):

    if hasattr(entities, '__len__'):
        for x in range(0,len(entities)):
            group.add_items(entities[x])

    else:
        group.add_items(entities)

    return

""" Adds 'File' and 'Actions' menubuttons on a given Tkinter root window.
    | param root : Tkinter tk instance
    | 
    | return: menubuttonsArr
    | rtype : array of tk.Menubutton()
"""
def SetupMenubuttons(root):
    print("Setting up menubuttons.")
    global isWinMoveObjOpen
    isWinMoveObjOpen = False

    global isInfoWindowOpen
    isInfoWindowOpen = False
    
    global isBugWindowOpen
    isBugWindowOpen = False

    # Opens Move Object window if not already open.
    def attemptAskForObjectsToMove():
        global isWinMoveObjOpen
        
        if isWinMoveObjOpen:
            print("Move Object window is already open.")
            return
        else:
            isWinMoveObjOpen = True
            AskForObjectsToMove(root)
        return
    
    # Opens Info Window if not already open.
    def attemptInfoWindow():
        global isInfoWindowOpen
        
        if isInfoWindowOpen:
            print("Info window is already open.")
            return
        else:
            isInfoWindowOpen = True
            InfoWindow(root)
        return
    
    # Opens Bug Window if not already open.
    def attemptBugWindow():
        global isBugWindowOpen
        
        if isBugWindowOpen:
            print("Bug window is already open.")
            return
        else:
            isBugWindowOpen = True
            BugWindow(root)
        return
    
    def toggle_InfoWindow(event):
        global isInfoWindowOpen

        if isInfoWindowOpen: 
            isInfoWindowOpen = False
            #root.focus_set()
            winInfo.destroy()
        else:
            isInfoWindowOpen = True
            InfoWindow(root)
        return
    
    def toggle_BugWindow(event):
        global isBugWindowOpen

        if isBugWindowOpen: 
            isBugWindowOpen = False
            #root.focus_set()
            winBug.destroy()
        else:
            isBugWindowOpen = True
            BugWindow(root)
        return
    
    def toggle_MoveObjWindow(event):
        global isWinMoveObjOpen

        if isWinMoveObjOpen: 
            isWinMoveObjOpen = False
            # root.focus_set()
            winMoveObj.destroy()
        else:
            isWinMoveObjOpen = True
            AskForObjectsToMove(root)
        return

    file_btn = tk.Menubutton(root, text = "File", bg='light gray')
    file_btn.menu = Menu(file_btn, tearoff=0)
    file_btn["menu"] = file_btn.menu
    file_btn.grid(row=0, sticky="nw")
    file_btn.menu.add_command(label="Info", command=attemptInfoWindow)
    file_btn.menu.add_command(label="Save Project", command=SaveProject)
    file_btn.menu.add_command(label="Known Bugs", command=attemptBugWindow)

    root.bind("<F1>", toggle_InfoWindow)
    root.bind("<F3>", toggle_BugWindow)

    actions_menubtn = tk.Menubutton(root, text = "Actions", bg='light gray')
    actions_menubtn.menu = Menu(actions_menubtn, tearoff=0)
    actions_menubtn["menu"] = actions_menubtn.menu
    actions_menubtn.grid(row=0, sticky="ne")
    actions_menubtn.menu.add_command(label="Move Objects", command=attemptAskForObjectsToMove)

    root.bind("<F2>", toggle_MoveObjWindow)

    menubuttonsArr = [file_btn, actions_menubtn]

    return menubuttonsArr

""" Updates the ending of each magnet set folder name to align with a current run number.
    | return: global_currentRunNUm
    | rtype : global int
"""
def EstablishCurrentRunNum():
    global global_currentRunNum

    if trimatic.find_group("Magnet Wizard") is None:
        global_currentRunNum = 0
        return

    allGroupList = trimatic.get_groups()

    maxNum = 0
    # Loop through every group
    for group in allGroupList:
        groupName = group.name
        startsWithMiniSet   = groupName.startswith("Mini Set ")
        startsWithSmallSet  = groupName.startswith("Small Set ")
        startsWithMediumSet = groupName.startswith("Medium Set ")
        startsWithLargeSet  = groupName.startswith("Large Set ")

        # Check all magnet wizard
        if startsWithMiniSet or startsWithSmallSet or startsWithMediumSet or startsWithLargeSet:
            lastNum = int(groupName[-1])
            if lastNum == maxNum: maxNum += 1
            elif lastNum > maxNum: maxNum = lastNum

    global_currentRunNum = maxNum

    return

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-= MAIN =-=-=-=-=-=-=-=-=-=-=-=-=-=-=
""" Prompts user for necessary information at each step. Automatically adds magnets (and housing) to a user-selected point.
    =-=-=-=-=-=-=-=-=-=-= PSEUDOCODE =-=-=-=-=-=-=-=-=-=-=
    Import aorta for testing.
    Abort the script if no entities are present within the 3-Matic file.
    Check if the magnet files can be found. Ask user to specify file path if not.
    Ask the user how many magnets of each size they want.

    Loop for each size that exists:
        Loop for how many magnets the user wants in the current size:
            Ask the user if they want housing.
            Import the magnets (and housings if necessary).
            Ask the user to select three points on the plane they would like to align the magnets to.
            Move the magnets (and housings if necessary) to the desired plane.
            Ask the user which entity they would like to subtract from.
            Boolean union the housings to the entity.
            Boolean subtract the magnets from the entity.
    =-=-=-=-=-=-=-=-=-= END PSEUDOCODE =-=-=-=-=-=-=-=-=-=
"""
def main():
    # Wraps the code in a protective layer.
    try: 
        testing = False

        global filePath_global
        housingList = []

        # Assign some global variables
        global global_currentMagnet, global_currentHousingSet, global_currentRunNum
        global_currentRunNum     = 0
        global_currentMagnet     = None
        global_currentHousingSet = None

        EstablishCurrentRunNum()

        if not testing:
            if HasEntities() == False:
                print("There are no entities. Magnet Wizard Cannot Run")
                return

        InitializeFileVariables()

        if testing: ImportHeartModel(filePath_global) # For Testing

        global global_isMagnetImportSkipped
        global_isMagnetImportSkipped = False

        AskForSizeInput()

        # Print the returned sizes.
        print("Total Number of Magnets: " + str(magnetNumTotal))
        print("Number of Minis: " + str(magnetNumMini))
        print("Number of Smalls: " + str(magnetNumSmall))
        print("Number of Mediums: " + str(magnetNumMedium))
        print("Number of Larges: " + str(magnetNumLarge))

        # Store user input and sizes for use within the loop.
        sizeArray = ["Mini", "Small", "Medium", "Large"]
        numArray = [magnetNumMini, magnetNumSmall, magnetNumMedium, magnetNumLarge]

        # For each size type
        for s in range(0, len(sizeArray)):

            # For each set of magnets
            for m in range(0, numArray[s]):

                currentSize = sizeArray[s]
                currentNum  = m+1
                totalNum    = numArray[s]

                global sizeAndMagNumArr
                sizeAndMagNumArr = [currentSize, currentNum, totalNum] # Used for displaying in UI

                global entitiesToExclude
                entitiesToExclude = [] # Clear the variable.

                # Ask user for housing.
                AskForHousingInput(sizeArray[s], m+1, numArray[s])
                housing = magnetHousing

                # Import magnets and/or housings, returns all the necessary lists.
                [entitiesToExclude, entitiesToAlign, housings, currentMagnet] = ImportAndReturnEntities(housing, m, sizeArray[s])
                print("entitiesToExclude")
                print(entitiesToExclude)

                # Store housings from output.
                if housing == True:
                    currentHousingA     = housings[0]
                    currentHousingB     = housings[1]

                    # Save housings to housingList for union prompt @ end.
                    housingList.append(currentHousingA)
                    housingList.append(currentHousingB)
                else:
                    currentHousingA = None
                    currentHousingB = None
                
                SelectFixedPlaneAndAlign(housing, entitiesToAlign)

                if len(housingList) > 0:
                    AskForHousingUnions(housingList)
                
                #PromptUserSubtraction(entitiesToExclude, currentMagnet)
                print(entitiesToExclude)
                AskForSubtractionEntities(entitiesToExclude, currentMagnet, sizeAndMagNumArr)

        # End main.
        print("Script is complete.")
        return
    
    # Catches SystemExit error that occurs from exit() commands.
    except SystemExit as e: 
        print("Program exited.")
        return



main()