from PIL import ImageGrab
import numpy as np
import cv2
import time
import threading
import keyboard as PythonKeyboard
from pynput.keyboard import Key, Controller, KeyCode
import random
import psutil
import datetime
import os
import shutil
import configparser
import winsound
from colorama import Fore, Style, init
import subprocess

init()
# Get settings.ini file from same dir as AutoBM.py
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(script_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_file_path)

global EnableButterfingers
global EnableBadManners
#global TimeRemaining

keyboard = Controller()
topTime = time.time()
bottomTime = time.time()
deadTime = time.time()
toggleTime = time.time()
BMtoggleTime = time.time()
CheckCounter = 0
DeathBMCounter = 0
BMCounter = 0
#TimeRemaining = 0

 

# Pull settings from settings.ini
EnableBadManners = int(config['Settings']['ChatSh*t'])
EnableButterfingers = int(config['Settings']['DropC4Immediately'])
EnableCS2Check = int(config['Settings']['CloseOnCS2Exit'])
EnableChirp = int(config['Settings']['PCSpeakerJingles'])
EnableVerboseConsole = int(config['Settings']['VerboseConsole'])
EnableBMOutToConsole = int(config['Settings']['PrettyConsoleOutput'])
imgCoords = list(map(int, config['Coordinates']['img'].split(',')))
img_x1, img_y1, img_x2, img_y2 = imgCoords
img2Coords = list(map(int, config['Coordinates']['img2'].split(',')))
img2_x1, img2_y1, img2_x2, img2_y2 = img2Coords
img3Coords = list(map(int, config['Coordinates']['img3'].split(',')))
check_x, check_y = img3Coords  # For color #FFFFFF, checks for the "5" in the HUD

#target_color1 = (172, 103, 22)  # Color #AC6716, unused
target_color = (255, 255, 255)  # Color #FFFFFF
margin_of_error = 10


def color_within_margin(pixel_color, target_color, margin):
    return all(abs(pixel_color[i] - target_color[i]) <= margin for i in range(3))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# Coordinates to check for each color
#check_x1, check_y1 = 295, 175  # For color #AC6716, checks for the dark bit of the C4 on your minimap when you have it, unused


# To Do: turn this code into its own seperate script to run as a Supervisor Script, something like AUTOBM-SUPERVISOR.py or something, which checks the state of CS2.exe and closes this script if CS2 isn't found.
# Take that, sticky controls bug! ฅ^•ﻌ•^ฅ
# Function to check if process is running
def is_process_running(process_name):
    for proc in psutil.process_iter():
        if proc.name().lower() == process_name.lower():  # Convert both to lowercase for case-insensitive comparison
            return True
    return False

# Get current date and time
CurrentDatetime = datetime.datetime.now()
FormattedDatetime = CurrentDatetime.strftime("%Y-%m-%D_%H-%M-%S")


# Specify the directory where log files are stored
LogDirectory = "./logs"

# Function to remove the oldest log files if the limit is exceeded
def RemoveOldLogs(LogDirectory, limit):
    LogFiles = [os.path.join(LogDirectory, f) for f in os.listdir(LogDirectory) if os.path.isfile(os.path.join(LogDirectory, f))]
    LogFiles.sort(key=os.path.getctime)
    while len(LogFiles) > limit:
        os.remove(LogFiles[0])
        LogFiles.pop(0)

# Check and create log directory if it does not exist
if not os.path.exists(LogDirectory):
    os.makedirs(LogDirectory)

def ChangeEBF():
    global EnableButterfingers
    global toggleTime
    
    # Define the delay between toggles (in seconds)
    toggle_delay = 1
    
    # Check if enough time has passed since the last toggle
    if time.time() - toggleTime >= toggle_delay:
        # Toggle EnableButterfingers state
        EnableButterfingers = 1 - EnableButterfingers
        
        # Update toggleTime to the current time
        toggleTime = time.time()
        
        # Print status message
        if EnableButterfingers == 1:
            print(Fore.GREEN + Style.BRIGHT + "Enabled Butterfingers!" + Style.RESET_ALL)
            if EnableChirp == 1:
                winsound.Beep(600,35)
                winsound.Beep(700,35)
                winsound.Beep(600,30)
                winsound.Beep(400,25)
                winsound.Beep(800,35)
        else:
            print(Fore.RED + Style.BRIGHT + "Disabled Butterfingers!" + Style.RESET_ALL)
            if EnableChirp == 1:
                winsound.Beep(800,35)
                winsound.Beep(600,30)
                winsound.Beep(400,25)
                winsound.Beep(100,50)
                winsound.Beep(50,50)

