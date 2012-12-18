#__*__charsert:UTF-8__*__
'''
Created on Dec 9, 2012

@author: denirz
'''
DEBUG_LEVEL=0
Picasa_Host='picasaweb.google.com'
import httplib,urllib
import ssl
#import string  # hope we will avoid to use it  
import re
import optparse
from email.mime.multipart import MIMEMultipart, MIMEBase
#import email.encoders as encoders
#from email import encoders
#from PicasaLib.XMLParse import xmlmparse 
from XMLParse import  ListOfAlbums,ListOfPhotos,UploadedPictureAddres

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
    
def GetInitialFromPicasa (AuthKey,Picasa_Url):
    
    Pic_Connection=httplib.HTTPSConnection(Picasa_Host)
    Pic_Connection.set_debuglevel(DEBUG_LEVEL)
    header=({'Authorization' : 'GoogleLogin auth='+AuthKey,
              "Content-type":"application/atom+xml",
             "Accept": "*/*"
             })
    Pic_Connection.set_debuglevel(DEBUG_LEVEL)
    Pic_Connection.request("GET",Picasa_Url,'',header)
    RetAnswer=Pic_Connection.getresponse()
    return RetAnswer.read()  

def xmlListOfPhotosInAlbum(Auth,PublisherUserID,AlbumID):
    '''
    will return a list of Photos  of  the AlbumID of PUblishedUser
    '''
    GetUrl='/data/feed/api/user/'+PublisherUserID+'/albumid/'+AlbumID
    xml=GetInitialFromPicasa(Auth,GetUrl)
    return xml

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

def PostPhoto(Auth,PublisherUserID,AlbumName,PhotoPath,Title="Default Title",Summary="Set  via Picasa API"):
# POST https://picasaweb.google.com/data/feed/api/user/userID/albumid/albumID
#https://picasaweb.google.com/data/feed/api/user/userID/albumid/albumID
    '''
    Should post the file to the selecter Album
    '''
    ListAlbumUrl='/data/feed/api/user/'+PublisherUserID
    AlbumID=Album_IDfromAlbumName(AlbumName,Auth,ListAlbumUrl)
    PostUrl='/data/feed/api/user/'+PublisherUserID+'/albumid/'+AlbumID
#    print "PostUrl:",PostUrl
    #Annotation Forming:
    # To define a spectial Function  for that:
    TextToMime="<entry xmlns='http://www.w3.org/2005/Atom'><title>"
    TextToMime=TextToMime+Title
    TextToMime=TextToMime+"</title><summary>"
    TextToMime=TextToMime+Summary
    TextToMime=TextToMime+"</summary><category scheme='http://schemas.google.com/g/2005#kind' term='http://schemas.google.com/photos/2007#photo'/></entry>"

    # Creating a connection 
    Pic_Connection=httplib.HTTPSConnection(Picasa_Host)
    Pic_Connection.set_debuglevel(DEBUG_LEVEL)
    header=({'Authorization' : 'GoogleLogin auth='+Auth,
              "Content-type":"multipart/related;boundary=END_OF_PART",
             "Accept": "*/*",
             "MIME-Version":"1.0"
             })
    
    # Creating Multipart Container 
    Msg=MIMEMultipart("related","END_OF_PART")
    # Creatinf XML part
    XmlToAdd=MIMEBase("application","atom+xml")
    XmlToAdd.set_payload(TextToMime)
    Msg.attach(XmlToAdd)
    
    #Creating Image part
    FilePath=PhotoPath
#    FilePath='/Users/denirz/Pictures/Keni.jpg'
    basefile=MIMEBase("image","jpeg")
    Fd=open(FilePath,'rb')
    basefile.set_payload(Fd.read())
    Fd.close() 
    Msg.attach(basefile)
    
    #now message is ready, so  let's  generate string to post:
    DataToSend=Msg.as_string()
    if DEBUG_LEVEL:
        print "see content in ./message.txt file"
        MsgFile=open('./message.txt','w')
        MsgFile.write(DataToSend)
        MsgFile.close()
    
    # now sending rewuest 
    Pic_Connection.request("POST",PostUrl,DataToSend,header)
    RetAnswer=Pic_Connection.getresponse()
    
