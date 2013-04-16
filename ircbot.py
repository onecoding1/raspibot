#!/usr/bin/env python

import sys
import os
import socket
import string
import time

import locale
import codecs
import urllib2
import re
import HTMLParser

import json
import urllib

def decode(bytes):
    try:
        text = bytes.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = bytes.decode('iso-8859-1')
        except UnicodeDecodeError:
            text = bytes.decode('cp1252')
    return text


def encode(bytes):
    try:
        unicode(bytes, "ascii")
    except UnicodeError:
        bytes = unicode(bytes, 'utf-8', errors="replace")
    else:    
        bytes = bytes

    try:
        text = bytes.encode('utf-8')
    except UnicodeEncodeError:
        try:
            text = bytes.encode('iso-8859-1')
        except UnicodeEncodeError:
            text = bytes.encode('cp1252')
    return text

def fix_urls(text):
    return re.search("(?P<url>https?://[^\s]+)", text).group("url")
	
def google(q):
    try:
        query = urllib.urlencode({'q': encode(q)})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        #print 'Total results: %s' % data['cursor']['estimatedResultCount']
        hits = data['results']
        #print 'Top %d hits:' % len(hits)
        #for h in hits: print ' ', h['url']
        #print 'For more results, see %s' % data['cursor']['moreResultsUrl']
        #print hits[0]['url']
        return hits[0]['url']
    except:
        return u'N/A'

def calc(q):
    try:
        query = urllib.urlencode({'q': encode(q)})
        url = 'http://www.google.com/ig/calculator?%s' %query
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        j = search_results
        j = re.sub(r"{\s*(\w)", r'{"\1', j)
        j = re.sub(r",\s*(\w)", r',"\1', j)
        j = re.sub(r"(\w):", r'\1":', j)
        j = encode(j)
        results = json.loads(j)
        return results['lhs'] + " = " + results['rhs']
    except:
        return u'N/A'

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

try:
   import cPickle as pickle
except:
   import pickle
import pprint

import string
#string.split(the_string, the_separator)
#the_string.split(the_separator[,the_limit])

def saveData(db, data):
    print db
    output = open('data/' + db + '.pkl', 'wb')
    pickle.dump(data, output)
    output.close()

def loadData(db):

    try:
        pkl_file = open('data/' + db + '.pkl', 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()
    except:
        saveData(db, [] )
        data = []

    return data

modules = []

def loadModule(id):
    print "loading Module [" + id + "]"
    _temp = __import__("modules." + id, globals(), locals(), ['func','trigger'], -1)
    _temp = reload(_temp)
	
    moduleExists=0
    for m in modules:
        if m[0] == id:
            #m = [id, _temp.func, _temp.trigger]
            removeModule(id)
            #moduleExists=1
            break

    if moduleExists == 0:
        modules.append([id, _temp.func, _temp.trigger])

def removeModule(id):
    global modules
    for m in modules:
        if m[0] == id:
            modules.remove(m)
            break

def reloadModule(id):
    removeModule(id)
    loadModule(id)

#loadModule("title")    #url announcer (triggered by a url posted)
loadModule("google")    #google search (!go SEARCHTERM)
loadModule("calc")      #google calc (!calc 1*PI or !calc 1 metre in miles or !calc 1 euro in dollars)
loadModule("shout")     #just a shout module YES YOU HEARD RIGHT

userdata = loadData('users')


HOST="irc.rizon.net"
PORT=6667
NICK="raspibot"
IDENT="onebot"
REALNAME="OneBot"
CHANNEL="#IRCCHANNEL"
readbuffer=""

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))

user = []

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        rawline = line
        nick = string.split(line, "!")
        nick = nick[0]
        nick = nick[1:]
        #print "current nick:" + nick
        msg = line.split(":", 2)
        if len(msg) > 2:
           msg = msg[2]
           #print "msg:" + msg
        else:
            msg = ""
        #print line
        line=string.rstrip(line)
        line=string.split(line)

#print "ID: " + m[0] + " TRIGGER:" + m[2]
                
        for m in modules:
            result = ""
            #print type(m[2])
            if type(m[2]) is list:
                for t in m[2]:
                    if t in msg:
                        result = m[1](msg.replace(t, '').strip())
                        break
            elif m[2] != "":
                if m[2] in msg:
                    result = m[1](msg.replace(m[2], '').strip())
            else:
                result = m[1](msg)

            if result != "":
                s.send("PRIVMSG " + CHANNEL + " :"  + result + " \r\n")

        
        if "/MOTD" in line:
            print "Connecting..."
            time.sleep(5)
            s.send("JOIN " + CHANNEL + " \r\n")
        if line[1] == "353":
            data = string.split(rawline, ":")
            names = string.split(data[2])
            user = user + names
            for u in user:
                print u
        if len(line) == 5 and line[1] == "MODE":
            if line[3] == "+o":
                user = [w.replace(line[4], '@' + line[4]) for w in user]
            if line[3] == "-o":
                user = [w.replace('@' + line[4], line[4]) for w in user]
            #print line[3]
            #print line[4]
        #if "!list" in rawline:
            #for u in user:
            #    s.send("PRIVMSG " + nick + " :" + u + " \r\n")
        #if "linux" in line:
        #    print "<===============Linux==========>"
        #    s.send("PRIVMSG " + CHANNEL + " :I think GNU/Linux is cool!!!RMS IS GOD! \r\n")
        if '@' + nick in user or '+@' + nick in user or '%' + nick in user or '+%' + nick:
            if "!quit" in rawline:
                saveData('users', userdata )
                s.send("QUIT :RIP :( \r\n")
                sys.exit()
            if "!restart" in rawline:
                saveData('users', userdata )
                s.send("QUIT :Brb restarting :3 \r\n")
                restart_program()
            if "!loadModule" in rawline:
                q = msg.split()
                q = " ".join(q[1::])
                try:
                    loadModule(q)
                    s.send("PRIVMSG " + CHANNEL + " :module [" + q + "] loaded \r\n")
                except:
                    s.send("PRIVMSG " + CHANNEL + " :module [" + q + "] could not be loaded \r\n")

            if "!removeModule" in rawline:
                q = msg.split()
                q = " ".join(q[1::])
                try:
                    removeModule(q)
                    s.send("PRIVMSG " + CHANNEL + " :module [" + q + "] removed \r\n")
                except:
                    s.send("PRIVMSG " + CHANNEL + " :module [" + q + "] could not be removed \r\n")
            
        if "!helpdklfjlsjflsjflsjfljslfjlsfjlsjflsjflsdjf" in rawline:
            s.send("PRIVMSG " + nick + " :Raspibot has the following features \r\n")
            s.send("PRIVMSG " + nick + " :to search google use: !go [KEYWORD] OR !google [KEYWORD] \r\n")
            s.send("PRIVMSG " + nick + " :to search wolfram alpha use: !wa [KEYWORD] OR raspibot, compute [KEYWORD] \r\n")
            s.send("PRIVMSG " + nick + " :to use googles calculator and currency converter use !calc [FORMULA OR CURRENCIES] \r\n")
            s.send("PRIVMSG " + nick + " :write in all caps to trigger the shout module \r\n")
            s.send("PRIVMSG " + nick + " :and pls don't be a dick. thx :3 \r\n")
        if "!load" in rawline:
            userdata = loadData('users')
        if "!save" in rawline:
            saveData('users', userdata)

        
			            
        if(line[0]=="PING"):
            s.send("PONG %s\r\n" % line[1])