def ChangeBM():
    global EnableBadManners
    global BMtoggleTime
    
    # Define the delay between toggles (in seconds)
    BM_toggle_delay = 1
    
    # Check if enough time has passed since the last toggle
    if time.time() - BMtoggleTime >= BM_toggle_delay:
        # Toggle EnableButterfingers state
        EnableBadManners = 1 - EnableBadManners
        
        # Update toggleTime to the current time
        BMtoggleTime = time.time()
        
        # Print status message
        if EnableBadManners == 1:
            print(Fore.GREEN + Style.BRIGHT + "Enabled Bad Manners!" + Style.RESET_ALL)
            if EnableChirp == 1:
                winsound.Beep(100,35)
                winsound.Beep(110,35)
                winsound.Beep(120,30)
                winsound.Beep(140,25)
                winsound.Beep(180,35)
        else:
            print(Fore.RED + Style.BRIGHT + "Disabled Bad Manners!" + Style.RESET_ALL)
            if EnableChirp == 1:
                winsound.Beep(180,35)
                winsound.Beep(140,30)
                winsound.Beep(120,25)
                winsound.Beep(100,50)
                winsound.Beep(50,50)


# Declare settings in console window before actually getting into the meat and potatoes
print(Fore.YELLOW + Style.BRIGHT + f"img  coordinates: ({img_x1}, {img_y1}), ({img_x2}, {img_y2})" + Style.RESET_ALL)
print(Fore.YELLOW + Style.BRIGHT + f"img2 coordinates: ({img2_x1}, {img2_y1}), ({img2_x2}, {img2_y2})" + Style.RESET_ALL)
print(Fore.YELLOW + Style.BRIGHT + "Close on CS2 Exit: ", EnableCS2Check," Drop C4: ", EnableButterfingers, " Bad Manners: ", EnableBadManners)
print(Fore.YELLOW + Style.BRIGHT + "Verbose Console: ", EnableVerboseConsole, " Pretty Console Output: ", EnableBMOutToConsole)
time.sleep(0.5)
print(Fore.MAGENTA + Style.BRIGHT + "You can change settings in config.ini" + Style.RESET_ALL)
time.sleep(0.5)

def is_process_running(process_name):
    for proc in psutil.process_iter():
        if proc.name().lower() == process_name.lower():  
            return True
    return False

def check_cs2():
    while True:
        #global TimeRemaining
        if EnableCS2Check == 1:
            # Use subprocess to check if the process is running
            result = subprocess.run('tasklist', stdout=subprocess.PIPE, text=True)
            if 'cs2.exe' not in result.stdout:
                print("cs2.exe is not running. Exiting script.")
                print("Total BMs: ", BMCounter)
                print("Total Death BMs:", DeathBMCounter)
                LogFilename= f"BMs_log_{FormattedDatetime}.txt"
                LogFilepath = os.path.join(LogDirectory, LogFilename)
                with open(LogFilepath, "a") as f:
                    f.write(f"-={FormattedDatetime}=-\n")
                    f.write(f"  Total BMs: {BMCounter}\n")
                    f.write(f"  Total Death BMs: {DeathBMCounter}\n")
                    f.write(f"  Hope you had fun games! :)\n")
                    
                    # Remove old log files if the limit is exceeded
                RemoveOldLogs(LogDirectory, 15)
                os._exit(0)
            else:
                #TimeRemaining = 5 - (time.time())
                if EnableVerboseConsole == 1:
                    print(Fore.CYAN + "CS2 is being checked for! It is still running!" + Fore.WHITE)
        else:
            if EnableVerboseConsole == 1:
                print(Fore.RED + "CS2 is not being checked for! Skipping..." + Style.RESET_ALL)
        time.sleep(5)



# Function to handle hotkey checks in a separate thread
def hotkey_thread():
    PythonKeyboard.add_hotkey('ctrl+alt+b', ChangeEBF)
    PythonKeyboard.add_hotkey('ctrl+alt+n', ChangeBM)

# Create and start the hotkey thread
hotkey_thread = threading.Thread(target=hotkey_thread)
hotkey_thread.daemon = True
hotkey_thread.start()

cs2_thread = threading.Thread(target=check_cs2)
cs2_thread.daemon = True  # Set as daemon so it exits when the main thread exits
cs2_thread.start()

