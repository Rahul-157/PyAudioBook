from .audioBook import *
from .utils import *
from os.path import expanduser,join,exists,abspath
from os import system
from sys import platform as PLATFORM
from datetime import datetime
def SetDefaultsIfBlank(lang,op,on,th):
    if not lang:
        lang="en"
    if not op:
        op = expanduser('~')
    if not on:
        on = "Output_"+datetime.now().strftime("%X").replace(":","_")
    if not th:
        th = THREADS
    else:
        assert int(th)>0, "Number of Threads Should be Greate than 0"
        th = int(th)
    return lang,join(op,on),th

class Pdf2Mp3:
    def __init__(self,filename, lang="", out_path="",out_name="",NumThreads=""):
        assert filename, "Input Pdf File is required"
        lang,output,NumThreads = SetDefaultsIfBlank(lang, out_path, out_name, NumThreads)
        lang = language_check(lang)
        self.input = abspath(filename)
        self.lang = lang
        self.output = output+".mp3"
        self.textFile = join(TEMP_LOC,random_name()+".txt")
        self.generateText()
        logger.info("Text file : "+ self.textFile)
        remove_extra_pages(self.textFile)
        process_file(self.textFile,NumThreads,lang)
        collect_files(self.textFile,self.output)
        cleanup()
    

    def generateText(self):

        if("linux" in PLATFORM):
            if not exists(abspath(TEMP_LOC)):
                system("mkdir " + TEMP_LOC)
            system("less "+self.input+" > "+self.textFile)
        else:
            pdfparser(self.input,self.textFile)

__all__= ["Pdf2Mp3"]