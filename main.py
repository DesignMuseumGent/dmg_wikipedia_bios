from supabase import create_client, Client
import os
import json
import time
from wikidata.client import Client
import wikipedia
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = "https://nrjxejxbxniijbmquudy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5yanhlanhieG5paWpibXF1dWR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY3NDMwNTY0NCwiZXhwIjoxOTg5ODgxNjQ0fQ.3u7yTeQwlheX12UbEzoHMgouRHNEwhKmvWLtNgpkdBY"
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

## connect to supabase

_p = supabase.table("dmg_personen_LDES").select("*").execute()
p = _p.json()
p = json.loads(p)

print(len(p["data"]))

import requests

base = (p["data"])
for i in range(0,len(p["data"])):
    wikipedia_data = {}
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

                try:
                    print("-----------DUTCH-------------")
                    wikipedia.set_lang("nl")
                    print(_json["entities"][Q]["labels"]["nl"]["value"])
                    _page = wikipedia.page(_json["entities"][Q]["labels"]["nl"]["value"], auto_suggest=False)

                    nl_url = _page.url
                    nl_title = _page.title
                    nl_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["nl"]["value"])

                except:
                    nl_url = "no data"
                    nl_title = "no data"
                    nl_snippet = "no data"

                try:
                    print("-----------ENGLISH-------------")
                    wikipedia.set_lang("en")
                    print(_json["entities"][Q]["labels"]["en"]["value"])
                    _page = wikipedia.page(_json["entities"][Q]["labels"]["en"]["value"], auto_suggest=False)

                    en_url = _page.url
                    en_title = _page.title
                    en_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["nl"]["value"])

                except:
                    en_url = "no data"
                    en_title = "no data"
                    en_snippet = "no data"

                try:
                    print("-----------FRENCH-------------")
                    wikipedia.set_lang("fr")
                    print(_json["entities"][Q]["labels"]["fr"]["value"])
                    _page = wikipedia.page(_json["entities"][Q]["labels"]["fr"]["value"], auto_suggest=False)

                    fr_url = _page.url
                    fr_title = _page.title
                    fr_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["fr"]["value"])

                except:
                    fr_url = "no data"
                    fr_title = "no data"
                    fr_snippet ="no data"

                print("------------------------")

                wikipedia_info = json.dumps({"nl":{"source": nl_url, "title": nl_title, "snippet": nl_snippet},
                                             "fr":{"source": fr_url, "title": fr_title, "snippet": fr_snippet},
                                             "en":{"source": en_url, "title": en_title, "snippet": en_snippet }})
                print(wikipedia_info)

                print("------------------------")

    except:
        print("no wikidata for this record")
        #print( base[i]["LDES_raw"]["object"])

## https://github.com/goldsmith/Wikipedia
## https://wikidata.readthedocs.io/en/stable/
