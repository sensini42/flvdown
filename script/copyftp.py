#!/sw/bin/python
# -*- coding: utf-8 -*-

import sys, os, ftplib
from optparse import OptionParser

usage = 'usage: %prog [-q] -p PASSWORD'
parser = OptionParser(usage=usage, version='%prog 1.0.0')
parser.add_option("-q", "--quiet", action="store_false",
    dest="verbose", default=True, help="don't print status message to stdout")

(options, args) = parser.parse_args()

config = {} 
file = os.path.expanduser('~') + '/.config/ftp/ftp.conf'
if os.path.isfile(file):
  fileconf = open(file, 'rb', 0)
  for line in fileconf:
    tmp = line.split('=')
    config[tmp[0]] = tmp[1].replace('"','')[:-1]

if not config:
  print 'check config file:' + file
  sys.exit()

basedirftp = config['ftphomedir']
basedirhome = config['homedir']

ftp = ftplib.FTP(config['ftpurl'])
ftp.login(config['login'], config['password'])

def getFilesFTP(url=''):
  ftp.cwd(basedirftp + '/' + url)
  lstfiles = []
  ftp.dir(lstfiles.append)
  files = []
  for file in lstfiles:
    if file=='..': continue
    files.append(file.split()[-1])
  return set(files)  

def getFiles(url='', dir=False):
  url = basedirhome + '/' + url
  lstfiles = os.listdir(url)
  files = []
  for file in lstfiles:
    if file=='.DS_Store': continue
    if file=='.': continue
    if file=='..': continue
    if dir and os.path.isdir(url + '/' + file):
      files.append(file)
    elif not dir and not os.path.isdir(url + '/' + file):
      files.append(file)
  return set(files)  

def upload(file):
  ext = os.path.splitext(file)[1]
  if ext in ('.srt'):
    ftp.storlines("STOR " + file, open(file))
  else:  
    ftp.storbinary("STOR " + file, open(file, "rb"), 1024)

def upload_all((mkdir, dir, lshows)):
  dirhome = basedirhome + '/' + dir
  if options.verbose: 
    print 'CHDIR: ' + dirhome
  os.chdir(dirhome)
  dirftp = basedirftp + '/' + dir 
  if mkdir:
    if options.verbose: 
      print 'MKD: ' + dirftp 
    ftp.mkd(dirftp)
  ftp.cwd(dirftp)  
  if options.verbose: 
    print 'CWD: ' + dirftp  
  for show in lshows:
    if options.verbose: 
      print 'STOR: ' + show 
    upload(show)

#listshow
listshow = getFiles(dir=True)
listshowftp = getFilesFTP()

filestoup = []

#newshow copier l'ensemble du dossier
newshow = listshow - listshowftp

for newdir in newshow:
  listnewshow = getFiles(newdir)
  if listnewshow: filestoup.append([True, newdir, listnewshow])

#oldshow tester si existe deja sur ftp
oldshow = listshow & listshowftp

for olddir in oldshow:
  listoldshow = getFiles(olddir)
  listoldshowftp = getFilesFTP(olddir)
  newfiles = listoldshow - listoldshowftp
  if newfiles: filestoup.append([False, olddir, newfiles])    

for mdshow in filestoup:
  upload_all(mdshow)

if not filestoup:  
  print 'Nothing to do !!!'

ftp.quit()

