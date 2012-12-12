#__*__charsert:UTF-8__*__
'''
Created on Dec 11, 2012

@author: denirz
'''
import re
import xml.etree.ElementTree as ET 

DEBUG_LEVEL=0
def xmlparse(InputString):
    if DEBUG_LEVEL:
            print "DebuggingMode"
            print InputString
    RootTree=ET.fromstring(InputString)
    print RootTree.tag
    print RootTree.attrib
    print 'RootText:', RootTree.text
    print RootTree.tail
    print RootTree.items()  
    print " Keys:", RootTree.keys()
    print " list", list(RootTree)
    
#    print  " is element", RootTree.iselement()
    print 'childrens:'
    
    
    ChildCount=0
    
    
    for Child in RootTree.findall('{http://www.w3.org/2005/Atom}entry'):
        ChildCount=ChildCount+1
#        print "is element:", Child.iselement()
        print "\t tag:", Child.tag
        print '\t attrib:',Child.attrib
        print '\t text:',Child.text
        print '\t items:',Child.items()
        print '\t keys:',Child.keys()
        print '\t list:', list(Child)
        for Cat in Child.findall('{http://www.w3.org/2005/Atom}title'):
            print Cat.items()
#            print Cat.attrib
#            print Cat.get('{http://www.w3.org/2005/Atom}title')
            print list(Cat)
#        print ' ---end of Child:', Child.tag
    print "ChildCount:", ChildCount
    
    
    ChildCount=0
    
    for Child in RootTree.findall('.//*/{http://www.w3.org/2005/Atom}title'):
#        print Child.tag
        print Child.text
#        strUnicode = eval("u'%s'"%re.escape(Child.text)) 
#        print re.escape(Child.text)
        ChildCount=ChildCount+1
    print ChildCount