import os
import sys
import time

import cookielib
import urllib, urllib2

import re
import HTMLParser


class String:
    """A designated static class to perform operations on strings""" 
    
    @staticmethod
    def urlDecode(url):
        """Recursively decode an url until there's no url entities left
        @param String url
        @retur String 
        """
        newUrl = urllib2.unquote(url)
        while (url != newUrl):
            url = newUrl
            newUrl = urllib2.unquote(url)
        return url.strip()
    
    @staticmethod
    def countMatchWords(s1, s2):
        """Count how many words of String s1 appear in String s2 (case insensitive)
        @param String s1
        @param String s2
        @return int: number of words in s1 that also appear in s2 
        """
        words = s1.lower().strip().split(' ')
        s2 = s2.lower().strip()
        count = 0
        for word in words:
            if s2.find(word) != -1:
                count += 1
        return count
    
    @staticmethod
    def decodeHtmlEntities(str):
        """Decode all html entities, e.g. "&amp;" -> '&'
        @param String str: string to be decoded
        @return String: the completely decoded string 
        """
        h = HTMLParser.HTMLParser()
        return h.unescape(str).strip()
    
    @staticmethod
    def symbolsToWords(str):
        """Change some special symbols from original string to words, e.g. '&' -> "and"
        @param String str
        @return String: a new string after all symbols have been properly replaced 
        """
        str = str.replace('&', 'and')
        return str.strip()
    

class DOM:
    """A designated static class to process HTML DOM elements"""
    
    class Node:
        """Each HTML DOM element is treated as a DOM.Node"""
        
        nodeName = ""   # e.g. div, span, h3
        nodeHtml = ""   # the outer html of the tag
        nodeValue = ""  # the inner html of the tag
        
        __tag = "" # the complete open tag, e.g. '<h3 class="here" id="there">'
        
        def __init__(self, name, tag, html):
            """ Init a Node
            @param String name: name of the tag e.g. h3, div, span
            @param String tag: the complete tag itself e.g. <h3 class="here" id="there">
            @param String html: the complete outer html containing this tag 
            """
            self.nodeName = name
            self.nodeHtml = html
            self.__tag = tag
            
        def evalNodeValue(self, closingTag):
            """ Actually eval the nodeValue. Designated to be called from within DOM
            @param String closingTag: the closing tag e.g. </h3>, </div>, </span> 
            """
            lenClosingTag = len(closingTag)
            html = self.nodeHtml
            html = html[len(self.__tag):len(html)-lenClosingTag]
            self.nodeValue = html.strip()
            
        def getAttr(self, attrName):
            """ Get an attr value e.g. <h3 class="here"> -> val of attr "class" is "here"
            @param String attrName: name of the attr
            @return String: value of the attribute
            """
            pos = self.__tag.find(attrName) + len(attrName)
            sqStartPos = self.__tag.find("'", pos)
            dqStartPos = self.__tag.find('"', pos)
            quote = ""
            if  sqStartPos==-1 or dqStartPos<sqStartPos:
                quote = '"'
            else:
                quote = "'"
            qStart = self.__tag.find(quote, pos)
            qEnd = self.__tag.find(quote, qStart+1)
            return self.__tag[qStart+1:qEnd].strip()
    
    @staticmethod
    def getElements(tagName, attributes, html):
        """ Get the <list>DOM.Node satisfying the given attributes
        @param String tagName: e.g. h3, div, span
        @param Dict attributes: e.g {"name":"main", "class":"layout"}, can be {}
        @param String html: the html code containing the elements to find
        @return: <List>DOM.Node   
        """
        attrs = []
        for key, val in attributes.iteritems():
            attrs.append(key+"[^>]*=[^>]+"+val)
            
        elements = []
        openTagRegex = '<'+tagName+"[^>]*>"
        tags = re.findall(openTagRegex, html)
        for tag in tags:
            if DOM.__containAll(tag, attrs):
                elements.append(tag)
        if elements == []:
            return []
        
        nextPos = html.find(elements[0])
        for i in range(0, len(elements)):
            tag = elements[i]
            startPos = nextPos
            if i == len(elements)-1:
                endPos = len(html)
            else:
                nextPos = html.find(elements[i+1])
                endPos = nextPos
            elements[i] = {"tag": tag, "html": html[startPos:endPos]}
            
        results = []
        for element in elements:
            tags = re.findall("</?[^>]+>", element["html"])
            elementTagName = DOM.__getTagName(element["tag"])
            stack = [elementTagName]
            tags.pop(0)
            curPos = len(element["tag"]) 
            while stack != []:
                t = tags.pop(0)
                curPos = element["html"].find(t, curPos) + len(t)
                tName = DOM.__getTagName(t)
                if t[0:2] == "</":
                    while stack.pop()!=tName and stack!=[]:
                        continue
                else:
                    stack.append(tName)
                if stack == []:
                    node = DOM.Node(elementTagName, element["tag"], element["html"][0:curPos])
                    node.evalNodeValue(t)
                    results.append(node)
        return results
    
    @staticmethod
    def __containAll(tag, elements):
        """ Check if all string elements in elements appear in the string tag
        @param String tag: e.g. <h3 name="main" class="layout">
        @param <List>Regex
        @return bool: True if tag contains all of them, False otherwise
        """
        for e in elements:
            if len(re.findall(e, tag)) == 0:
                return False
        return True
    
    @staticmethod
    def __getTagName(tag):
        """ Extract the tag name from the complete open tag
        @param String tag: e.g. <h3 name="main" class="layout">
        @return String: the tag name only e.g. h3, dive, span
        """
        tag = tag.replace("</", '')
        tag = tag.replace("<", '')
        tag = tag.replace(">", '')
        tag = tag.replace("\s+", ' ')
        words = tag.strip().split(' ')
        return words[0].strip().lower()
        

