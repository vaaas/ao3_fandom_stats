#!/usr/bin/env python3
import sys
import json

stats = [json.loads(line) for line in sys.stdin]
total = json.loads(open("total_works.json", "r").read())
stats.sort(key=lambda x: x["works"], reverse=True)

print("####### FANDOMS BY NUMBER OF WORKS")
for i in stats:
	print(i["works"], "\t", i["fandom"])

stats.sort(key=lambda x: x["works"]/total[x["fandom"]], reverse=True)

print("\n", "####### FANDOMS BY RELATIVE WORKS")
for i in stats:
	print(i["works"], "\t", i["fandom"])
