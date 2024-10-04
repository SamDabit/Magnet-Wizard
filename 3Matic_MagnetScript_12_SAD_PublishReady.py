# Created on 7/25/24 by Samir Dabit
# This is the automatic magnet-placing script.

# Version 12 contains completely overhauled UI.
""" ChangeLog:
    | Updated each window's GUI.
    | Changed button colors.
    | Added frames to UI to allow easier centering.
"""

# Tip   : Ctrl+K Ctrl+0 collapses all collapsables.
# Notes : I use the terms 'entity' and 'part' interchangeably.
#         'return' does not work normally when using Tkinter. I used global variables to get around it.

""" Known issues:
    - *While script is running, cannot quit it or close 3-Matic safely.
    -  Finding parts based on name. There should be a safer way to do this in a revision.
"""

""" TODO: Current Task (B)
        [* means completed]
        (R) Delete cut planes after they are used?
        (U) Include all Tkinter specific global variables at the start of the script possibly.
        (X) Add ability to move housings & magnets set before subtraction/union
        (Y) Move Aorta_Hollow.mxp to sharedrive so that testing can work in both Student Edition & Medical Edition
        (A) Clean up all GUIs for final presentation.
            1) AskForFilePathAndUpdate()     [Good]
            2) AskForSizes()                 [Good]
            3) AskForHousingInput()          [Decent]
                > Change Radiobuttons to be full boxes. Or make them bigger so it looks right.
            4) IndicatePointsPopupWithUndo() [Good]
                > Gray out the undo button and submit buttons when they cant be used.
            5) AskForEntityInput()           [Good]
        (B) Standardize all the GUI font sizes.
            -> Title
            -> Subtitle
            -> Body
        (C) Revise Pseudocode to be more accurate & easier to read.
        (D) Reorganize methods.
        (E) Change to having 1 GUI window. 
            -> Add a global 'Back' button.
        (F) Add a help feature to each window.
        (G) Add a background color to each window.
            > Does not look good with diff background colors
        (H) Show plane before submit in IndicatePoints UI
            -> Delete if undo, Create if 3 points are selected.
"""

import trimatic
import os

# Tkinter is Python's Native GUI interface.
import tkinter as tk
from tkinter import *
# import customtkinter
from tkinter import ttk

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
mediumNormalVector = (0.0081, 0.0795, 0.9968)   # Set normal vector.
mediumOrigin = (52.7673, 27.3229, 10.3038)      # Set origin.
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

# *.*.* End Global Variables *.*.*

# =-=-=-=-=-=-==-=-=-=-=-=-= ALL METHODS =-=-=-=-=-=-==-=-=-=-=-=-=

# Temporary method for testing.
""" Imports Aorta for testing.
    | Source: 'Align and remesh.py'
    | 
    | return: void
"""
def ImportAorta():
    application_exe = trimatic.get_application_path()
    application_path = os.path.dirname(application_exe)
    demopath = os.path.join(application_path, "DemoFiles")
    path = os.path.join(demopath, "Aorta_Hollow.mxp")
    trimatic.open_project(path)

""" Finds a valid file path to use for the magnet STL files.
"""
def InitializeFileVariables():
    trimatic.suspend_progress()

    filePath1 = r"X:"
    filePath2 = r'X:\X\X'
    filePath3 = r'\\X\X\X\X'

    # Create filePathArray. Make sure that all 3 file paths are in the array b4 running.
    filePathsArray = [filePath1, filePath2, filePath3]

    # Try each of the three different file paths I've found.
    for filePath in filePathsArray:

        # Check if the file path exists.
        if(os.path.exists(filePath)):
            print("File path " + filePath + " exists!")

            # Store the file path, update the global magnet file paths variables.
            UpdateMagnetFilePaths(filePath)
            return
        
    # If none of the file paths work. ask user for their specific file path.
    AskForFilePathAndUpdate()

    return

