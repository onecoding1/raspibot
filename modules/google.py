#!/usr/bin/python
import urllib, json

def encode(s):
    try:
        return unicode(s, 'utf-8')
    except:
        try: 
            return s.encode('utf-8')
        except:
            return s.decode('cp1250')

trigger = ["!go","!google"]

def func(line):
    #line = line.split()
    #line = " ".join(line[1::])
    line = encode(line)

    try:
        query = urllib.urlencode({'q': line})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        hits = data['results']
        return urllib.unquote(encode(hits[0]['url'])).decode('utf8')
    except:
        return ""