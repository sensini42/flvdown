a='19 0=18 17(\'2://16.15.3/5/5.14\',\'5\',\'13\',\'12\',\'9\');0.4(\'11\',\'6\');0.4(\'10\',\'z\');0.4(\'y\',\'x\');0.1(\'w\',\'v\');0.1(\'u\',\'2://8.7.3:t/d/s/r.q.p.o-n.m\');0.1(\'l\',\'2://8.7.3/i/k/j.h\');0.1(\'g\',\'f\');0.1(\'e\',\'2\');0.1(\'c\',\'6\');0.b(\'a\');'

u=36

i=46

e='s1|addVariable|http|com|addParam|player|true|divxden|s37||flvplayer|write|autostart||type|video|provider|jpg||cg31ud9gd1fe|00078|image|flv|LOL|XviD|HDTV|S03E16|Fringe|ytuebva4tfzau5lxvzusgfzatnshs3no7eattqak6hnxo|364|file|2576|duration|opaque|wmode|always|allowscriptaccess|allowfullscreen|318|640|swf|vidxden|www|SWFObject|new|var'.split('|')

import re

import string


def convDecToBase(num, base, dd=False):
    if not dd:
        dd = dict(zip(range(36), list(string.digits+string.ascii_lowercase)))
    if num == 0: return ''
    num, rem = divmod(num, base)
    return convDecToBase(num, base, dd)+dd[rem]


def trad(p,a,c,k):
    while(c>0):
        c-=1
        if(k[c]):
            cdtb=str(convDecToBase(c,a))
            if (not cdtb):
                cdtb = str(0)
            regexp = re.compile('\\b'+cdtb+'\\b')
            p = regexp.sub(k[c], p)
    return p


        
## function(p,a,c,k,e,d){
##   while(c--)
##      if(k[c])
##         p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);
##   return p}


l = [i for i in trad(a,u,i,e).split(';') if 'flv' in i][0]
print l.split("'")[-2]

