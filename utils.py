from random import random
from multiprocessing import cpu_count 
from gtts import langs
from sys import platform as PLATFORM
from os import system
NOTIFY_MSG = "'Remove Pages Contents, Preface, Acknowledgements, References'"
THREADS = cpu_count()
LANGS = langs._langs

def language_check(language):
    while(language not in LANGS):
        Warning("Language Not supported... Defaul : en English")
        Warning("Supported Languages :"+ LANGS)
        language = input("Enter Language Key eg: en for English")
    return language

def find_last_word(start,blk_size,text):
    lst_idx = start + blk_size
    if(lst_idx>=len(text)):
        lst_idx=len(text)-1
    for i in range(lst_idx,start,-1):
        if(text[i]==" "):
            return i
            break
  


def cleanup(filename):
    if "linux" in PLATFORM:
        system("rm *tmp* ")
    else:
        system("del /f *tmp* ")


def random_name(length=6):
    s=""
    a="abcdfeghijklmnopqrstuvwxyz1234567890"
    for i in range(length):
        s+=a[int(random()*100)%36]
    return s