""" Updates the magnet file paths.
    | param filePath: string
"""
def UpdateMagnetFilePaths(filePath):
    trimatic.suspend_progress()

    # Magnet Files
    global magnetMini, magnetSmall, magnetMedium, magnetLarge
    magnetMini      = filePath + r"\X\magnet.stl"
    magnetSmall     = filePath + r"\X\magnet.stl"
    magnetMedium    = filePath + r"\X\magnet.stl"
    magnetLarge     = filePath + r"\X\magnet.stl"

    # Magnet Housings
     # Mini
    global magnetMiniHousingA,   magnetMiniHousingB     # Minis
    magnetMiniHousingA = filePath + r"\X\housing.stl"
    magnetMiniHousingB = filePath + r"\X\housing.stl"

     # Smalls
    global magnetSmallHousingA,  magnetSmallHousingB    # Smalls
    magnetSmallHousingA = filePath + r"\X\housing.stl"
    magnetSmallHousingB = filePath + r"\X\housing.stl"

     # Mediums
    global magnetMediumHousingA, magnetMediumHousingB   # Mediums
    magnetMediumHousingA = filePath + r"\X\housing.stl"
    magnetMediumHousingB = filePath + r"\X\housing.stl"

     # Larges
    global magnetLargeHousingA,  magnetLargeHousingB    # Larges
    magnetLargeHousingA = filePath + r"\X\housing.stl"
    magnetLargeHousingB = filePath + r"\X\housing.stl"

    return

