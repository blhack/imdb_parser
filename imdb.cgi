#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import time
import re
import simplejson
import urllib


def fetch_data(url):
	req = urllib.urlopen(url)
	data = req.read()
	return(data)

def find_showtimes(data):
	soup = BeautifulSoup(data)

	movies = soup.findAll(itemprop="url")
	titles = []
	for movie in movies:
		if movie.has_key("title"):
			if len(movie.getText()) > 0:
				titles.append(str(movie.getText()))

	showtimes = soup.findAll("div", {"class":"showtimes"})
	times = []
	for showtime in showtimes:
		times.append(showtime.getText().split("|"))

	showtimes = {}
	for i in range(0,len(titles)-1):
		showtimes[titles[i]] = times[i] 

	showtimes["modified"] = time.time()

	return(showtimes)

if __name__ == "__main__":
        print "content-type:application/json\n"
        now = time.time()
        try:
                input = open("imdb.json","r")
                saved = input.read()
                showtimes = simplejson.loads(saved)
                modified = showtimes['modified']
        except:
                modified = 0 

        age = now - modified
        if age > 600:
		data = fetch_data(url = "http://www.imdb.com/showtimes/cinema/US/ci0031375/US/85281")
		showtimes = find_showtimes(data)
		print simplejson.dumps(showtimes)
		json = open("imdb.json","w")
		json.write(simplejson.dumps(showtimes))
		json.close()
	else:
		print simplejson.dumps(showtimes)
