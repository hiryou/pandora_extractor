from pkg.Web import Web

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