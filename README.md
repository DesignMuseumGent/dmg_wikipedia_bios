# DMG_Wikipedia_bios
Service that fetches wikipedia biographies in several languages (Dutch, French, English) for agents related to the collection and programming of Design Museum Gent. The results are stored in a Postgres DB, which serves otter services such as the REST-API (https://github.com/designmuseumgent/dmg-rest-api). This service is running inhouse on a recycled (otherwise obsolete) mac Mini which is rebooted to run DEBIAN.

## dependencies

this service runs on top of our Postgres DB (hosted on Supabase). 
we make use of the following open source libraries:
- [wikipedia](https://pypi.org/project/wikipedia/)

## how it works
this service weekly runs over all agent (human and organisations) entities in our public database (exposed via the dmg-rest-api) and checks for updates on Wikipedia articles produced on these entities. 

example log:
```
---------------------------------------------------------------------------
**                       STARTING WIKIPEDIA HARVESTER                    **
---------------------------------------------------------------------------
processing:     0/3842
id:             DMG-A-03682
same as:        https://id.erfgoed.net/personen/4314

---------------------------------------------------------------------------
processing:     1/3842
no wikidata for this record
---------------------------------------------------------------------------
processing:     2/3842
id:             DMG-A-00782
same as:        ['http://www.wikidata.org/entity/Q62059706', 'https://data.rkd.nl/artists/433477']
DUTCH:          Berthold Boeß
ENGLISH:        Berthold Boeß
FRENCH:         Berthold Boeß
{"nl": {"source": "no data", "title": "no data", "snippet": "no data"}, "fr": {"source": "no data", "title": "no data", "snippet": "no data"}, "en": {"source": "no data", "title": "no data", "snippet": "no data"}}
DMG-A-00782
---------------------------------------------------------------------------
```

