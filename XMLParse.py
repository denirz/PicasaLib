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
    RootTree=ET.fromstring(InputString)
    if DEBUG_LEVEL:
        ChildCount=0
    print RootTree.findall('.//*/{http://schemas.google.com/photos/2007}id')
    for gfotoid in RootTree.findall('.//*/{http://schemas.google.com/photos/2007}id'):
#    for gfotoid in RootTree.findall('.//*/{http://schemas.google.com/photos/2007}gphoto:id'):    
        
        print gfotoid.tag
        print gfotoid.text
#        print gfotoid.keys()
        ParentGphoto=gfotoid.findall('.//*/{http://www.w3.org/2005/Atom}entry')
        print ParentGphoto
        
    
    for Child in RootTree.findall('.//*/{http://www.w3.org/2005/Atom}title'):
#        print Child.tag
        ReturnSet=ReturnSet + (Child.text,)

        if  DEBUG_LEVEL:
            print Child.text
            ChildCount=ChildCount+1
    if DEBUG_LEVEL:
        print ChildCount
        print ReturnSet
    
    return ReturnSet 