class Web:
    __tmpDir = "tmp" # place to save temp working files like cookies, etc
    __cookieFile = "Web.tmp.cookies"
    
    __username = ""
    __password = ""
    
    def setTmpDir(self, dir):
        self.__tmpDir = dir
        
    def setUsername(self, username):
        self.__username = username
        return self
    def setPassword(self, password):
        self.__password = password
        return self
    
    def login(self):
        """ Attempt to login
        @return bool: True if succeed, False if fail
        """
        return True
    
    def downloadFile(self, fileUrl, saveUrl, minAcceptedSize=-1):
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
        if not self.__downloadStream(f, file):
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
    
    def __downloadStream(self, f, resp, minAcceptedSize=-1):
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
            print("---- The file size is less than "+minAcceptedSize+" bytes."+ \
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
            
            
class emp3WorldMp3(Web):
    # base url to (GET method) to retrieve results
    __SEARCH_BASE_URL = "http://www.emp3world.com/search/[keyword]_mp3_download.html"
    # min accepted file size in bytes
    __MIN_ACCEPTED_FILE_SIZE = 2048
    
    # keyword to search and search results as a list
    __keyword = ""
    __results = [] # <List>Dict{"title": $trackTitle, "url": $directDownloadUrl}
    __curItemIdx = -1 # current index of selected result item from search
    
    # basic info with where to save
    __saveDir = "mp3"
    __ext = ".mp3"
    
    def __init__(self, keyword = None):
        """ Init a new search
        @param String keyword: 
        """
        if keyword != None:
            self.__newSearch(keyword)
            
    def setKeyword(self, keyword = None):
        """ Setting a new keyword also means resetting to a new search
        @param String keyword: 
        """
        if keyword != None:
            self.__newSearch(keyword)
            
    def __newSearch(self, keyword):
        self.__keyword = keyword
        self.__results = []
        self.__curItemIdx = -1
            
    def search(self):
        """ Execute the search
        @return int: number of returned records with respect to the keyword
        """
        searchUrl = self.__createSearchUrl()
        response = urllib2.urlopen(searchUrl)
        html = response.read()
        elements = DOM.getElements("div", {"id": "song_[0-9]+", "class": "song_item"}, html)
        for e in elements:
            titleNodes = DOM.getElements("span", {"id": "song_title"}, e.nodeValue)
            if len(titleNodes)==0:
                continue
            title = titleNodes[0].nodeValue
            playLinkNodes = DOM.getElements("div", {"class": "play_link"}, e.nodeValue)
            if len(playLinkNodes)==0:
                continue
            playLinkNode = playLinkNodes[0]
            urlNodes = DOM.getElements("a", {"href": "[^>]+\.mp3"}, playLinkNode.nodeValue)
            if len(urlNodes)==0:
                continue
            url = urlNodes[0].getAttr("href")
            self.__results.append({"title": title, "url": url})
        return len(self.__results)
    
    def downloadNext(self):
        """ Iterate the results from the current selected item index to attempt
        downloads until an acceptable file is found and successfully retrieved
        @return bool: True if found one, False otherwise
        """
        foundIt = False
        while (self.__curItemIdx+1)<len(self.__results) and not foundIt:
            self.__curItemIdx += 1
            track = self.__results[self.__curItemIdx]
            url = track["url"]
            title = track["title"]
            foundIt = self.downloadFile(url, self.__saveDir+'/'+title+self.__ext, self.__MIN_ACCEPTED_FILE_SIZE)
        return foundIt
        
    def __createSearchUrl(self):
        kw = self.__keyword.strip().replace("\s+", ' ');
        kw = kw.replace(' ', '_')
        url = self.__SEARCH_BASE_URL.replace("[keyword]", kw) 
        return url
    
                
class Pandora(Web):
    # account
    LOGIN_POST_URL = ""
    
    # stations info
    STATION_TRACKS_BASE_URL = "http://www.pandora.com/content/station_track_thumbs?stationId=[stationId]&page=true&posFeedbackStartIndex=[startIdx]&posSortAsc=false&posSortBy=date"
    
    
class PandoraStationExtractor(Pandora):
    """ Station Extractor receives a station ID and manage all songs in that station
    """
    
    # station ID and the list of total thumbed up tracks within the station
    __stationId = 0
    __thumbUpTracks = []
    
    __curStartIdx = 0 # replaces the [startIdx] in the STATION_TRACKS_BASE_URL 
    __prevItems = 0 # remember number of items in prev search to know what the __curStartIdx should be
    __curThumbUpTracks = [] # list of tracks in the current pagination
    
    def __init__(self):
        """ Init a new station info
        """
        self.__newStation()
    
    def setStationId(self, stationId):
        """ Setting a new stationId also means resetting to a new station info
        @param int stationId:
        @return bool: True if this station is valid, False otherwise 
        """
        self.__newStation(stationId)
        # temporarily do this to scan to make sure the station contains >0 tracks
        test = self.nextList()
        if test==None:
            return False
        # now reset back to be ready for the actual searching process
        self.__newStation(stationId)
        return True
        
    def __newStation(self, stationId=0):
        self.__stationId = stationId
        self.__thumbUpTracks = []
        self.__curThumbUpTracks = []
        self.__curStartIdx = 0
        self.__prevItems = 0
        
    def nextList(self):
        """ Each time this func is invoked, a next pagination of tracks is loaded
        Then self.getCurTracks should be called to retrieve the current list of tracks
        @return bool: True if this new pagination still contains tracks, 
                      False if no more tracks, i.e. last pagination
                      None if something wrong with the station, e.g. incorrect stationId
        """
        self.__curStartIdx += self.__prevItems
        self.__prevItems = 0
        self.__curThumbUpTracks = []
        
        url = self.STATION_TRACKS_BASE_URL
        url = url.replace("[stationId]", self.__stationId)
        url = url.replace("[startIdx]", str(self.__curStartIdx))
        
        try:
            response = urllib2.urlopen(url)
        except:
            # there must be something wrong with the url, i.e. incorrect url
            return None
        html = response.read()
        elements = DOM.getElements("li", {"data-date": "[0-9]+", "data-artist": "[^>]+"}, html)
        for e in elements:
            trackNodes = DOM.getElements("h3", {}, e.nodeValue)
            if len(trackNodes)==0:
                continue
            trackNode = trackNodes[0]
            songNodes = DOM.getElements("a", {}, trackNode.nodeValue)
            if len(songNodes)<2:
                continue
            song = String.decodeHtmlEntities(songNodes[0].nodeValue)
            song = String.symbolsToWords(song)
            song = self.__removeRedundantWords(song)
            artist = String.decodeHtmlEntities(songNodes[1].nodeValue)
            artist = String.symbolsToWords(artist)
            record = song+' '+artist
            if not record in self.__thumbUpTracks:
                self.__thumbUpTracks.append(record)
                self.__curThumbUpTracks.append(record)
            self.__prevItems += 1
        
        if self.__prevItems == 0:
            return False
        return True
    
    def scan(self):
        """ Quickly scan the station to see how many unique tracks
        Such stats and the list of unique tracks will be printed on screen
        """
        # temporarily do this just to scan for the station stats
        count = 0
        print "Below is the list of unique tracks in your station: "
        print "----------------------------------------------------"
        time.sleep(3)
        while self.nextList():
            for t in self.getCurTracks():
                count += 1
                print str(count)+". " + t
        print "----------------------------------------------------"
        print "This station has a total of " + str(count) + " tracks"
        # reset to a new station to be ready for the actual searching process
        self.__newStation(self.__stationId)
    
    def getCurTracks(self):
        return self.__curThumbUpTracks
    
    def __removeRedundantWords(self, str):
        live = re.compile(re.escape("(live)"), re.IGNORECASE)
        str = live.sub('', str)
        str = str.replace('#', '')
        return str.strip()
        

class Youtube(Web):
    # account
    LOGIN_POST_URL = ""
    
    # videos search base url
    VIDEO_SEARCH_BASE_URL = "http://www.youtube.com/results?search_query="
    
    # video related
    VIDEO_VIEW_BASE_URL = "http://www.youtube.com/watch?v="
    GET_VIDEO_BASE_URL = "http://youtube.com/get_video_info?video_id="
    
    # video stream related
    GET_VIDEO_TITLE_PARAM     = "title"
    GET_VIDEO_STREAM_PARAM     = "url_encoded_fmt_stream_map"
    
    # video streams info
    STREAM_INFO_TYPE_FLV     = "type=video/x-flv"
    STREAM_INFO_TYPE_MP4     = "type=video/mp4"
    STREAM_INFO_TYPE_3GPP    = "type=video/3gpp"
    
class VideoSearcher(Youtube):
    # SYSTEM CONFIGS
    __MAX_TRIALS = 10 # execute search until there'r enough records returned
    __MIN_ACCEPTED_RESULTS = 10 # stop search until we have >= this
    __MIN_WORDS_ACCEPTED = .5 # at least half of the words in the keyword must
                              # be in a search item in order to select that item
    
    # query (usually video title) and search results as a list
    __IGNORE_WORDS = "live cover" # ignore result items which contain any of these words
                                  # use sing space to separate each word
    __keyword = ""
    __query = ""
    __results = []
    __currentItemIdx = -1 # current index of selected result item from search
    # keys for each item in __results
    __KEY_TITLE = "video_title"
    __KEY_URL = "video_url"
    
    # regrex to match each search result element
    __REGEX_SEARCH_RESULT_ITEM = "<li[^>]+data-context-item-id=[^>]+>"
    __REGEX_TITLE_ATTR = "data-context-item-title=\"[^\"]+\""
    __REGEX_ID_ATTR = "data-context-item-id=\"[^\"]+\""
    
    def __init__(self, keyword):
        self.__keyword = keyword.strip().replace("\s+", ' ');
        self.__query = self.__createQuery(keyword)
        
    def search(self):
        countTrial = 0
        accepted = False
        while not accepted and countTrial<self.__MAX_TRIALS:
            countTrial += 1
            response = urllib2.urlopen(self.VIDEO_SEARCH_BASE_URL + self.__query)
            html = response.read()
            elements = re.findall(self.__REGEX_SEARCH_RESULT_ITEM, html)
            if len(elements) >= self.__MIN_ACCEPTED_RESULTS:
                accepted = True
        for e in elements:
            title = re.findall(self.__REGEX_TITLE_ATTR, e)[0].split('=')[1]
            title = title[1:len(title)-1]
            title = title.strip().replace("\s+", ' ');
            if String.countMatchWords(self.__IGNORE_WORDS, title) > 0:
                continue
            vidId = re.findall(self.__REGEX_ID_ATTR, e)[0].split('=')[1]
            vidId = vidId[1:len(vidId)-1]
            vidId = vidId.strip().replace("\s+", ' ');
            self.__results.append({
                self.__KEY_TITLE: title, self.__KEY_URL: self.VIDEO_VIEW_BASE_URL+vidId
            })
        return len(self.__results)
            
    def getNextVideoUrl(self):
        if self.__currentItemIdx == -1:
            url = self.__getFirstMatchVideoUrl()
        else:
            url = self.__getNextVideoUrl()
        return url
    def __getFirstMatchVideoUrl(self):
        maxPoints = .0
        videoUrl = ""
        keyWords = float(len(self.__keyword.split(' ')))
        for i in range(0, len(self.__results)):
            e = self.__results[i]
            title = e[self.__KEY_TITLE]
            points = String.countMatchWords(self.__keyword, title)/keyWords
            if points > maxPoints:
                maxPoints = points
                videoUrl = e[self.__KEY_URL]
                self.__currentItemIdx = i
            elif maxPoints > 0.:
                break
        return videoUrl
    def __getNextVideoUrl(self):
        videoUrl = ""
        keyWords = float(len(self.__keyword.split(' ')))
        for i in range(self.__currentItemIdx+1, len(self.__results)):
            e = self.__results[i]
            title = e[self.__KEY_TITLE]
            points = String.countMatchWords(self.__keyword, title)/keyWords
            if points > self.__MIN_WORDS_ACCEPTED:
                videoUrl = e[self.__KEY_URL]
                self.__currentItemIdx = i
                break
        return videoUrl
        
    # see if we finished trying all results
    def finishedAll(self):
        return self.__currentItemIdx == len(self.__results)-1
            
    def __createQuery(self, kw):
        kw = kw.strip().replace("\s+", ' ');
        kw = kw.replace(' ', '+')
        return kw
    
class VideoDownloader(Youtube):
    # SYSTEM CONFIGS
    __MAX_TRIALS = 10 # try several times until being able to retrieve the file or quit

    # basic info with where to save, input video url, video ID derived from video url
    __saveDir     = "video"
    __videoUrl    = ""
    __videoId     = ""
    
    # video info getting from the get_video_info stream
    __videoTitle = ""
    
    # file urls grouped by video type
    __fileUrls = None
    
    # priority of video type to consider
    __priorityQuality = []
    __effQuality = 1    # 1: consider flv > mp4; -1: otherwise
    __effSize = 1        # 1: consider smaller > bigger; -1: otherwise
    
    def __init__(self, username="", password=""):
        # login to Youtube
        # file urls grouped by video type
        str1 = self.STREAM_INFO_TYPE_FLV
        str2 = self.STREAM_INFO_TYPE_MP4
        str3 = self.STREAM_INFO_TYPE_3GPP
        self.__fileUrls = {str1: [], str2: [], str3: []}
        # priority of video type to consider
        if self.__effQuality == 1:
            self.__priorityQuality = [
                self.STREAM_INFO_TYPE_FLV
                ,self.STREAM_INFO_TYPE_MP4
                #,self.STREAM_INFO_TYPE_3GPP    # we don't consider download for cellphone
            ]
        else:
            self.__priorityQuality = [
                self.STREAM_INFO_TYPE_MP4
                ,self.STREAM_INFO_TYPE_FLV
                #,self.STREAM_INFO_TYPE_3GPP    # we don't consider download for cellphone
            ]

    def setSaveDir(self, dir):
        self.__saveDir = dir
    def setVideoUrl(self, url):
        self.__videoUrl = url
        return self.__configVideoId()
    
    def download(self) :
        # to keep track of the downloading process
        foundIt = False
        countTrial = 0
    
        # keep trying as best until the file is retrieved
        while (not foundIt) and countTrial < self.__MAX_TRIALS:
            # this trial
            countTrial += 1
            # first off, get the array of all streams (different video formats & qualities)
            streams = self.__getVideoStreamsInfo()
            # then group them by video type, quality to lowest to highest
            for stream in streams:
                url = self.__getVideoStreamUrl(stream)
                if url == None:
                    continue;
                if stream.find(self.STREAM_INFO_TYPE_FLV)==0:
                    self.__fileUrls[self.STREAM_INFO_TYPE_FLV].append(url)
                elif stream.find(self.STREAM_INFO_TYPE_MP4)==0:
                    self.__fileUrls[self.STREAM_INFO_TYPE_MP4].append(url)
                else:
                    self.__fileUrls[self.STREAM_INFO_TYPE_3GPP].append(url)
            
            # at the end, reverse each list to make their quality from lowest -> highest
            if self.__effSize == 1:
                for key in self.__fileUrls:
                    self.__fileUrls[key].reverse()
                
            # now start to get the video file
            ext = ""
            #for key in self.__fileUrls:
            for key in self.__priorityQuality:
                if key == self.STREAM_INFO_TYPE_FLV:
                    ext = ".flv"
                elif key == self.STREAM_INFO_TYPE_MP4:
                    ext = ".mp4"
                else:
                    ext = ".3gpp"
                for url in self.__fileUrls[key]:
                    foundIt = self.downloadFile(url, self.__saveDir+'/'+self.__videoTitle+ext)
                    if foundIt:
                        break;
                if foundIt:
                    break;
            return foundIt
    
    def __configVideoId(self):
        try:
            cleanUrl = self.__videoUrl.split('&', 1)[0].strip()
            self.__videoId = cleanUrl.split("v=")[1].strip()
        except:
            return False
        return True
        
    def __getVideoStreamsInfo(self):
        # prepare to get the streams info of the video
        infoUrl = self.GET_VIDEO_BASE_URL + self.__videoId
        resp = urllib2.urlopen(infoUrl)
        content = resp.read()
        # also, prepare to get the video title
        streams = ""
        for item in content.split('&'):
            if item.find(self.GET_VIDEO_TITLE_PARAM) == 0:
                if self.__videoTitle == '':
                    self.__videoTitle = String.urlDecode(item.split('=')[1])
                    self.__videoTitle = self.__videoTitle.replace('+', ' ')
                    self.__videoTitle = self.__videoTitle.replace('/', ' ')
            elif item.find(self.GET_VIDEO_STREAM_PARAM) == 0:
                streams = item.strip()
                if self.__videoTitle != '':
                    break;
        streams = map(lambda stream: String.urlDecode("type"+stream), streams.split("type"))[1:]
        return streams
    
    def __getVideoStreamUrl(self, videoStreamInfo):
        # there're only 2 params contains commas in their values: fexp & sparams
        fexp = self.__extractArg("[?|&]fexp=[0-9|,]+", videoStreamInfo)
        if (fexp == None):
            return None
        # continue and extract sparams
        sparams = self.__extractArg("[?|&]sparams=[a-z|,]+", videoStreamInfo)
        if (sparams == None):
            return None
        # continue and extract signature
        signature = self.__extractArg("[?|&]sig=[A-Z0-9|.]+", videoStreamInfo)
        if (signature == None):
            return None
        signature = signature.replace("sig=", "signature=")
        
        # extract the main url
        info = videoStreamInfo
        info = info.replace(fexp, ''); info = info.replace(sparams, '');
        info = info.replace(signature, '');
        # now split out and sanitize the main url
        temp = info.split("url=")
        url = temp[1]
        url = url.replace(',', '&')
        
        # now split this remaining url by '&' and recombine to ensure no duplicate
        # arguments and no empty arguments
        url = url.replace('?', '&', 1)
        args = url.split('&')
        url = args[0] + '?'
        for arg in args[1:]:
            if arg != '':
                temp = arg.split('=')[0] + '='
                if (url.find(temp) == -1 and temp != "sig"):
                    if url[len(url)-1] != '?':
                        url += '&'
                    url += arg
        url += fexp + signature + sparams
        return url
        
    def __extractArg(self, regexArg, url):
        substrings = re.findall(regexArg, url)
        if (len(substrings)==0):
            return None
        try:
            arg = substrings[0]
            if arg[0] == '?':
                arg[0] = '&'
        except:
            return None
        return arg
        

stationId = "520484469577045057"
extractor = PandoraStationExtractor()
emp3 = emp3WorldMp3()

if extractor.setStationId(stationId):
    extractor.scan()
exit(1)

while extractor.nextList():
    tracks = extractor.getCurTracksList()
    for t in tracks:
        print t; print "-------------------------------------------------------"
        emp3.setKeyword(t)
        if emp3.search() > 0:
            if emp3.download():
                print " --- successful"
            else:
                print " --- no file was found for this track!"
print "Total songs: ", extractor.getTotalSongNumber()
exit(1)

'''     
w = Web()
url = "http://www.emp3world.com/search/Halfway_Gone_Lifehouse_mp3_download.html"
#params = {"phrase": "Halfway Gone Lifehouse", "submit": "Search"}
data = w.getWebpageContent(url);
print data
exit(1)
'''

#videoUrl = "http://www.youtube.com/watch?v=vxIOUJ7by6U"
#videoUrl = "http://www.youtube.com/watch?v=NRQi8rM5OyE"
#videoUrl = "http://www.youtube.com/watch?v=nvZfBobWAhE"
#videoUrl = "http://www.youtube.com/watch?v=MQXWStYcwGs"

#search = VideoSearcher("Rhythm Of Love by Plain White T's")
#search = VideoSearcher("Electric Daisy Violin Lindsey Stirling")
#search = VideoSearcher("Give Me Everything by Pitbull")
#search = VideoSearcher("Wake Me Up When September Ends by Green Day")
#search = VideoSearcher("Hey There Delilah by Plain White T's")

search = VideoSearcher("Halfway Gone by Lifehouse")
vd = VideoDownloader()
if search.search() > 0:
    foundIt = False
    startTime = time.time()
    while not foundIt and not search.finishedAll() and time.time()-startTime<60:
        videoUrl = search.getNextVideoUrl()
        if not vd.setVideoUrl(videoUrl):
            continue;
        foundIt = vd.download()



