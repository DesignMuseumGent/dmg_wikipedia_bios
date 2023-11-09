from supabase import create_client
import requests
import os
import json
import time
from wikidata.client import Client
import wikipedia
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

print("---------------------------------------------------------------------------")
print("**                       STARTING WIKIPEDIA HARVESTER                    **")
print("---------------------------------------------------------------------------")

supabase: Client = create_client(url, key)

_x = supabase.table('dmg_personen_LDES') \
    .select("*") \
    .execute()

p = _x.json()
p = json.loads(p)

count = len(p["data"])
process = 0

base = (p["data"])
for i in range(0, len(p["data"])):
    print("processing:     " + str(process) + "/" + str(len(p["data"])))
    wikipedia_data = {}
    try:
        owl = base[i]["LDES_raw"]["object"]["owl:sameAs"]
        _id = base[i]["agent_ID"]

        try:
            print("id:             " + str(_id))
            print("same as:        " + str(owl))

            time.sleep(1)
            # parse wikidata Q number from LDES
            Q = owl.split("/")[-1]

            # create link for API request
            link = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + Q + "&format=json"
            f = requests.get(link)
            _json = json.loads(f.text);

            print(" ")

            try:
                # DUTCH
                wikipedia.set_lang("nl")
                _page = wikipedia.page(_json["entities"][Q]["labels"]["nl"]["value"], auto_suggest=False)

                print("DUTCH:          " + str(_json["entities"][Q]["labels"]["nl"]["value"]))

                nl_url = _page.url
                nl_title = _page.title
                nl_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["nl"]["value"])

            except:
                nl_url = "no data"
                nl_title = "no data"
                nl_snippet = "no data"

            try:
                # ENGLISH
                wikipedia.set_lang("en")
                print("ENGLISH:        " + str(_json["entities"][Q]["labels"]["nl"]["value"]))
                _page = wikipedia.page(_json["entities"][Q]["labels"]["en"]["value"], auto_suggest=False)

                en_url = _page.url
                en_title = _page.title
                en_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["nl"]["value"])

            except:
                en_url = "no data"
                en_title = "no data"
                en_snippet = "no data"

            try:
                # FRENCH
                wikipedia.set_lang("fr")
                print("FRENCH:         " + str(_json["entities"][Q]["labels"]["fr"]["value"]))
                _page = wikipedia.page(_json["entities"][Q]["labels"]["fr"]["value"], auto_suggest=False)

                fr_url = _page.url
                fr_title = _page.title
                fr_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["fr"]["value"])

            except:
                fr_url = "no data"
                fr_title = "no data"
                fr_snippet = "no data"


            wikipedia_info = json.dumps({"nl": {"source": nl_url, "title": nl_title, "snippet": nl_snippet},
                                         "fr": {"source": fr_url, "title": fr_title, "snippet": fr_snippet},
                                         "en": {"source": en_url, "title": en_title, "snippet": en_snippet}})


            ## update in supabase.
            supabase.table("dmg_personen_LDES").update({"wikipedia_bios": wikipedia_info}).eq("agent_ID", _id).execute()

        except:
            for i in range(0, len(owl)):
                if "wikidata" in owl[i]:

                    time.sleep(1)
                    # parse wikidata Q number from LDES
                    Q = owl[i].split("/")[-1]

                    # create link for API request
                    link = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + Q + "&format=json"
                    f = requests.get(link)
                    _json = json.loads(f.text);

                    try:
                        #DUTCH
                        wikipedia.set_lang("nl")
                        print("DUTCH:          " + str(_json["entities"][Q]["labels"]["nl"]["value"]))

                        _page = wikipedia.page(_json["entities"][Q]["labels"]["nl"]["value"], auto_suggest=False)

                        nl_url = _page.url
                        nl_title = _page.title
                        nl_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["nl"]["value"])

                    except:
                        nl_url = "no data"
                        nl_title = "no data"
                        nl_snippet = "no data"

                    try:
                        # ENGLISH
                        wikipedia.set_lang("en")
                        print("ENGLISH:        " + str(_json["entities"][Q]["labels"]["en"]["value"]))

                        _page = wikipedia.page(_json["entities"][Q]["labels"]["en"]["value"], auto_suggest=False)

                        en_url = _page.url
                        en_title = _page.title
                        en_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["nl"]["value"])

                    except:
                        en_url = "no data"
                        en_title = "no data"
                        en_snippet = "no data"

                    try:
                        #FRENCH
                        wikipedia.set_lang("fr")
                        print("FRENCH:         " + str(_json["entities"][Q]["labels"]["fr"]["value"]))
                        _page = wikipedia.page(_json["entities"][Q]["labels"]["fr"]["value"], auto_suggest=False)

                        fr_url = _page.url
                        fr_title = _page.title
                        fr_snippet = wikipedia.summary(_json["entities"][Q]["labels"]["fr"]["value"])

                    except:
                        fr_url = "no data"
                        fr_title = "no data"
                        fr_snippet = "no data"


                    wikipedia_info = json.dumps({"nl": {"source": nl_url, "title": nl_title, "snippet": nl_snippet},
                                                 "fr": {"source": fr_url, "title": fr_title, "snippet": fr_snippet},
                                                 "en": {"source": en_url, "title": en_title, "snippet": en_snippet}})
                    print(wikipedia_info)

                    ## update in supabase.
                    print(_id)
                    supabase.table("dmg_personen_LDES").update({"wikipedia_bios": wikipedia_info}).eq("agent_ID",
                                                                                                      _id).execute()

        process = process + 1
        print("---------------------------------------------------------------------------")



    except:
        process = process + 1
        print("no wikidata for this record")
        print("---------------------------------------------------------------------------")

    ## https://github.com/goldsmith/Wikipedia
## https://wikidata.readthedocs.io/en/stable/
