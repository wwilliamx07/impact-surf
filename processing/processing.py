from csv import *
from time import *
from pgeocode import *
from json import *
from favicon import *
from google import genai

ident = {}
entries = []

with open("processing/input/ident.csv", newline="", encoding="utf-8-sig") as csvfile:
    rd = reader(csvfile)
    header = next(rd)
    for row in rd:
        bn = row[0]
        entry = {}
        for i in range(len(row)):
            entry[header[i]] = row[i]
        ident[bn] = entry

with open("processing/input/url.csv", newline="", encoding="utf-8-sig") as csvfile:
    rd = reader(csvfile)
    next(rd)
    for row in rd:
        bn = row[0]
        if bn in ident and ident[bn]["City"] == "TORONTO":
            entries.append(ident[bn])
            entries[-1]["url"] = row[-1]

print(f"Imported {len(entries)} entries")

results = []
nomi = Nominatim("ca")

for i in range(len(entries)):
    print(f"Start {i}")
    entry = entries[i]
    data = nomi.query_postal_code(f"{entry["Postal Code"][:3]} {entry["Postal Code"][3:]}")
    entry["lon"] = data.longitude
    entry["lat"] = data.latitude
    results.append(entry)

print(f"Finished getting coordinates of {len(results)} results")
filename = f"processing/output/out_{time()}.js"
print(f"Writing results to {filename}")

with open(filename, "w", newline="", encoding="utf-8-sig") as out:
    out.write(f"const entries = {dumps(results)}")

print("Finished")