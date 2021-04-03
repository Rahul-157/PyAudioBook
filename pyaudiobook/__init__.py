from .audioBook import removeExtraPages,collectFiles,processFile,pdfParser
from .utils import *
from os.path import expanduser,join,exists,abspath 
from sys import platform as PLATFORM
from datetime import datetime

def setDefaultsIfBlank(lang,op,on):
    if not lang:
        lang="en"
    if not op:
        op = expanduser('~')
    else:
        op = getAbsolutePath(op)
    if not on:
        on = "Output_"+datetime.now().strftime("%X").replace(":","_")
    return lang,join(op,on)

class Pdf2Mp3:
    def __init__(self,filename, lang="", out_path="",out_name="",num_threads=""):
        assert filename, "Input Pdf File is required"
        assert filename.split(".")[-1]=="pdf", "Only PDF file is accepted"
        #Todo :  LanguageCheck
        lang,output = setDefaultsIfBlank(lang, out_path, out_name)
        lang = languageCheck(lang)
        self.input = getAbsolutePath(filename)
        assert exists(self.input), "File not found"
        self.lang = lang
        self.output = output+".mp3"
        self.text_file = join(TEMP_LOC,randomName()+".txt")
        self.threads = setThreads(num_threads)
        if not exists(abspath(TEMP_LOC)):
            runCommand(["mkdir " , TEMP_LOC])
    
    def convert(self):
        logger.info("Generating Text...")
        self.generateText()
        logger.info("Text file : "+ self.text_file)
        removeExtraPages(self.text_file)
        logger.info("Conversion Started...")
        processFile(self.text_file,self.lang)   
        logger.info("Wrapping Up...")
        collectFiles(self.text_file,self.output)
        cleanup()
        logger.info("Finished...")
        logger.info("Output File :"+self.output)


    def generateText(self):
        if("linux" in PLATFORM):
            runCommand(["less ",self.input," > ",self.text_file])
        else:
            pdfParser(self.input,self.text_file)
        # Extract Text from Pdf
        f = open(self.text_file)
        text = f.read()
        f.close()
        return text

__all__= ["Pdf2Mp3"]