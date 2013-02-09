from __init__ import *

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
            self.__eval_node_value()
            
        def __eval_node_value(self):
            """ Eval the nodeValue being the inner html of the node
            @param String closingTag: the closing tag e.g. </h3>, </div>, </span> 
            """
            html = self.nodeHtml
            str = html[::-1]
            tags = re.findall(">[^<]+/?<", str)
            lenClosingTag = len(tags[0])
            html = html[len(self.__tag):len(html)-lenClosingTag]
            self.nodeValue = html.strip()
            
        def get_attr(self, attrName):
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
    def get_elements(tagName, attributes, html):
        """ Get the <list>DOM.Node satisfying the given attributes
        @param String tagName: e.g. h3, div, span
        @param Dict attributes: e.g {"name":"main", "class":"layout"}, can be {}
        @param String html: the html code containing the elements to find
        @return: <List>DOM.Node   
        """
        # first, build the list of regex representing each attribute
        # e.g. attrs[0] = "class[^>]*=[^>]+clearfix"
        tagName = tagName.lower() 
        attrs = []
        for key, val in attributes.iteritems():
            attrs.append(key+"[^>]*=[^>]+"+val)
            
        # then simply collect a list of all html tags
        allTags = re.findall("</?[^>]+>", html)
        
        # prepare results being <List>DOM.Node
        results = []
        ## loop through all tags to find the matched open tag
        curPos = 0
        for i in range(0, len(allTags)):
            tag = allTags[i]
            tName = DOM.__get_tag_name(tag)
            # if it's a matched open tag
            if tag[0:2]!="</" and tName==tagName and DOM.__contain_all(tag, attrs):
                startPos = html.find(tag, curPos)
                endPos = startPos + DOM.__findCloseTagEndPos(i, allTags, html[startPos:])
                node = DOM.Node(tName, tag, html[startPos:endPos])
                results.append(node)
                curPos = startPos + len(tag) 
        return results
    
    @staticmethod
    def __findCloseTagEndPos(idx, tags, html):
        """ Find the endPos of the correct closing tag of tags[idx] in html
        @param int idx: the index of the open tag in tags
        @param <List>String tags: e.g. a tag element can be like 
                                "<div class="btn_bg clearfix space-b-1 right">"
        @param String html: the html to look into
            !note: html must be prefixed by tags[idx]
        @return int: the endPos of the correct closing tag of tags[idx] in html
        """
        
        # use a stack storing html tags name to achieve this purpose
        # the first element in this stack is the tagname of tags[idx]
        # if the next tag in tags is an open tag, we push it to stack
        #    else if it's a closing tag, we pop items out of the stack until the
        #    popped one matches the found closing tag
        # when the stack becomes empty, we know that we already encountered
        #    the correct closing tag of tags[idx]
        tag = tags[idx]
        tagName = DOM.__get_tag_name(tag)
        stack = [tagName]
        # startPos is where in html to start looking for the next tag
        startPos = html.find(tag, 0) + len(tag)
        # curIdx is the index of current item in tags that is in consideration
        curIdx = idx
        while stack!=[] and curIdx<len(tags)-1:
            curIdx +=1
            curTag = tags[curIdx]
            # curPos is the pos of the next tag found in html
            curPos = html.find(curTag, startPos)
            curTagName = DOM.__get_tag_name(curTag)
            if curTag[0:2] == "</":
                while stack.pop()!=curTagName and stack!=[]:
                    continue
            elif curTag[len(curTag)-2:]!="/>" and curTag[0:4]!="<!--":
                stack.append(curTagName)
            startPos = curPos + len(curTag)
        return curPos + len(curTag)
    
    @staticmethod
    def __contain_all(tag, elements):
        """ Check if all regex elements in elements appear in the string tag
        @param String tag: e.g. <h3 name="main" class="layout">
        @param <List>Regex elements
        @return bool: True if tag contains all of them, False otherwise
        """
        for e in elements:
            if len(re.findall(e, tag)) == 0:
                return False
        return True
    
    @staticmethod
    def __get_tag_name(tag):
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