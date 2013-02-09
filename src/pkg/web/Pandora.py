from pkg.Web import Web

class Pandora(Web):
    # profile related pages
    LOGIN_POST_URL = ""
    STATIONS_VIEW_BASE_URL = "http://www.pandora.com/profile/stations/[username]"
    STATIONS_REQUEST_BASE_URL = "http://www.pandora.com/content/stations?startIndex=0&webname=[username]"
    
    # station related pages
    STATION_TRACKS_BASE_URL = "http://www.pandora.com/content/station_track_thumbs?stationId=[stationId]&page=true&posFeedbackStartIndex=[startIdx]&posSortAsc=false&posSortBy=date"
    
    # profile stuffs
    profileUsername = ""