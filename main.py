from supabase import create_client, Client
import os
import json
import time
from wikidata.client import Client
import wikipedia

SUPABASE_URL = "https://nrjxejxbxniijbmquudy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5yanhlanhieG5paWpibXF1dWR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY3NDMwNTY0NCwiZXhwIjoxOTg5ODgxNjQ0fQ.3u7yTeQwlheX12UbEzoHMgouRHNEwhKmvWLtNgpkdBY"

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

client = Client()

## connect to supabase

_p = supabase.table("dmg_personen_LDES").select("*").execute()
p = _p.json()
p = json.loads(p)

print(len(p["data"]))

import requests

base = (p["data"])
for i in range(0,len(p["data"])):
    try:
        owl = base[i]["LDES_raw"]["object"]["owl:sameAs"]
        for i in range(0, len(owl)):
            if "wikidata" in  owl[i]:
                time.sleep(1)

                # parse wikidata Q number from LDES
                Q = owl[i].split("/")[-1]

                #create link for API request
                link = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+Q+"&format=json"
                f = requests.get(link)
                _json = json.loads(f.text);

                print("-----------DUTCH-------------")
                #dutch
                wikipedia.set_lang("nl")
                print(_json["entities"][Q]["labels"]["nl"]["value"])
                _page = wikipedia.page(_json["entities"][Q]["labels"]["nl"]["value"], auto_suggest=False)

                nl_url = _page.url
                nl_title = _page.title
                nl_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["nl"]["value"])

                print(nl_url)
                print(nl_title)
                print(nl_snippet)

                print("-----------ENGLISH-------------")

                #english
                wikipedia.set_lang("en")
                print(_json["entities"][Q]["labels"]["en"]["value"])
                _page = wikipedia.page(_json["entities"][Q]["labels"]["en"]["value"], auto_suggest=False)

                en_url = _page.url
                en_title = _page.title
                en_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["nl"]["value"])

                print(en_url)
                print(en_title)
                print(en_snippet)

                print("-----------FRENCH-------------")
                # french
                wikipedia.set_lang("fr")
                print(_json["entities"][Q]["labels"]["fr"]["value"])
                _page = wikipedia.page(_json["entities"][Q]["labels"]["fr"]["value"], auto_suggest=False)

                fr_url = _page.url
                fr_title = _page.title
                fr_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["fr"]["value"])

                print(fr_url)
                print(fr_title)
                print(fr_snippet)
                print("------------------------")
                print("------------------------")

    except:
        print("no wikidata for this record")
        #print( base[i]["LDES_raw"]["object"])

## https://github.com/goldsmith/Wikipedia
## https://wikidata.readthedocs.io/en/stable/

#https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q1440151&format=json#