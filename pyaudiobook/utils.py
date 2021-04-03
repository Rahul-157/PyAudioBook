from random import random
import ctypes 
from gtts import langs
from sys import platform as PLATFORM
from os import system,path
import logging
from multiprocessing import cpu_count
logger = logging.getLogger('pyaudiobook')
logging.basicConfig(level = logging.INFO)

_THREADS = 1
NOTIFY_MSG = "'Remove Pages Contents, Preface, Acknowledgements, References'"
LANGS = langs._langs
TEMP_LOC = path.join(path.expanduser("~"),".TXTnMP3")


def setThreads(num_threads):
    global _THREADS
    if not num_threads:
        _THREADS = cpu_count()
    else:
        assert int(th)>0, "Number of Threads Should be Greater than 0"
        _THREADS = int(th)

def getThreads():
    return _THREADS

def runCommand(cmd_list):
    command = " ".join(cmd_list)
    exit_code = system(command)
    assert exit_code == 0, "Command : " + command + "Failed | ExitCode : " + str(exit_code)
    return exit_code

def getAbsolutePath(filepath):
    if "linux" not in PLATFORM:
        filepath = filepath.replace('/','\\')
    if(filepath[0]=='~'):
        filepath = path.join(path.expanduser('~'),filepath[2:])
    else:
        filepath = path.abspath(filepath)
    return filepath
       

def languageCheck(language):
    while(language not in LANGS):
        logger.error("Language Not supported... Default : en English\nSupport Lanaguages are : \n")
        #Todo : Print only once
        for key,value in LANGS.items():
            print(key + " : "+ value)
        language = input("Enter Language Key eg: en for English\n")
    return language

def findLastWord(start,blk_size,text):
    lst_idx = start + blk_size
    if(lst_idx>=len(text)):
        lst_idx=len(text)-1
    for i in range(lst_idx,start,-1):
        if(text[i]==" "):
            return i
            break
  
def cleanup():
    if "linux" in PLATFORM:
        runCommand(["rm -rf ",TEMP_LOC])
    else:
        runCommand(["rd /s /q ",TEMP_LOC])


def randomName(length=6):
    s=""
    a="abcdfeghijklmnopqrstuvwxyz1234567890"
    for i in range(length):
        s+=a[int(random()*100)%36]
    return s

def removeExtraPages(filename):
    editors_nix = ["vim","gedit","nano","vi"]
    if "linux" in PLATFORM:
        for editor in editors_nix:
            try:
                runCommand(["notify-send", NOTIFY_MSG])
                ret_val = runCommand([editor,filename])
                if not ret_val:
                    break
            except:
                pass
    else:    
        ctypes.windll.user32.MessageBoxW(0, NOTIFY_MSG, "Notification", 1)
        runCommand(["notepad",filename])