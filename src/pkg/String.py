from __init__ import * 

class String:
    """A designated static class to perform operations on strings""" 
    
    @staticmethod
    def url_decode(url):
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
    def count_match_words(s1, s2):
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
    def decode_html_entities(str):
        """Decode all html entities, e.g. "&amp;" -> '&'
        @param String str: string to be decoded
        @return String: the completely decoded string 
        """
        h = HTMLParser.HTMLParser()
        return h.unescape(str).strip()
    
    @staticmethod
    def symbols_to_words(str):
        """Change some special symbols from original string to words, e.g. '&' -> "and"
        @param String str
        @return String: a new string after all symbols have been properly replaced 
        """
        str = str.replace('&', 'and')
        return str.strip()