#!/usr/bin/python
import urllib, json, re

def encode(s):
    try:
        return unicode(s, 'utf-8')
    except:
        try: 
            return s.encode('utf-8')
        except:
            return s.decode('cp1250')

trigger = "!calc"

def func(line):
    #line = line.split()
    #line = " ".join(line[1::])
    line = encode(line)

    try:
        query = urllib.urlencode({'q': line})
        url = 'http://www.google.com/ig/calculator?%s' %query
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        j = search_results
        j = encode(urllib.unquote(j))
        
        j = re.sub(r"{\s*(\w)", r'{"\1', j)
        j = re.sub(r",\s*(\w)", r',"\1', j)
        j = re.sub(r"(\w):", r'\1":', j)
		
        results = json.loads(j)
        return encode(results['lhs'] + " = " + results['rhs'])
    except:
        return ""