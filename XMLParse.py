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
    ReturnDict={}
    RootTree=ET.fromstring(InputString)
  
    for gfotoElement in RootTree.findall('.//*/{http://schemas.google.com/photos/2007}id/..'):
        IDElement=gfotoElement.find('.//{http://schemas.google.com/photos/2007}id')
        IDElement=gfotoElement.find('.//{http://schemas.google.com/photos/2007}id')
        TitleElement=gfotoElement.find('.//{http://www.w3.org/2005/Atom}title')
        ReturnDict[TitleElement.text]=IDElement.text
    if DEBUG_LEVEL:
        print ReturnDict
        print "lenght is:",len(ReturnDict.keys())
    return ReturnDict

def ListOfPhotos(InputString):
    if DEBUG_LEVEL:
        print "list of Photo XML"
        print InputString
    RootTree=ET.fromstring(InputString)
#    f=open('./photo.xml','w')
#    f.write(InputString)
#    f.close
#    print RootTree
    elements=RootTree.findall('.//{http://www.w3.org/2005/Atom}entry')
    ReturnDict={}
    for e in elements:
        Fid=e.find('./{http://schemas.google.com/photos/2007}id').text
        Furl=e.find('./{http://search.yahoo.com/mrss/}group/{http://search.yahoo.com/mrss/}content').attrib['url']
        ReturnDict[Fid]=Furl
    return ReturnDict