""" Creates a popup window and asks the user to input a their AMU file path.
"""
def AskForFilePathAndUpdate():
    trimatic.suspend_progress()

    # Initialize Tkinter root
    winPath = tk.Tk()
    winPath.title('Magnet Wizard')
    winPath.attributes('-topmost', True)
    winPath.geometry("315x120")

    top_frame = Frame(winPath, width=315, height=60)
    top_frame.grid(row=0, padx=5)
    middle_frame = Frame(winPath, width=315, height=60)
    middle_frame.grid(row=1, pady=10)
    bottom_frame = Frame(winPath, width=315)
    bottom_frame.grid(row=2)

    textEntry_var = tk.StringVar()

    def submit():
        # Check if file path exists.
        # Keep asking user to input until the file path is valid.

        # Check if file exists.
        if (os.path.exists(textEntry_var.get())):
            # If true, return file path name.

            print("A file path has been successfully found: " + textEntry_var.get())
            global filePath_global
            filePath_global = textEntry_var.get()

            UpdateMagnetFilePaths(filePath_global)

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
            # middle_frame.config(height=90)
            invalidLabel.config(text="Invalid File Path")
            return
    
    def quit():
        winPath.destroy()
        exit()

    # Text labels and Buttons
    textLabel = tk.Label(top_frame, text = "Enter your file path.", font=('Arial', 12, 'bold'))
    descriptionLabel = tk.Label(top_frame, text = "Copy your general file path...", font=('Arial', 10, 'italic'))
    filePath_Entry = tk.Entry(top_frame, text = "X:\...", textvariable=textEntry_var, width=20)

    sub_btn = tk.Button(middle_frame, text = 'Submit', command = submit, background = 'lime green')
    quit_btn = tk.Button(middle_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2')

    invalidLabel = tk.Label(bottom_frame, text = "", font=('Arial', 12), fg="red")

    # Set locations
    textLabel.grid(row=0)
    descriptionLabel.grid(row=1)
    filePath_Entry.grid(row=2)

    sub_btn.grid(row=0, column=0, padx=15)
    quit_btn.grid(row=0, column=1, padx=15)

    invalidLabel.grid(row=0)

    winPath.mainloop()

    return

""" Asks the user to input the desired amount of magnets of each size.
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

    # Set Title
    winSize.title('Magnet Wizard')

    # Make Window Stay on Top
    winSize.attributes('-topmost', True)

    # Sets geometry (width x height)
    winSize.geometry("285x190")

    top_frame = Frame(winSize, width=285)
    top_frame.grid(row=0)
    middle_frame = Frame(winSize, width=285)
    middle_frame.grid(row=1, pady=10)
    bottom_frame = Frame(winSize, width=285)
    bottom_frame.grid(row=2)

    # Variables
    magnetSize_Mini_var   = tk.IntVar()
    magnetSize_Small_var  = tk.IntVar()
    magnetSize_Medium_var = tk.IntVar()
    magnetSize_Large_var  = tk.IntVar()

    # Submit Function
    # 1. Saves information from Tkinter prompt.
    # 2. Closes the window.
    def submit():
        global magnetNumMini
        magnetNumMini = int(S1.get())
        global magnetNumSmall
        magnetNumSmall = int(S2.get())
        global magnetNumMedium
        magnetNumMedium = int(S3.get())
        global magnetNumLarge
        magnetNumLarge = int(S4.get())

        global magnetNumTotal
        magnetNumTotal = magnetNumMini + magnetNumSmall + magnetNumMedium + magnetNumLarge

        # Prevents the user from continuing with the script unless the following conditions are met.
        if magnetNumTotal <= 0:
            print("[ERROR] Unable to continue:\n    Please input magnet numbers.")
        else:
            winSize.destroy()

    def quit():
        winSize.destroy()
        exit()
    # Label & Entry

        # Size of magnets?
    title_label = tk.Label(top_frame, text = 'Magnet Sizes',  font=('Arial', 12, 'bold'))
    subtitle_label = tk.Label(top_frame, text = 'Enter the amount of each magnet size you want.', font=('Arial', 10, 'italic'))

    S1Label = tk.Label(middle_frame, text = "Mini", font=('Arial', 10, 'bold'))
    S2Label = tk.Label(middle_frame, text = "Small", font=('Arial', 10, 'bold'))
    S3Label = tk.Label(middle_frame, text = "Medium", font=('Arial', 10, 'bold'))
    S4Label = tk.Label(middle_frame, text = "Large", font=('Arial', 10, 'bold'))
    S1 = tk.Spinbox(middle_frame, from_=0, to_=1000, textvariable = magnetSize_Mini_var, font=('Arial', 12))
    S2 = tk.Spinbox(middle_frame, from_=0, to_=1000, textvariable = magnetSize_Small_var, font=('Arial', 12))
    S3 = tk.Spinbox(middle_frame, from_=0, to_=1000, textvariable = magnetSize_Medium_var, font=('Arial', 12))
    S4 = tk.Spinbox(middle_frame, from_=0, to_=1000, textvariable = magnetSize_Large_var, font=('Arial', 12))
    
        # Submit button
    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'lime green')

        # Quit Button
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2')
    
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

    # Loop until closed
    winSize.mainloop()

""" Asks user if they want housing.
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
    global winHousing   # Global b/c close when all magnets are done (outside of this function).
    winHousing = tk.Tk()

    # Global so that I can change it back to False before every loop.
    global magnetHousing
    magnetHousing = False

    # Make Window Stay on Top
    winHousing.attributes('-topmost', True)

    # Sets geometry (width x height)
    winHousing.geometry("250x130")

    # Set Title
    winHousing.title('Magnet Wizard')

    top_frame = Frame(winHousing, width=120, height=60)
    top_frame.grid(row=0, padx=5)
    middle_frame = Frame(winHousing, width=120, height=30)
    middle_frame.grid(row=1, pady=10)
    bottom_frame = Frame(winHousing, width=120, height=30)
    bottom_frame.grid(row=2)

    # Save and return the value.
    def submit():
        global magnetHousing
        magnetHousing = magnetHousing_var.get()
        winHousing.destroy()
        print("You answered: " + str(magnetHousing))
    
    def quit():
        winHousing.destroy()
        exit()

    def selectYes():
        yesButton.config(bg='pale green')
        noButton.config(bg='light gray')
        return
    
    def selectNo():
        yesButton.config(bg='light gray')
        noButton.config(bg='salmon')
        return
    
    # Labels and Buttons
    title_label = tk.Label(top_frame, text = "Housings", font=('Arial', 12, 'bold'))
    size_label = tk.Label(top_frame, text = "Would you like housings for " + size + " " + str(currentNum) + "/" + str(totalNum) + "?", font=('Arial', 10, 'italic'))

    magnetHousing_var = tk.BooleanVar()

    yesButton = Radiobutton(middle_frame, text = "Yes", variable = magnetHousing_var, value = True, font=('Arial', 10, 'bold'), bg='light gray', command=selectYes)
    noButton = Radiobutton(middle_frame, text = "No", variable = magnetHousing_var, value = False, font=('Arial', 10, 'bold'), bg='salmon', command=selectNo)

    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'lime green')
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2')

    # Set Locations on Grid
    title_label.grid(row=0)
    size_label.grid(row=1)

    yesButton.grid(row=0, column=0, padx=5)
    noButton.grid(row=0, column=1, padx=5)

    sub_btn.grid(row=0, column=0, padx=10)
    quit_btn.grid(row=0, column=1, padx=10)

    # Loop until closed
    winHousing.mainloop()

