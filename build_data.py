"""Join the three source tables into the small files the charts read.

Run once:  python3 build_data.py path/to/australian_postcodes.csv path/to/state_centroids.csv
Sources:
  data/source/aria_winners.csv              Wikipedia ARIA category pages (winners)
  data/source/artist_origins_wikipedia.csv  Wikipedia artist infoboxes (origin / birthplace)
  data/source/abs_erp_2026q1.csv            ABS National, state and territory population, Mar 2026
  australian_postcodes.csv                  github.com/matthewproctor/australianpostcodes
                                            (locality coordinates + ABS remoteness class)
No values are changed; this only looks up coordinates and joins tables.
"""
import csv, json, sys
from collections import Counter

PC_FILE = sys.argv[1]
RA = {"1": "Major city", "2": "Inner regional", "3": "Outer regional", "4": "Remote", "5": "Very remote"}
# locality used for the coordinate lookup when it differs from the infobox name
LOOKUP_NAME = {"Gold Coast": "SURFERS PARADISE", "Nulla Nulla Creek": "KEMPSEY"}
# delivery-area postcode for big cities (avoids PO-box rows with odd coordinates)
PREFERRED_PC = {"Sydney": "2000", "Melbourne": "3000", "Brisbane": "4000", "Perth": "6000",
                "Adelaide": "5000", "Canberra": "2601", "Granville": "2142", "Alice Springs": "0870"}

pc_rows = list(csv.DictReader(open(PC_FILE, encoding="utf-8")))

def geocode(locality, state):
    name = LOOKUP_NAME.get(locality, locality).upper()
    m = [r for r in pc_rows if r["locality"] == name and r["state"] == state]
    if locality in PREFERRED_PC:
        m = [r for r in m if r["postcode"] == PREFERRED_PC[locality]] or m
    m = [r for r in m if r["type"] == "Delivery Area"] or m
    r = m[0]
    # ABS Remoteness Areas: use the 2021 edition; fall back to the 2016 code where 2021 is blank (NT rows)
    names21 = {"Major Cities of Australia": "Major city", "Inner Regional Australia": "Inner regional",
               "Outer Regional Australia": "Outer regional", "Remote Australia": "Remote",
               "Very Remote Australia": "Very remote"}
    ra = names21.get(r["RA_2021_NAME"]) or RA[r["RA_2016"] or r["RA_2011"]]
    return float(r["lat"]), float(r["long"]), ra

origins = {}
for o in csv.DictReader(open("data/source/artist_origins_wikipedia.csv", encoding="utf-8")):
    lat = lon = None
    ra = "Unknown"
    if o["locality"]:
        lat, lon, ra = geocode(o["locality"], o["state"])
    origins[o["artist"]] = {"state": o["state"] or "Unknown", "place": o["locality"] or "",
                            "lat": lat, "lon": lon, "remoteness": ra}

wins = []
for w in csv.DictReader(open("data/source/aria_winners.csv", encoding="utf-8")):
    o = origins[w["lead_artist"]]
    wins.append({"year": int(w["year"]), "category": w["category"], "winner": w["winner"],
                 "work": w["work"], "artist": w["lead_artist"], **o})

with open("data/aria_wins.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["year", "category", "winner", "work", "artist", "state", "place", "lat", "lon", "remoteness"]
    wr = csv.DictWriter(f, fieldnames=cols)
    wr.writeheader()
    for w in sorted(wins, key=lambda d: (d["category"], d["year"])):
        wr.writerow(w)

# quick facts printed for the narrative
print("wins", len(wins), "artists", len({w['artist'] for w in wins}))
print("by state", Counter(w["state"] for w in wins).most_common())
print("by remoteness", Counter(w["remoteness"] for w in wins).most_common())
for c in ["Album of the Year", "Best Group", "Best Country Album"]:
    print(c, Counter(w["remoteness"] for w in wins if w["category"] == c).most_common(),
          Counter(w["state"] for w in wins if w["category"] == c).most_common())
print("top artists", Counter(w["artist"] for w in wins).most_common(12))
print("places", Counter(w["place"] for w in wins).most_common())
pop = {r["state"]: float(r["population_thousands"]) for r in csv.DictReader(open("data/source/abs_erp_2026q1.csv"))}
tot = sum(pop.values()); n = sum(1 for w in wins if w["state"] in pop)
for s in pop:
    k = sum(1 for w in wins if w["state"] == s)
    print(s, k, "win share %.1f" % (100*k/n), "pop share %.1f" % (100*pop[s]/tot), "per million %.2f" % (k/(pop[s]/1000)))
for d in range(1985, 2030, 10):
    sub = [w for w in wins if d <= w["year"] < d + 10]
    if sub:
        print(d, len(sub), "major-city share %.0f%%" % (100*sum(w["remoteness"] == "Major city" for w in sub)/len(sub)))

# ---- helper files for layout (label points, tile-grid positions) and the waffle ----
TILE = {"NT": (0, 1), "QLD": (0, 2), "WA": (1, 0), "SA": (1, 1), "NSW": (1, 2),
        "VIC": (2, 1), "ACT": (2, 2), "TAS": (3, 1)}
ABBR = {r["state_name"]: r["state"] for r in csv.DictReader(open("data/source/abs_erp_2026q1.csv"))}
with open("data/state_points.csv", "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["state", "state_name", "lon", "lat", "tile_row", "tile_col"])
    for r in csv.DictReader(open(sys.argv[2])):
        s = ABBR[r["STATE_NAME"]]
        wr.writerow([s, r["STATE_NAME"], round(float(r["lon"]), 3), round(float(r["lat"]), 3), *TILE[s]])

def hundred(shares):  # largest-remainder rounding to exactly 100 squares
    raw = {k: v * 100 / sum(shares.values()) for k, v in shares.items()}
    n = {k: int(v) for k, v in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - n[k], reverse=True)[:100 - sum(n.values())]:
        n[k] += 1
    return n
order = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]
pw = hundred({s: pop[s] for s in order})
ww = hundred({s: sum(1 for w in wins if w["state"] == s) for s in order})
with open("data/waffle.csv", "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["measure", "square", "state"])
    for label, counts in [("Share of Australians", pw), ("Share of ARIA wins", ww)]:
        i = 0
        for s in order:
            for _ in range(counts[s]):
                wr.writerow([label, i, s]); i += 1
print("waffle pop", pw); print("waffle wins", ww)
