#!/usr/bin/env python3
import sys
import json
import random
import time
import subprocess
import lxml.html as html
from urllib.parse import urlencode

DOMAINSTRING = "https://archiveofourown.org/works/search?"

FANDOMS = [
	"https://archiveofourown.org/media/Anime%20*a*%20Manga/fandoms",
	"https://archiveofourown.org/media/Books%20*a*%20Literature/fandoms",
	"https://archiveofourown.org/media/Cartoons%20*a*%20Comics%20*a*%20Graphic%20Novels/fandoms",
	"https://archiveofourown.org/media/Celebrities%20*a*%20Real%20People/fandoms",
	"https://archiveofourown.org/media/Movies/fandoms",
	"https://archiveofourown.org/media/Music%20*a*%20Bands/fandoms",
	"https://archiveofourown.org/media/Other%20Media/fandoms",
	"https://archiveofourown.org/media/Theater/fandoms",
	"https://archiveofourown.org/media/TV%20Shows/fandoms",
	"https://archiveofourown.org/media/Video%20Games/fandoms" ]

def err_print(*args): print(*args, file=sys.stderr)

def get(url):
	err_print(url)
	time.sleep(random.random() + 0.5)
	while True:
		try:
			return subprocess.check_output(["curl", "-Lfg", "--", url])
		except:
                        time.sleep(1)
                        continue

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
	if elem is None: return 0
	else: return int(elem.text.strip().split(" ")[0])

def populate_fandoms():
	fandoms = []
	for category in FANDOMS:
		fandoms.extend(get_fandoms(parse(get(category))))
	fandoms = set(fandoms)
	with open("fandoms.json", "w") as fp:
		fp.write(json.dumps(list(fandoms), indent=4))

def months(number):
	with open("fandoms.json") as fp:
		fandoms = json.loads(fp.read())
	for fandom in fandoms:
		print(json.dumps(get_fandom_stats(0, number, fandom)))

def total_fandom_works():
	fandoms = {}
	for category in FANDOMS:
		tree = parse(get(category))
		for elem in tree.findall(".//ul[@class='tags index group']/li/a"):
			fandoms[elem.text] = int(elem.tail.strip()[1:-1])
	with open("total_works.json", "w") as fp:
		fp.write(json.dumps(fandoms))

def get_fandom_stats(start, end, fandom):
	Q = urlencode({
		"utf8": "✔",
		"commit": "Search",
		"work_search[revised_at]": "%d-%d months ago" % (start, end),
		"work_search[fandom_names]": fandom })
	works = get_work_count(parse(get(DOMAINSTRING + Q)))
	return { "months_ago": end, "fandom": fandom, "works": works }

def main():
	with open("fandoms.json") as fp:
		fandoms = json.loads(fp.read())
	for i in range(24):
		for fandom in fandoms:
			print(json.dumps(get_fandom_stats(i, i+1, fandom)))

if __name__ == "__main__":
	if len(sys.argv) < 2: main()
	elif sys.argv[1] == "-fandoms":
                populate_fandoms()
	elif sys.argv[1] == "-months" and len(sys.argv) >= 3:
                months(int(sys.argv[2]))
	elif sys.argv[1] == "-total":
                total_fandom_works()