""" Via a popup window, prompts the user to indicate 3 points.
    | This window's UI needs to be improved, but this is a working version at least.
    | 
    | return: globalPointsArray
    | rtype : global array of trimatic.coordinate
"""
def AskForFixedPlanePoints():
    trimatic.suspend_progress()

    winPoints = tk.Tk()
    winPoints.title('Magnet Wizard')
    winPoints.attributes('-topmost', True)
    # winPoints.geometry(str(width) + "x" + str(height))
    winPoints.geometry("275x180")

    winPoints.current_num = 0 # Creates a self-contained variable.
    winPoints.points_array         = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    winPoints.points_array_display = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    top_frame = Frame(winPoints, width = 270)
    top_frame.grid(row=0)
    bottom_frame = Frame(winPoints, width=270)
    bottom_frame.grid(row=1)

    def submit():
        if (winPoints.current_num >= 3):
            print("All points sucessfully selected.")
            winPoints.destroy()

            # Assign global variable b/c return doesn't work in Tkinter.
            global globalPointsArray
            globalPointsArray = winPoints.points_array
        else:
            print("Cannot Submit.")
        return

    # Quits the entire program.
    def quit():
        winPoints.destroy()
        exit()

    def undo():
        if (winPoints.current_num == 0):
            print("Cannot undo.")
            return
        winPoints.current_num = winPoints.current_num - 1

        if (winPoints.current_num == 0):
            undo_btn.config(bg='light gray')

        # Reset the most recent stored coordinate.
        winPoints.points_array[winPoints.current_num] = [0, 0, 0]
        winPoints.points_array_display[winPoints.current_num] = [0, 0, 0]
        
        # Update window labels
        pointNumLabel.config(text = "Indicate Point " + str(winPoints.current_num)  + "/" + str(3))
        pointLabel1.config(text = "Point 1: " + str(winPoints.points_array_display[0]))
        pointLabel2.config(text = "Point 2: " + str(winPoints.points_array_display[1]))
        pointLabel3.config(text = "Point 3: " + str(winPoints.points_array_display[2]))

        sub_btn.config(bg='light gray') # Make sure submit button is grayed out

        print("Successfully performed undo operation.")

        trimatic.suspend_progress()

    # Prompts user for next point, updates display
    def indicateNextPoint():

        print("Please Indicate coordinate.")
        winPoints.current_num = winPoints.current_num + 1
        #pointNumLabel.config(text = "Indicate Point " + str(winPoints.current_num)  + "/" + str(3))
        print(winPoints.points_array)

        # Prompt user to indicate coordinates, Store coordinates, Update display with coordinates.
        numDecimals = 3
        if (winPoints.current_num == 1):
            winPoints.points_array[0] = trimatic.indicate_coordinate()
            winPoints.points_array_display[0] = [round(winPoints.points_array[0][0], numDecimals), round(winPoints.points_array[0][1], numDecimals), round(winPoints.points_array[0][2], numDecimals)]
            pointLabel1.config(text = "Point 1: " + str(winPoints.points_array_display[0]))

            undo_btn.config(bg='PaleTurquoise1')

        elif (winPoints.current_num == 2):
            winPoints.points_array[1] = trimatic.indicate_coordinate()
            winPoints.points_array_display[1] = [round(winPoints.points_array[1][0], numDecimals), round(winPoints.points_array[1][1], numDecimals), round(winPoints.points_array[1][2], numDecimals)]
            pointLabel2.config(text = "Point 2: " + str(winPoints.points_array_display[1]))

        elif (winPoints.current_num == 3):
            winPoints.points_array[2] = trimatic.indicate_coordinate()
            winPoints.points_array_display[2] = [round(winPoints.points_array[2][0], numDecimals), round(winPoints.points_array[2][1], numDecimals), round(winPoints.points_array[2][2], numDecimals)]
            pointLabel3.config(text = "Point 3: " + str(winPoints.points_array_display[2]))

            sub_btn.config(bg='lime green') # Make submit button green

        pointNumLabel.config(text = "Indicate Point " + str(winPoints.current_num)  + "/" + str(3))

        trimatic.suspend_progress()

    # Prompts the user for the next point:

    # Initialize Labels and Buttons
    pointNumLabel = tk.Label(top_frame, text = "Indicate Point " + str(winPoints.current_num)  + "/" + str(3), font=('Arial', 12, 'bold'))
    subtitle_label = tk.Label(top_frame, text = "Select three points to indicate the fixed plane.", font=('Arial', 10, 'italic'))
    pointLabel1 = tk.Label(top_frame, text = "Point 1: " + str(winPoints.points_array[0]), font=('Arial', 10))
    pointLabel2 = tk.Label(top_frame, text = "Point 2: " + str(winPoints.points_array[1]), font=('Arial', 10))
    pointLabel3 = tk.Label(top_frame, text = "Point 3: " + str(winPoints.points_array[2]), font=('Arial', 10))

    indicateNext_btn = tk.Button(bottom_frame, text = 'Indicate Next Point', command = indicateNextPoint, background = 'gold2', width=15)
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2', width=15)
    undo_btn = tk.Button(bottom_frame, text = "Undo", command=undo, background = 'light gray', width=15)
    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'light gray', width=15)

    # Set Locations on Grid
    pointNumLabel.grid(row=0)
    subtitle_label.grid(row=1)
    pointLabel1.grid(row=2)
    pointLabel2.grid(row=3)
    pointLabel3.grid(row=4)

    indicateNext_btn.grid(row=0, column=0, padx=15, pady=5)
    undo_btn.grid(row=0, column=1, padx=5)
    sub_btn.grid(row=1, column=0)
    quit_btn.grid(row=1, column=1)

    winPoints.mainloop()

