#!/usr/bin/python
import re, urllib2, HTMLParser

trigger = "://"

def func(line):
    try:
        isUrl = re.search("(?P<url>https?://[^\s]+)", line).group("url")
        if isUrl:
            url = isUrl
            response = urllib2.urlopen(url)
            html = response.read()
                        
            title_search = re.search('<title>(.*)</title>', html, re.IGNORECASE)

            if title_search:
                title = title_search.group(1)
                h = HTMLParser.HTMLParser()
                title = h.unescape(title)
                try:
                    return unicode(title, 'utf-8')
                except:
                    return title.encode('utf-8')
                    
    except:
        return ""