#__*__charsert:UTF-8__*__
'''
Created on Dec 11, 2012

@author: denirz
'''
#import re
import xml.etree.ElementTree as ET 

DEBUG_LEVEL=0
def ListOfAlbums(InputString):
    if DEBUG_LEVEL:
            print "DebuggingMode"
            print InputString
    ReturnSet=()
    ReturnDict={}
    RootTree=ET.fromstring(InputString)
  
    for gfotoElement in RootTree.findall('.//*/{http://schemas.google.com/photos/2007}id/..'):
        IDElement=gfotoElement.find('.//{http://schemas.google.com/photos/2007}id')
        TitleElement=gfotoElement.find('.//{http://www.w3.org/2005/Atom}title')
        ReturnDict[TitleElement.text]=IDElement.text
    if DEBUG_LEVEL:
        print ReturnDict
        print "lenght is:",len(ReturnDict.keys())
    return ReturnDict
