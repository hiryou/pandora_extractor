from __init__ import *

from pkg.String import String

from pkg.web.Youtube import Youtube

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

    def set_save_dir(self, dir):
        self.__saveDir = dir
    def set_video_url(self, url):
        self.__videoUrl = url
        return self.__config_video_id()
    
    def download(self) :
        # to keep track of the downloading process
        foundIt = False
        countTrial = 0
    
        # keep trying as best until the file is retrieved
        while (not foundIt) and countTrial < self.__MAX_TRIALS:
            # this trial
            countTrial += 1
            # first off, get the array of all streams (different video formats & qualities)
            streams = self.__get_video_streams_info()
            # then group them by video type, quality to lowest to highest
            for stream in streams:
                url = self.__get_video_stream_url(stream)
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
                    foundIt = self.download_file(url, self.__saveDir+'/'+self.__videoTitle+ext)
                    if foundIt:
                        break;
                if foundIt:
                    break;
            return foundIt
    
    def __config_video_id(self):
        try:
            cleanUrl = self.__videoUrl.split('&', 1)[0].strip()
            self.__videoId = cleanUrl.split("v=")[1].strip()
        except:
            return False
        return True
        
    def __get_video_streams_info(self):
        # prepare to get the streams info of the video
        infoUrl = self.GET_VIDEO_BASE_URL + self.__videoId
        resp = urllib2.urlopen(infoUrl)
        content = resp.read()
        # also, prepare to get the video title
        streams = ""
        for item in content.split('&'):
            if item.find(self.GET_VIDEO_TITLE_PARAM) == 0:
                if self.__videoTitle == '':
                    self.__videoTitle = String.url_decode(item.split('=')[1])
                    self.__videoTitle = self.__videoTitle.replace('+', ' ')
                    self.__videoTitle = self.__videoTitle.replace('/', ' ')
            elif item.find(self.GET_VIDEO_STREAM_PARAM) == 0:
                streams = item.strip()
                if self.__videoTitle != '':
                    break;
        streams = map(lambda stream: String.url_decode("type"+stream), streams.split("type"))[1:]
        return streams
    
    def __get_video_stream_url(self, videoStreamInfo):
        # there're only 2 params contains commas in their values: fexp & sparams
        fexp = self.__extract_arg("[?|&]fexp=[0-9|,]+", videoStreamInfo)
        if (fexp == None):
            return None
        # continue and extract sparams
        sparams = self.__extract_arg("[?|&]sparams=[a-z|,]+", videoStreamInfo)
        if (sparams == None):
            return None
        # continue and extract signature
        signature = self.__extract_arg("[?|&]sig=[A-Z0-9|.]+", videoStreamInfo)
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
        
    def __extract_arg(self, regexArg, url):
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