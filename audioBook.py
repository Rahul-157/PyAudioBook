#!/usr/bin/env python
from sys import platform as PLATFORM, argv
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import  TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from gtts import gTTS
from os import system
from re import sub
import ctypes 
from threading import Thread
from datetime import datetime
from .utils import *


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
        pid= system("notepad " + filename)
        if(pid==0):
            return

  
def worker(text,filename,i,language):
    tts = gTTS(text,lang=language)
    tts.save(filename+"_"+str(i)+".mp3")

def collect_files(filename):
    fp = open(filename+"_0.mp3","rb")
    book = fp.read()
    fp.close()
    for i in range(1,THREADS):
        fp=open(filename+"_"+str(i)+".mp3","rb")
        book = book + fp.read()
        fp.close()
    opt_file = open("Output_"+datetime.now().strftime("%X").replace(":","_")+".mp3","wb")
    opt_file.write(book)


def main(pdf_to_process,language="en"):
    filename = random_name()+".tmp"
    language = language_check(language)
    if("linux" in PLATFORM):
        system("less "+pdf_to_process+" > "+filename)
    else:
        pdfparser(pdf_to_process,filename)
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
        threads.append(Thread(target = worker,args=(text[start:last_idx+1],filename,i,language)))
        threads[i].start()
        start=last_idx+1
    
    for i in range(THREADS):
        threads[i].join()
    collect_files(filename)
    cleanup(filename)

if __name__=="__main__":
    assert ( len(argv)>1 )
    if(len(argv)==3):
        main(argv[1],argv[2])
    else:
        main(argv[1])
    