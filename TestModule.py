#__*__charsert:UTF-8__*__
'''
Created on Dec 9, 2012

@author: denirz
'''
import re


DEBUG_LEVEL=0
import httplib,urllib
#import string  # hope we will avoid to use it  
import re
#from PicasaLib.XMLParse import xmlmparse 
from XMLParse import  ListOfAlbums 


def  GetInitialFromPicasa (AuthKey,Picasa_Url):
    Picasa_Host='picasaweb.google.com'
    Pic_Connection=httplib.HTTPSConnection(Picasa_Host)
    Pic_Connection.set_debuglevel(DEBUG_LEVEL)
    header=({'Authorization' : 'GoogleLogin auth='+AuthKey,
#              "Content-type":"application/atom+xml",
#             "Accept": "*/*"
             })
    Pic_Connection.set_debuglevel(DEBUG_LEVEL)
    Pic_Connection.request("GET",Picasa_Url,'',header)
    RetAnswer=Pic_Connection.getresponse()
    return RetAnswer.read()  

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
    try:
        LogConnection.request("POST",GoogleLoginUrl,AuthParams,headers)
    except httplib.HTTPResponse as ex:
        print "Error  %s" % ex    
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
    if DEBUG_LEVEL:
        print '\n-------- google Auth Printed ', AuthToken
        
    Picasa_Url_to_get='/data/feed/api/user/denirz'
    xml=GetInitialFromPicasa(AuthToken, Picasa_Url_to_get)
#    print xml

    for AlbName in ListOfAlbums(xml):
            print AlbName
    pass