""" Asks user to select an entity from a dropdown.
    | param entitiesToExclude: array of trimatic.part
    | 
    | return: entityName
    | rtype : global string
"""
def AskForEntityInput(entitiesToExclude):
    # Set up window for input.
    winName = tk.Tk()
    winName.title('Magnet Wizard')
    winName.attributes('-topmost', True)
    winName.geometry("300x120")

    top_frame = Frame(winName, width=300, height=50)
    top_frame.grid(row=0)
    bottom_frame = Frame(winName, width=300, height=50)
    bottom_frame.grid(row=1, pady=10)


    def submit():
        global entityName
        entityName = entityNameComboBox.get()
        winName.destroy()
        #return entityName
       
    def quit():
        winName.destroy()
        exit()
    
    # Labels, Entries, and Buttons
    title_label = tk.Label(top_frame, text = "Subtraction", font=('Arial', 12, 'bold'))
    subtitle_label = tk.Label(top_frame, text = "Select which part you would like to subtract from.", font=('Arial', 10, 'italic'))
    
    prompt_label = tk.Label(bottom_frame, text = 'Name of Entity: ', font=('Arial', 10, 'bold'))

        # Create ComboBox
    entityName_var = tk.StringVar()
    entityNameComboBox = ttk.Combobox(bottom_frame, width = 27, textvariable = entityName_var)

        # Dropdown Values
    partList = trimatic.get_parts()
    partNamesList = []
        # This loop simplifies names to be displayed.
    for x in range(0, len(partList)):
        if partList[x] not in entitiesToExclude: # Only shows non-magnet/housing entities.
            partNamesList.append(partList[x].name)
    entityNameComboBox['values'] = partNamesList

        # Submit button
    sub_btn = tk.Button(bottom_frame, text = 'Submit', command = submit, background = 'lime green')

        # Quit Button
    quit_btn = tk.Button(bottom_frame, text = 'Exit Wizard', command = quit, background = 'firebrick2')

    # Setting Locations
    title_label.grid(row=0)
    subtitle_label.grid(row=1)
    prompt_label.grid(row=2, column=0)
    entityNameComboBox.grid(row=2, column=1)
    sub_btn.grid(row=3, column=0)
    quit_btn.grid(row=3, column=1)

    # Loop until closed
    winName.mainloop()
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

    AskForFixedPlanePoints() # Testing

    local_pointsArray = globalPointsArray
    print("Points returned: ")
    print(local_pointsArray)

    # Store coordinates.
    [p1, p2, p3] = local_pointsArray

    planeFixed = trimatic.analyze.create_plane_3_points(p1, p2, p3)
    print("Successfully created Plane on Fixed Entity!")

    # planeMoving = trimatic.analyze.create_plane_3_points(p4, p5, p6)
    print("Successfully created Plane on Moving Entity!")

    # Now get entity to move along. This will move the magnet to the aligned plane.
    trimatic.plane_to_plane_align(planeFixed, planeMoving, magnet)

    # Store both planes in an array to return.
    planeArray = [planeFixed, planeMoving]
    return planeArray

"""  Asks user to select 3 points for the fixed plane. Aligns magnet and housings to fixed plane.
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
    AskForFixedPlanePoints()

    local_pointsArray = globalPointsArray
    print("Points returned: ")
    print(local_pointsArray)

    # Store coordinates.
    [p1, p2, p3] = local_pointsArray

    planeFixed = trimatic.analyze.create_plane_3_points(p1, p2, p3)
    print("Successfully created Plane on Fixed Entity!")

    # planeMoving = trimatic.analyze.create_plane_3_points(p4, p5, p6)
    print("Successfully created Plane on Moving Entity!")

    # Now get entity to move along. This will move the magnet to the aligned plane.
    trimatic.plane_to_plane_align(planeFixed, planeMoving, [magnet, housingA, housingB])

    # Store both planes in an array to return.
    planeArray = [planeFixed, planeMoving]
    return planeArray

""" Subtracts one entity from another. Catches errors if they occur.
    | param entity            : trimatic.part
    | param subtracting_entity: trimatic.part
    | 
    | return: newEntity
    | rtype : trimatic.part
