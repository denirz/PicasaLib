#__*__charsert:UTF-8__*__
'''
Created on Dec 9, 2012

@author: denirz
'''

DEBUG_LEVEL=0
import httplib,urllib
#import string  # hope we will avoid to use it  
import re
#from PicasaLib.XMLParse import xmlmparse 
from PicasaLib.XMLParse import  xmlparse 


def  GetInitialFromPicasa (AuthKey):
#    print "hello"
#    Picasa_Host='picasaweb.google.com'
#    Picasa_Url='/data/feed/api/user/default?kind=album'
    Picasa_Url='/data/feed/api/user/denirz' 
#    Picasa_Url='http://picasaweb.google.com/home'
    Picasa_Host='picasaweb.google.com'
    Pic_Connection=httplib.HTTPSConnection(Picasa_Host)
    Pic_Connection.set_debuglevel(DEBUG_LEVEL)
#    print "timeout:", Pic_Connection.port
#    QueryParameters=urllib.urlencode({'kind' :'album'})
    header=({'Authorization' : 'GoogleLogin auth='+AuthKey,
#              "Content-type":"application/atom+xml",
#             "Accept": "*/*"
             })
#    Pic_Connection.set_debuglevel(6)
    Pic_Connection.request("GET",Picasa_Url,'',header)
#    Pic_Connection.
    
#    print " ------------------\n"
#    r1=Pic_Connection.getresponse()
#    print r1.read()
    return Pic_Connection.getresponse().read()  

def GoogleAuth(login='denirz@gmail.com',password='pass'):
    GoogleLoginHost='www.google.com'
    GoogleLoginUrl='/accounts/ClientLogin'
# we need an HTTPS Connection to Auth:
    LogConnection=httplib.HTTPSConnection(GoogleLoginHost)
#    LogConnection.set_debuglevel(6)
# Set up parameters
    AuthParams=urllib.urlencode({'Email':login,
                                 'Passwd':password,
                                 'accountType':'GOOGLE',
                                 'source':'Google-cURL-Example',
                                 'service':'lh2'
                                 })
# It Looks like it doesn't work without these headers
    headers = {"Content-type": "application/x-www-form-urlencoded",
                 "Accept": "text/plain"}
    LogConnection.request("POST",GoogleLoginUrl,AuthParams,headers)
    Received=LogConnection.getresponse()
    '''
        Let's check if the answer is  not OK - return 0 and exit 
    '''
    if (Received.status <> 200):
        return "0"
    '''
    now looking for Auth value in response and returning it:
    '''
    DataReceived=Received.read()
    Searchauth=re.compile('Auth=(\S*)')
    g=Searchauth.search(DataReceived)
    AuthToken=g.groups()[0]
    return AuthToken

if __name__ == '__main__':
    AuthToken=GoogleAuth('denirz@gmail.com','shevuqufiwhiz')
    print '\n-------- google Auth Printed ', AuthToken
    xml=GetInitialFromPicasa(AuthToken)
#    print xml
    xmlparse(xml)
    pass