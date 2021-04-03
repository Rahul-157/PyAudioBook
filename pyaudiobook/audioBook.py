#!/usr/bin/env python
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import  TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from gtts import gTTS
from os import stat
from re import sub
from threading import Thread
from .utils import *
from time import sleep,time


done = False

def pdfParser(data,filename):
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
    text_file = open(filename,mode="w+", encoding="utf-8")
    text_file.write(data)
    text_file.close()
  
def worker(text,filename,i,language):
    tts = gTTS(text,lang=language)
    filename = filename.replace(".txt", "")
    tts.save(filename+"_"+str(i)+".mp3")

def collectFiles(filename,output_name):
    filename = filename.replace(".txt", "")
    fp = open(filename+"_0.mp3",mode="rb")
    book = fp.read()
    fp.close()
    for i in range(1,getThreads()):
        fp= open(filename+"_"+str(i)+".mp3",mode="rb")
        book = book + fp.read()
        fp.close()
    opt_file = open(output_name,mode="wb")
    opt_file.write(book)
    opt_file.close()


def processFile(text_file,lang):
    global done
    f = open(text_file,mode="r", encoding="utf-8")
    text = f.read()
    f.close()
    block_size = int(len(text)/getThreads())+1
    threads = list()
    start=0
    s_time = time()
    for i in range(getThreads()):
        last_idx = findLastWord(start,block_size,text)
        if(i==getThreads()-1):
            last_idx=len(text)
        threads.append(Thread(target = worker,args=(text[start:last_idx+1],text_file,i,lang)))
        threads[i].start()
        start=last_idx+1
    progressBar(text_file)
    for i in range(getThreads()):
        threads[i].join()
    done = True
    e_time = time()
    print(f'\rProgress: |{"█"*70}| {100.0}% Completed')
    logger.info("Conversion Finished in : "+ str(e_time-s_time) +" seconds\n")


def printProgressBar (total, filename,length = 70, fill = '█'):
    global done
    while not done:
        itr=0
        for i in range(getThreads()):
            itr = itr + (stat(filename+"_"+str(i)+".mp3").st_size)
        if itr >= total: 
            break
        percent = ("{0:.1f}").format(100 * (itr / float(total)))
        filledLength = int(length * itr // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\rProgress: |{bar}| {percent}% Completed', end = '\r')
        sleep(5)

def progressBar(text_file):
    total = 916.55 * stat(text_file).st_size
    text_file = text_file.replace(".txt","")
    print(f'Progress: |{"-"*70}| {0.0}% Completed', end = '\r')
    # p_bar = Thread(target = printProgressBar,args=(total,text_file))
    # p_bar.start()
    printProgressBar(total, text_file)

   