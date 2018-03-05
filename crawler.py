#!/usr/bin/env python3
import sys
import json
import urllib.request
import random
import time
import lxml.html as html

QUERYSTRING = "http://archiveofourown.org/works/search?utf8=✓&commit=Search&work_search[revised_at]=%d-%d+months+ago&work_search[fandom_names]=%s"

FANDOMS = [
	"http://archiveofourown.org/media/Anime%20*a*%20Manga/fandoms",
	"http://archiveofourown.org/media/Books%20*a*%20Literature/fandoms",
	"http://archiveofourown.org/media/Cartoons%20*a*%20Comics%20*a*%20Graphic%20Novels/fandoms",
	"http://archiveofourown.org/media/Celebrities%20*a*%20Real%20People/fandoms",
	"http://archiveofourown.org/media/Movies/fandoms",
	"http://archiveofourown.org/media/Music%20*a*%20Bands/fandoms",
	"http://archiveofourown.org/media/Other%20Media/fandoms",
	"http://archiveofourown.org/media/Theater/fandoms",
	"http://archiveofourown.org/media/TV%20Shows/fandoms",
	"http://archiveofourown.org/media/Video%20Games/fandoms" ]

OPENER = urllib.request.build_opener()
OPENER.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; polite fandom work count collection)')]

def err_print(*args): print(*args, file=sys.stderr)

def get(url):
	err_print(url)
	time.sleep(random.random() + 0.5)
	while True:
		try: return OPENER.open(url, timeout=20).read()
		except: continue

def parse(string):
	return html.fromstring(string)

def get_fandoms(tree, minimum=100):
	fandoms = []
	for elem in tree.findall(".//ul[@class='tags index group']/li/a"):
		fandom = elem.text
		works = int(elem.tail.strip()[1:-1])
		if works >= minimum: fandoms.append(fandom)
	return fandoms

def get_work_count(tree):
	elem = tree.find(".//div[@id='main']/h3[@class='heading']")
	if (elem is None):
		return 0
	return int(elem.text.strip().split(" ")[0])

def populate_fandoms():
	fandoms = []
	for category in FANDOMS:
		fandoms.extend(get_fandoms(parse(get(category))))
	fandoms = set(fandoms)
	with open("fandoms.json", "w") as fp:
		fp.write(json.dumps(list(fandoms)))

def three_months():
	with open("fandoms.json") as fp:
		fandoms = json.loads(fp.read())
	for fandom in fandoms:
		print(json.dumps(get_fandom_stats(0, 3, fandom)))

def get_fandom_stats(start, end, fandom):
	works = get_work_count(parse(get(QUERYSTRING % (start, end, fandom))))
	return { "months_ago": end, "fandom": fandom, "works": works }

def main():
	for i in range(24):
		for fandom in fandoms:
			print(json.dumps(get_fandom_stats(i, i+1, fandom)))

if __name__ == "__main__":
	if len(sys.argv) < 2: main()
	elif sys.argv[1] == "-fandoms": populate_fandoms()
	elif sys.argv[1] == "-three": three_months()
