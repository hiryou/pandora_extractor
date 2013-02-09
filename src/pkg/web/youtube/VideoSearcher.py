from __init__ import *

from pkg.String import String

from pkg.web.Youtube import Youtube

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
        self.__query = self.__create_query(keyword)
        
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
            if String.count_match_words(self.__IGNORE_WORDS, title) > 0:
                continue
            vidId = re.findall(self.__REGEX_ID_ATTR, e)[0].split('=')[1]
            vidId = vidId[1:len(vidId)-1]
            vidId = vidId.strip().replace("\s+", ' ');
            self.__results.append({
                self.__KEY_TITLE: title, self.__KEY_URL: self.VIDEO_VIEW_BASE_URL+vidId
            })
        return len(self.__results)
            
    def get_next_video_url(self):
        if self.__currentItemIdx == -1:
            url = self.__get_first_match_video_url()
        else:
            url = self.__get_next_video_url()
        return url
    def __get_first_match_video_url(self):
        maxPoints = .0
        videoUrl = ""
        keyWords = float(len(self.__keyword.split(' ')))
        for i in range(0, len(self.__results)):
            e = self.__results[i]
            title = e[self.__KEY_TITLE]
            points = String.count_match_words(self.__keyword, title)/keyWords
            if points > maxPoints:
                maxPoints = points
                videoUrl = e[self.__KEY_URL]
                self.__currentItemIdx = i
            elif maxPoints > 0.:
                break
        return videoUrl
    def __get_next_video_url(self):
        videoUrl = ""
        keyWords = float(len(self.__keyword.split(' ')))
        for i in range(self.__currentItemIdx+1, len(self.__results)):
            e = self.__results[i]
            title = e[self.__KEY_TITLE]
            points = String.count_match_words(self.__keyword, title)/keyWords
            if points > self.__MIN_WORDS_ACCEPTED:
                videoUrl = e[self.__KEY_URL]
                self.__currentItemIdx = i
                break
        return videoUrl
        
    # check if we finished trying all results
    def finished_all(self):
        return self.__currentItemIdx == len(self.__results)-1
            
    def __create_query(self, kw):
        kw = kw.strip().replace("\s+", ' ');
        kw = kw.replace(' ', '+')
        return kw