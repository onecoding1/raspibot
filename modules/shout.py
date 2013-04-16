#!/usr/bin/python
import os, sys, string, random

trigger=""

#if msg.upper() == msg:
#    print "UPPERCASE"
#if msg2.upper() == msg2:
#    print "UPPERCASE"	

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
        if random.randrange(num + 2): continue
        line = aline
    return line

def func(line):
    if line == line.upper() and len(line) > 10 and line != "( ≖‿≖)":
        f = open('data\shout.txt', 'a')
        f.write(line+'\n')
        f.close()
    
        f = open('data\shout.txt', 'r')
        data = random_line(f)
        f.close()
        return data
    else:
        return ""