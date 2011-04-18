
from urllib import urlencode
from urllib2 import Request, build_opener, HTTPCookieProcessor, \
   install_opener, urlopen
from cookielib import LWPCookieJar
from tempfile import NamedTemporaryFile
from os.path import isfile
from glob import glob

def existFile(tvshow, season, episode):
		if(len(episode)==1):
				episode = "0" + episode
		tvshow = '_'.join(tvshow.split()).lower()
		return glob(tvshow + '/' + tvshow + season + episode + '.*')


class NextEpisode():
		""" class to deal with next-episode.net """

		def __init__(self, login, password, dict_bug={}):
				
				# save parameters
				self.login = login
				self.password = password

				
				self.txheaders = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; WinNT)'}
				self.urlbase = 'http://next-episode.net/'
				self.dict_bug = dict_bug

				# take care of cookies
				self.cookieFile = NamedTemporaryFile()
				self.cj = LWPCookieJar()
				opener = build_opener(HTTPCookieProcessor(self.cj))
				install_opener(opener)

		def addDictBug(self, key, value):
				self.dict_bug[key] = value

		def getSrcPage(self, url, txdata=None):

				req = Request(self.urlbase + url, txdata, self.txheaders)
				src = urlopen(req).read()
				self.cj.save(self.cookieFile.name)
				return src

		def connect(self):

				txdata = urlencode({"username": self.login, "password": self.password})

				try:
						self.getSrcPage('userlogin', txdata)
				except:
						raise Exception('Connect Error')


		def getListEpisode(self):
				source = self.getSrcPage('track/')
				if not source:
						return []

				src = source.split('showName">')

				listep = []
				for i in src[1:]:
						lines = i.split('\n')
						if lines[0].endswith("</a>"):
								#else: tvshow not tracked
								item_ep_ondisk = []
								item_ep_notondisk = []
								for i in lines:
										if "removeEpisode" in i:
												tv_name = lines[0][:-4]
												if tv_name in self.dict_bug:
														tv_name = self.dict_bug[tv_name]
												item_se = i.split()[9][1:-2]
												num_ep = i.split()[10][1:-2]
												strlist = i.split("removeEpisode(")[1].split(')')[0]
												epilist = [x[1:-1] for x in strlist.split(', ')[:-1]]
												if not existFile(tv_name, item_se, num_ep):
														item_ep_notondisk.append(num_ep)
												else:
														item_ep_ondisk.append(num_ep)
								if(item_ep_ondisk or item_ep_notondisk):
										listep.append((tv_name, item_se, item_ep_ondisk, \
										    item_ep_notondisk))

				return listep

		def addShow(self, title):
				src = self.getSrcPage('-'.join(title.split(' ')))
				url = src.split('to watchlist')[0].split('"')[-2]
				self.getSrcPage(url)

		def removeEpisode(self, movieId, userId, seasonId, episodeId):
				url = 'PAGES/stufftowatch_files/ajax/ajax_requests_stuff.php'
				txdata = urlencode({"showCat": "episode", \
				                    "movieId": movieId, \
														"userId": userId, \
														"seasonId": seasonId, \
														"episodeId": episodeId, \
														"parsedString": seasonId + "x" + episodeId})
				self.getSrcPage(url, txdata)
				
import sys
if __name__ == '__main__':
		ne = NextEpisode(sys.argv[1], sys.argv[2])
		ne.addDictBug('The Office (US)', 'The Office')
		ne.addDictBug('Brothers & Sisters', 'Brothers and Sisters')
		ne.connect()
		#print ne.getListEpisode()
		#ne.addShow('chelsea lately')
		#ne.removeEpisode('619', '66436', '5', '7')


