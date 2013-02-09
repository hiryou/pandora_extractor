from __init__ import *

from pkg.String import String
from pkg.DOM import DOM

from pkg.Web import Web

class Emp3World(Web):
    # base url to (GET method) to retrieve results
    __SEARCH_BASE_URL = "http://www.emp3world.com/search/[keyword]_mp3_download.html"
    # min accepted file size in bytes
    __MIN_ACCEPTED_FILE_SIZE = 2048
    
    # keyword to search and search results as a list
    __keyword = ""
    __results = [] # <List>Dict{"title": $trackTitle, "url": $directDownloadUrl}
    __curItemIdx = -1 # current index of selected result item from search
    
    # basic info with where to save
    __saveDir = ""
    __ext = ".mp3"
    
    def __init__(self, keyword = None):
        """ Init a new search
        @param String keyword: 
        """
        if keyword != None:
            self.__new_search(keyword)
            
    def set_save_dir(self, dir):
        self.__saveDir = dir
            
    def set_keyword(self, keyword = None):
        """ Setting a new keyword also means resetting to a new search
        @param String keyword: 
        """
        if keyword != None:
            self.__new_search(keyword)
            
    def __new_search(self, keyword):
        self.__keyword = keyword
        self.__results = []
        self.__curItemIdx = -1
            
    def search(self):
        """ Execute the search
        @return int: number of returned records with respect to the keyword
        """
        searchUrl = self.__create_search_url()
        response = urllib2.urlopen(searchUrl)
        html = response.read()
        elements = DOM.get_elements("div", {"id": "song_[0-9]+", "class": "song_item"}, html)
        for e in elements:
            titleNodes = DOM.get_elements("span", {"id": "song_title"}, e.nodeValue)
            if len(titleNodes)==0:
                continue
            title = titleNodes[0].nodeValue
            playLinkNodes = DOM.get_elements("div", {"class": "play_link"}, e.nodeValue)
            if len(playLinkNodes)==0:
                continue
            playLinkNode = playLinkNodes[0]
            urlNodes = DOM.get_elements("a", {"href": "[^>]+\.mp3"}, playLinkNode.nodeValue)
            if len(urlNodes)==0:
                continue
            url = urlNodes[0].get_attr("href")
            self.__results.append({"title": title, "url": url})
        return len(self.__results)
    
    def download_next(self):
        """ Iterate the results from the current selected item index to attempt
        downloads until an acceptable file is found and successfully retrieved
        @return bool: True if found one, False otherwise
        """
        foundIt = False
        while (self.__curItemIdx+1)<len(self.__results) and not foundIt:
            self.__curItemIdx += 1
            track = self.__results[self.__curItemIdx]
            url = track["url"]
            title = self.__remove_redundant_words(track["title"])
            foundIt = self.download_file(url, self.__saveDir+'/'+title+self.__ext, self.__MIN_ACCEPTED_FILE_SIZE)
        return foundIt
        
    def __create_search_url(self):
        kw = self.__keyword.strip().replace("\s+", ' ');
        kw = kw.replace(' ', '_')
        url = self.__SEARCH_BASE_URL.replace("[keyword]", kw) 
        return url
    
    def __remove_redundant_words(self, str):
        """ Tracks from this website usually titled with a word "mp3" in it
        This function is to remove all redundant words from the track title
        before saving the file to disk
        @param String str:
        @return String: sanitized string 
        """
        removed = re.compile(re.escape("mp3"), re.IGNORECASE)
        str = removed.sub('', str)
        return str.strip()