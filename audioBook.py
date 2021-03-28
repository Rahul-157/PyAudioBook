#!/usr/bin/env python
from sys import platform as PLATFORM, argv
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import  TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from random import random
from gtts import gTTS
from os import system
from re import sub
from multiprocessing import cpu_count 
import ctypes 
from threading import Thread
from pydub import AudioSegment

NOTIFY_MSG = "'Remove Initial Pages like Contents, Preface, Acknowledgements to avoid those in mp3...'"
THREADS = cpu_count()

def random_name():
    s=""
    a="abcdfeghijklmnopqrstuvwxyz1234567890"
    for i in range(6):
        s+=a[int(random()*100)%36]
    return s

def pdfparser(data,filename):
    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr,  laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue() 
    data = sub(" \(cid:\d{1,6}\) ","",data)
    textfile = open(filename,'w+')
    textfile.write(data)
    textfile.close()

def remove_extra_pages(filename):
    editors_nix = ["gedit","nano","vim","vi"]
    if "linux" in PLATFORM:
        for editor in editors_nix:
            try:
                system("notify-send "+ NOTIFY_MSG)
                pid= system(editor +" "+ filename)
                if(pid==0):
                    
                    return
            except:
                pass
    else:    
        ctypes.windll.user32.MessageBoxW(0, NOTIFY_MSG, "Notification", 1)
        pid= system("notepad" + filename)
        if(pid==0):
            return

def find_last_word(start,blk_size,text):
    lst_idx = start + blk_size
    if(lst_idx>=len(text)):
        lst_idx=len(text)-1
    for i in range(lst_idx,start,-1):
        if(text[i]==" "):
            return i
            break
    
def worker(text,filename,i):
    tts = gTTS(text,lang="hi")
    tts.save(filename+"_"+str(i)+".mp3")

def collect_files(filename):
    book = AudioSegment.from_mp3(filename+"_0.mp3")
    for i in range(1,THREADS):
        book = book + AudioSegment.from_mp3(filename+"_"+str(i)+".mp3")
    opt_file = filename.replace("tmp","mp3")
    book.export(opt_file, format="mp3")
    system("rm "+filename+"_*")

if __name__=="__main__":
    assert ( len(argv)>1 )
    filename = random_name()+".tmp"
    if("linux" in PLATFORM):
        system("less "+argv[1]+" > "+filename)
    else:
        pdfparser(argv[1],filename)
    remove_extra_pages(filename)
    f = open(filename,"r")
    text = f.read()
    f.close()
    block_size = int(len(text)/THREADS)+1
    threads = list()
    start=0
    for i in range(THREADS):
        last_idx = find_last_word(start,block_size,text)
        if(i==THREADS-1):
            last_idx=len(text)
        threads.append(Thread(target = worker,args=(text[start:last_idx+1],filename,i)))
        threads[i].start()
        start=last_idx+1
    
    for i in range(THREADS):
        threads[i].join()
    system("rm "+filename)
    collect_files(filename)
    