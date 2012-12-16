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

def Album_IDfromAlbumName(AlbumName,AuthKey,Picasa_Url):
    '''
     Returns AlbumID from AlbumName
     Auth Key  is neede as Auth  URL to get album
    _Gets_ 
        - Album Name, 
        - Auth Key,
        - Picasa url: (  for exampole /data/deef/api/user/denirz) 
    _returns_
        - Album ID of  the  Album Name
    '''
    if AlbumName == '':
        return ''
    if AuthKey == '' or AuthKey == 0:
        print "EmptyAuthKey"
        return''
    if Picasa_Url == '':
        Picasa_Url='/data/feed/api/user/default'
    xml=GetInitialFromPicasa(AuthKey,Picasa_Url)
    DictOfAlbums=ListOfAlbums(xml)

    if AlbumName in DictOfAlbums.keys():
        return DictOfAlbums[AlbumName]
    else:
        if DEBUG_LEVEL:
            print "not found"
        return '' 
    
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
        Received=LogConnection.getresponse()
    except (httplib.HTTPException,ssl.SSLError) as ex:
        print "Error  %s" % ex    
#    Received=LogConnection.getresponse()
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
    Picasa_Url_to_get='/data/feed/api/user/osoldatova@mail.ru'
    xml=GetInitialFromPicasa(AuthToken, Picasa_Url_to_get)
    print xml
    Lalbums=ListOfAlbums(xml)
    print  Lalbums
    for Album in Lalbums.keys():
        print "Name:\t",Album, "AlbumID\t", Lalbums[Album]

    AlbumN='Kondratiev'
#    AlbumN='8/13/11'
    AlbumN=u'\u041a\u0438\u0440\u0438\u0437\u043b\u0438\u0435\u0432\u044b'
    print  AlbumN
    AlbumID=Album_IDfromAlbumName(AlbumN,AuthToken,'/data/feed/api/user/denirz')
    print AlbumID
       