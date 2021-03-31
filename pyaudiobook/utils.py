from random import random
from multiprocessing import cpu_count 
from gtts import langs
from sys import platform as PLATFORM
from os import system,path
import logging
logger = logging.getLogger('pyaudiobook')
logger.setLevel(logging.DEBUG)

NOTIFY_MSG = "'Remove Pages Contents, Preface, Acknowledgements, References'"
THREADS = cpu_count()
LANGS = langs._langs
TEMP_LOC = path.join(path.expanduser("~"),".TXTnMP3")


def get_absolute_path(filepath):
    if "linux" not in PLATFORM:
        filepath = filepath.replace('/','\\')
    if(filepath[0]=='~'):
        filepath = path.join(path.expanduser('~'),filepath[2:])
    else:
        filepath = path.abspath(filepath)
    return filepath
       

def language_check(language):
    while(language not in LANGS):
        logger.error("Language Not supported... Default : en English\nSupport Lanaguages are : \n")
        for key in LANGS:
            logger.error(key + " : "+ LANGS[key])
        language = input("Enter Language Key eg: en for English\n")
    return language

def find_last_word(start,blk_size,text):
    lst_idx = start + blk_size
    if(lst_idx>=len(text)):
        lst_idx=len(text)-1
    for i in range(lst_idx,start,-1):
        if(text[i]==" "):
            return i
            break
  
def cleanup():
    if "linux" in PLATFORM:
        system("rm -rf "+TEMP_LOC)
    else:
        system("rd /s /q "+TEMP_LOC)


def random_name(length=6):
    s=""
    a="abcdfeghijklmnopqrstuvwxyz1234567890"
    for i in range(length):
        s+=a[int(random()*100)%36]
    return s