"""
def Subtract(entity, subtracting_entity):
    try: 
        print("Attempting to subtract...")
        newEntity = trimatic.boolean_subtraction(entity, subtracting_entity)
    except ValueError:
        print("[VALUE ERROR] Could not subtract " + subtracting_entity.name + " from " + entity.name + ".")
    except RuntimeError:
        print("[RUNTIME ERROR] Could not subtract " + subtracting_entity.name + " from " + entity.name + ".")
    except:
        print("[ERROR] Could not subtract " + subtracting_entity.name + " from " + entity.name + ".")
    return newEntity

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
    except ValueError:
        print("[VALUE ERROR]")
    except RuntimeError:
        print("[RUNTIME ERROR]")
    except:
        print("[ERROR]")
    return newEntity

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
def GetEntityFromUser(entitiesToExclude):
    trimatic.suspend_progress()

    AskForEntityInput(entitiesToExclude)    # Get Entity Name
    entityName_local = entityName
    
    print("Entity found: " + entityName_local)        # Testing

    entity = trimatic.find_part(entityName_local)     # Find entity from name.
    return entity

""" Combines magnet housings to specified 3-matic part.
    | param housingPartA: trimatic.part
    | param housingPartB: trimatic.part
    | 
    | return: newEntity
    | rtype : trimatic.part
"""
def UnionHousingToPart(housingPartA, housingPartB, entity):
    newEntity = Union([entity, housingPartA])
    entity = newEntity

    newEntity = Union([entity, housingPartB])

    return newEntity

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
    entitiesToExclude = []
    entitiesToAlign = []
    housings = []

    # Import correct magnet and housing
    if housing == True:
        currentPartsArray = ImportMagnetAndHousing(magNum, currentSize, housing)
        currentMagnet   = currentPartsArray[0]
        currentHousingA = currentPartsArray[1]
        currentHousingB = currentPartsArray[2]
                
        entitiesToExclude.append(currentHousingA) # Store current housings for exclusion.
        entitiesToExclude.append(currentHousingB)
    else:
        currentMagnet = ImportMagnetAndHousing(magNum, currentSize, housing)
    
    # Get new center plane
    currentCenterPlane = CreateCenterPlane(currentSize, magNum+1)
            
    entitiesToExclude.append(currentMagnet)

    # Select plane and align parts.
    if housing == True:
        entitiesToAlign = [currentMagnet, currentCenterPlane, currentHousingA, currentHousingB]
        housings = [currentHousingA, currentHousingB]   # Fill housings array if necessary.
    else:
        entitiesToAlign = [currentMagnet, currentCenterPlane]

    return [entitiesToExclude, entitiesToAlign, housings, currentMagnet]

# =-=-=-=-=-=-==-=-=-=-=-=-= END ALL METHODS =-=-=-=-=-=-==-=-=-=-=-=-=

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

        # ImportAorta() # For testing.

        # Maybe if no entities then importAorta()
        if HasEntities() == False:
            return

        InitializeFileVariables()

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

                entitiesToExclude = [] # Clear the variable.

                # Ask user for housing.
                AskForHousingInput(sizeArray[s], m+1, numArray[s])
                housing = magnetHousing

                # Import magnets and/or housings, returns all the necessary lists.
                [entitiesToExclude, entitiesToAlign, housings, currentMagnet] = ImportAndReturnEntities(housing, m, sizeArray[s])

                # Store housings from output.
                if housing == True:
                    currentHousingA     = housings[0]
                    currentHousingB     = housings[1]
                
                SelectFixedPlaneAndAlign(housing, entitiesToAlign)

                # Get entity to subtract from.
                entity = GetEntityFromUser(entitiesToExclude)

                # Combine housing to part if necessary.
                if housing == True:
                    entity = UnionHousingToPart(currentHousingA, currentHousingB, entity)
                
                # Subtract magnet from entity.
                Subtract(entity, currentMagnet)

        # End main.
        print("Script is complete.")
        return
    
    # Catches SystemExit error that occurs from exit() commands.
    except SystemExit as e: 
        print("Program exited.")
        return


main()