#    print RetAnswer.getheaders()
#    xmlFilePut=open('./post.xml','wb')
#    xmlFilePut.write(RetAnswer.read())
#    xmlFilePut.close()
    
    address=UploadedPictureAddres(RetAnswer.read())
    return address  

def Test_main():
    AuthToken=GoogleAuth('denirz@gmail.com','--')
    if DEBUG_LEVEL:
        print '\n-------- google Auth Printed ', AuthToken

 
    # List of albums:
#    Picasa_Url_to_get='/data/feed/api/user/osoldatova@mail.ru'
    Picasa_Url_to_get='/data/feed/api/user/denirz'
    xml=GetInitialFromPicasa(AuthToken, Picasa_Url_to_get)
#    print xml
    Lalbums=ListOfAlbums(xml)
    print  "list of Albums", Lalbums
#    for Album in Lalbums.keys():
#        print "Name:\t",Album, "AlbumID\t", Lalbums[Album]
        
        
    #Album Selection:
#    AlbumN='Kondratiev'
#    AlbumN='MarsEdit Images'
    AlbumN='denirz Blog'
#    AlbumN='8/13/11'
#    AlbumN=u'\u041a\u0438\u0440\u0438\u0437\u043b\u0438\u0435\u0432\u044b'
    print  AlbumN
    # AlbumID from name:
    AlbumID=Album_IDfromAlbumName(AlbumN,AuthToken,'/data/feed/api/user/denirz')
    print "AlbumID:",AlbumID
#    List of Photo 
    xml=xmlListOfPhotosInAlbum(AuthToken,'denirz',AlbumID)
#    print xml
    Photos=ListOfPhotos(xml)
    for i in Photos.keys():
        print i,Photos[i]

    print "Main:PostPhoto"
#    PhotoPath='/Users/denirz/Pictures/MTSMusor/DSC_0795.JPG'
    print PostPhoto(AuthToken,'denirz',AlbumN,PhotoPath,'Title','DenisSummary')

def ReadOptions():
    '''
    Reads Command Line options and return (args, additional_args)
    Where "additional_args" are filenames to upload 
    '''
    parser=optparse.OptionParser()
    parser.add_option("-v","--verbose",help="Verbouse output",default=0)
    parser.add_option("-n","--name",help="Google Picasa UserName",default='denirz')
    parser.add_option("-p","--password",help="Google Picasa Password",default='')
    parser.add_option("-a","--album",help="Album in Google Picasa",default='denirz Blog')
    parser.add_option("-t","--title",help="Picture Title",default='')
    parser.add_option("-s","--summary",help="Picture Summary, If empty current Date will be here",default='')
    (args,additional_args)=parser.parse_args()
    if len( additional_args)==0:
        print  " no file specified"
#    print args
    return (args,additional_args)


import time
import os.path
def main():
    (Options,Files)=ReadOptions()
  
#    print "Files:",Files
#    print "Options:",Options
#    print Options.name
#    print Options.keys()
#    print Options['name']
#Let's try to authenticate:
    AuthToken=GoogleAuth(Options.name,Options.password)
#    print AuthToken
    if AuthToken=='0':
        print "Can not Auth -  Probably Invalid Username or Password"
        return 0
# Get Album Id  from Album Name:
##     picasa URL:
    UserUrl='/data/feed/api/user/'+Options.name
    AlbumID=Album_IDfromAlbumName(Options.album,AuthToken,UserUrl)
    if AlbumID =='':
        print "Wrong album Name"
        return
#    print Options.album, AlbumID
   
    for File_To_Submit in Files:
        if os.path.isfile(File_To_Submit):
            if Options.summary=='':
                Summary=time.asctime()
            else:
                Summary=Options.summary
            Title=File_To_Submit.split('/')[-1]    
            HostedUrl=PostPhoto(AuthToken,Options.name,Options.album,File_To_Submit,Title,Summary)
            print "\t",File_To_Submit,"\n", HostedUrl
        else:
            print File_To_Submit, "is not a file" 
        
if __name__ == '__main__':
    main()
