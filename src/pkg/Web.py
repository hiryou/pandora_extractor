from __init__ import *

class Web:
    __tmpDir = "tmp" # place to save temp working files like cookies, etc
    __opener = None
    __cookies = None
    
    def __init__(self):
        #self.__cookies = cookielib.CookieJar()
        self.__cookies = cookielib.LWPCookieJar()
        self.__opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.__cookies)
        )
        self.__opener.addheaders = [
            ('User-agent', ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:14.0)'
                           'Gecko/20100101 Firefox/14.0.1'))
        ]
        
        # this is the only special treatment for PandoraStations class
        if self.__class__.__name__ == "PandoraStations":
            ck = cookielib.Cookie(
                version=0, name='at', value='w37g156hi2JBm/qyFezb38/XK+OFmuiaA', 
                port=None, port_specified=False, domain='.pandora.com', 
                domain_specified=False, domain_initial_dot=False, path='/', 
                path_specified=True, secure=False, expires=None, discard=True, 
                comment=None, comment_url=None, rest={'HttpOnly': None}, 
                rfc2109=False
            )
            self.__cookies.set_cookie(ck)
        #self.__cookies.save('mycookies.txt');
        #self.__cookies.load('mycookies.txt');
        
    def get_request(self, url):
        """ Navigate to a webpage url
        @param String url
        @return String: html body, or None if there's a connection problem 
        """
        try:
            response = self.__opener.open(url)
        except:
            return None
        return response.read()
    
    def post_request(self, url, data):
        """ Post data to a page, usually uses when submitting a form
        @param String url: the url where we actually post data to
        @param Dict data: e.g. {"username": $name, "password": $pass} 
        @return String: html body, or None if there's a connection problem 
        """
        data = urllib.urlencode(data)
        try:
            response = self.__opener.open(url, data)
        except:
            return None
        return response.read()
        
    def set_tmp_dir(self, dir):
        self.__tmpDir = dir
        
    def download_file(self, fileUrl, saveUrl, minAcceptedSize=-1):
        """ Attempt to download a file
        @param String fileUrl: the url that returns the file stream if being entered in the 
            browser, e.g. "www.example.com/test.mp3" or "www.example.com/test.php?file_id=123"
        @param String saveUrl: complete url to save to local, e.g. "video/my_download.flv"
        @param int minAcceptedSize: min file size in bytes to accept for download
            left unspecified to accept any file size
        @return bool: True of download succeed, False otherwise  
        """
        print("Creating file: " + saveUrl)
        f = open(saveUrl, "wb")
        print("-- Attempt to download...")
        
        # first of all, try to stream the file
        try: 
            file = urllib2.urlopen(fileUrl)
        except:
            try: 
                file = urllib.urlopen(fileUrl)
            except:
                print("-- Can not retrieve this file. The download will be skipped.")
                f.close()
                try:
                    os.remove(saveUrl)
                except:
                    print "---- !Can not delete this garbage file: " + saveUrl
                return False
            
        # second, check if streaming process goes well and acceptably
        if not self.__download_stream(f, file, minAcceptedSize):
            f.close()
            try:
                os.remove(saveUrl)
            except:
                print "---- !Can not delete this garbage file: " + saveUrl
            return False
        
        # if everything goes fine, these commands will execute
        f.flush()
        f.close()
        return True
    
    def __download_stream(self, f, resp, minAcceptedSize=-1):
        """ Stream the file from remote host to local
        @param fileSource f: e.g. f =  open(localFileSaveUrl, "wb")
        @param fileStream resp: e.g. file = urllib.urlopen(remoteFileStreamUrl)
        @param int minAcceptedSize: min file size in bytes to accept for download
            left unspecified to accept any file size
        @return bool: True if succeed, False if Fail
        """
        try:
            totalSize = int(resp.info().getheader('Content-Length').strip())
        except:
            return False
        
        # check if file size is accepted
        if totalSize/1024. < minAcceptedSize:
            print("---- The file size is less than "+str(minAcceptedSize)+" bytes."+ \
                   " This download will be skipped.")
            return False
        
        currentSize = 0
        CHUNK_SIZE = 32768
        while True:
            data = resp.read(CHUNK_SIZE)
            if not data:
                print("---- Streaming process failed. This download will be skipped.")
                return False
            currentSize += len(data)
            f.write(data)
            sys.stdout.write("---- Downloading "+str(totalSize/1024)+ \
                             " bytes..............................."+ \
                             str(round(float(currentSize*100)/totalSize, 2))+'%\r')
            sys.stdout.flush()
            if currentSize >= totalSize:
                break
        print
        return True
    
    def __parse_headers(self, headerStr):
        print headerStr
        headers = []
        items = headerStr.split("\n")
        for e in items:
            e = e.strip()
            if e == '':
                continue
            parts = e.split(':', 1)
            headers.append((parts[0].strip(), parts[1].strip()))
        return headers