# Main loop
while True:
    time.sleep(0.14)            
    # Capture screenshot for top position
    img = ImageGrab.grab(bbox=(img_x1,img_y1,img_x2,img_y2))
    img_np = np.array(img)
    
    # Capture screenshot for bottom position
    img2 = ImageGrab.grab(bbox=(img2_x1,img2_y1,img2_x2,img2_y2))
    img2_np = np.array(img2)
    
    # Capture screenshot for dead position
    img3 = ImageGrab.grab(bbox=(1000,500,1001,501))
    img3_np = np.array(img3)
    
    # Extract pixel value from top position
    checkNum = str(img_np[0][0]).split(" ")
    checkNum = str(checkNum[0])+ str(checkNum[1]) + str(checkNum[2])
    
    # Extract pixel value from bottom position
    checkNum2 = str(img2_np[0][0]).split(" ")
    checkNum2 = str(checkNum2[0])+ str(checkNum2[1])+ str(checkNum2[2])
    
    # Extract pixel value from dead position
    checkNum3 = str(img3_np[0][0]).split(" ")
    checkNum3 = str(checkNum3[0])+ str(checkNum3[1])+ str(checkNum3[2])

    if EnableBadManners == 1:
        # Check conditions for top position
        if checkNum == "[225" and time.time()-topTime >= 7:
            topTime = time.time()
            BMCounter +=1
            KeyToPress = random.choice(['/', '.'])  # randomly choose between '/' or '.'
            if EnableBMOutToConsole == 1:
                PrintTime = datetime.datetime.now()
                CurrentPrintTime = PrintTime.strftime("%H:%M:%S")
                print("[", CurrentPrintTime, "]", "BM","\t", KeyToPress )
            keyboard.press(KeyToPress)
            keyboard.release(KeyToPress)

    # Check conditions for dead position
    if checkNum3 == "[000]" and time.time()-deadTime >= 8:
        deadTime = time.time()
        KeyToPress = random.choice(['/', '.'])  # randomly choose between '/' or '.'
        keyboard.press(KeyToPress)
        keyboard.release(KeyToPress)
        if EnableBMOutToConsole == 1:
            PrintTime = datetime.datetime.now()
            CurrentPrintTime = PrintTime.strftime("%H:%M:%S")
            print("[", CurrentPrintTime, "]", "DeadBM","\t", KeyToPress )
        DeathBMCounter +=1

        # Currently disabled due to dumb chicanery on my part. Sorry.
        # Check conditions for bottom position
        #if checkNum2 == "[225" and time.time()-bottomTime >= 8:
        #    topTime = time.time()
        #    bottomTime = time.time()
        #    BMCounter +=1
        #    KeyToPress = random.choice(['/', '.'])  # randomly choose between '/' or '.'
        #   if EnableBMOutToConsole == 1:
        #        PrintTime = datetime.datetime.now()
        #        CurrentPrintTime = PrintTime.strftime("%H:%M:%S")
        #        print("[", CurrentPrintTime, "]", "BM","\t", KeyToPress )
        #    keyboard.press(KeyToPress)
        #    keyboard.release(KeyToPress)

    if EnableButterfingers == 1:
        # Take a screenshot of the region that includes the coordinates to check for color #AC6716, 
        # Disabled as if you walk over the bomb even if it is planted it will "force" you to drop the C4. 
        # Relying purely on HUD, which I think is reliable enough to cause chaos
       # screenshot1 = ImageGrab.grab(bbox=(check_x1, check_y1, check_x1 + 1, check_y1 + 1))
       # screenshot_np1 = np.array(screenshot1)
       # pixel_color1 = screenshot_np1[0, 0]

        # Take a screenshot of the region that includes the coordinates to check for color #FFFFFF
        screenshot2 = ImageGrab.grab(bbox=(check_x, check_y, check_x + 1, check_y + 1))
        screenshot_np2 = np.array(screenshot2)
        pixel_color2 = screenshot_np2[0, 0]

        # Check if either pixel color is within the margin of error
        #if color_within_margin(pixel_color1, target_color1, margin_of_error) or color_within_margin(pixel_color2, target_color, margin_of_error):
        if color_within_margin(pixel_color2, target_color, margin_of_error):
            #if EnableBMOutToConsole == 1:
            #    if color_within_margin(pixel_color1, target_color1, margin_of_error): #AC6716 Check
            #        PrintTime = datetime.datetime.now()
            #        CurrentPrintTime = PrintTime.strftime("%H:%M:%S")
            #        print("[", CurrentPrintTime, "]", "BF!\t#AC6716")
            if EnableBMOutToConsole == 1:        
                if color_within_margin(pixel_color2, target_color, margin_of_error): #FFFFFF Check
                    PrintTime = datetime.datetime.now()
                    CurrentPrintTime = PrintTime.strftime("%H:%M:%S")
                    print("[", CurrentPrintTime, "]", "BF!\t#FFFFFF")   
            # Simulate pressing and releasing the 'h' key (perform custom action)
            keyboard.press('h')
            time.sleep(0.1)
            keyboard.release('h')
        else:
            #pixel_color_hex1 = rgb_to_hex(pixel_color1)
            pixel_color_hex2 = rgb_to_hex(pixel_color2)



        
        
            if EnableVerboseConsole == 1:
                print("")
                print("================================================================================")
                print("Don't BM because:", checkNum, "isn't [225 or", time.time()-topTime, "isn't greater than 8")
                print("Don't BM because:", checkNum2, "isn't [225 or", time.time()-bottomTime, "isn't greater than 8")
                #print(f"Target color not detected. Found color at ({check_x1}, {check_y1}): {pixel_color_hex1}, at ({check_x2}, {check_y2}): {pixel_color_hex2}")
                print(f"Target color not detected. Found color at ({check_x}, {check_y}): {pixel_color_hex2}")
                print("EnableCS2Check: ", EnableCS2Check, " Butterfingers: ", EnableButterfingers)





# If you find any bugs, this cat might be able to help!
#                          ╱|、
#                  meow   (˚ˎ 。7  
#                          |、˜〵          
#                          じしˍ,)ノ


#                                                           AUTOBMBD                                                             #
#                                             IT MEANS AUTO BAD MANNERS & BOMB DROPS                                             #
#                       ORIGINAL CODE BY COLOSSALTROLLER. MODIFIED MASSIVELY BY TRIXINOUS. PROVIDED AS IS.                       #
#							                            VERSION NUMBER 45                           							 #
