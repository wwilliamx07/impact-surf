from csv import *

ident = {}
entries = []

with open("input/ident.csv", newline="", encoding="utf-8-sig") as csvfile:
    rd = reader(csvfile)
    header = next(rd)
    for row in rd:
        bn = row[0]
        entry = {}
        for i in range(1, len(row)):
            entry[header[i]] = row[i]
        ident[bn] = entry

with open("input/url.csv", newline="", encoding="utf-8-sig") as csvfile:
    rd = reader(csvfile)
    next(rd)
    for row in rd:
        bn = row[0]
        if bn in ident:
            entries.append(ident[bn])
            entries[-1]["url"] = row[-1]
        
