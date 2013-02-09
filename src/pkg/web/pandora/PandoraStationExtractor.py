from __init__ import *

from pkg.String import String
from pkg.DOM import DOM

from pkg.web.Pandora import Pandora

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
        self.__new_station()
    
    def set_station_id(self, stationId):
        """ Setting a new stationId also means resetting to a new station info
        @param int stationId:
        @return bool: True if this station is valid, False otherwise 
        """
        self.__new_station(stationId)
        # temporarily do this to scan to make sure the station contains >0 tracks
        test = self.next_list()
        if test==None:
            return False
        # now reset back to be ready for the actual searching process
        self.__new_station(stationId)
        return True
        
    def __new_station(self, stationId=0):
        self.__stationId = stationId
        self.__thumbUpTracks = []
        self.__curThumbUpTracks = []
        self.__curStartIdx = 0
        self.__prevItems = 0
        
    def next_list(self):
        """ Each time this func is invoked, a next pagination of tracks is loaded
        Then self.get_cur_tracks should be called to retrieve the current list of tracks
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
        elements = DOM.get_elements("li", {"data-date": "[0-9]+", "data-artist": "[^>]+"}, html)
        for e in elements:
            trackNodes = DOM.get_elements("h3", {}, e.nodeValue)
            if len(trackNodes)==0:
                continue
            trackNode = trackNodes[0]
            songNodes = DOM.get_elements("a", {}, trackNode.nodeValue)
            if len(songNodes)<2:
                continue
            song = String.decode_html_entities(songNodes[0].nodeValue)
            song = String.symbols_to_words(song)
            song = self.__remove_redundant_words(song)
            artist = String.decode_html_entities(songNodes[1].nodeValue)
            artist = String.symbols_to_words(artist)
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
        @return int: number of scanned tracks
        """
        # temporarily do this just to scan for the station stats
        count = 0
        while self.next_list():
            for t in self.get_cur_tracks():
                count += 1
                print str(count)+". " + t
        # reset to a new station to be ready for the actual searching process
        self.__new_station(self.__stationId)
        # return the number of scanned tracks
        return count
        
    def get_cur_tracks(self):
        return self.__curThumbUpTracks
    
    def __remove_redundant_words(self, str):
        live = re.compile(re.escape("(live)"), re.IGNORECASE)
        str = live.sub('', str)
        str = str.replace('#', '')
        return str.strip()