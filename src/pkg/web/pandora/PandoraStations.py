from __init__ import *

from pkg.String import String
from pkg.DOM import DOM

from pkg.web.Pandora import Pandora

class PandoraStations(Pandora):
    # <List> of stations
    __stations = [] # <List>Dict{"name": $stationName, "id": $stationId}
    
    def set_profile_username(self, name):
        """ Init or set a new username 
        Also means to reset the __stations
        """
        self.profileUsername = name
        self.__stations = []
    
    def scan(self):
        """ Scan the stations page and retrieve all stations to __stations
        @return bool: True if the account contains some stations
            False if something wrong, e.g. incorrect profileUsername, or no station found
        """
        preURL = self.STATIONS_VIEW_BASE_URL
        preURL = preURL.replace("[username]", str(self.profileUsername))
        url = self.STATIONS_REQUEST_BASE_URL
        url = url.replace("[username]", str(self.profileUsername))
        
        try:
            html = self.get_request(preURL)
            html = self.get_request(url)
        except:
            # there must be something wrong with the url, i.e. incorrect profile username
            return False
        
        elements = DOM.get_elements("div", {"class":"infobox-body"}, html)
        for e in elements:
            stationNodes = DOM.get_elements("a", {"href":"/station/[0-9]+"}, e.nodeValue)
            if len(stationNodes)==0:
                continue
            stationNode = stationNodes[0]
            stationName = String.decode_html_entities(stationNode.nodeValue)
            stationId = stationNode.get_attr("href").split('/')[2].strip() 
            self.__stations.append({"name":stationName, "id":stationId})
        return True
    
    def list_stations(self):
        count = 0
        for s in self.__stations:
            count += 1
            print str(count)+". " + s["name"]
            
    def get_count(self):
        return len(self.__stations)
    
    def get_station(self, idx):
        return self.__stations[idx]
    
    def get_null_station(self):
        return {"name":"", "":"id"}