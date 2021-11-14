#!/usr/bin/env python3 -c "exit()"

## appdirs will be for storing settings and local cache of files if necessary
# import appdirs
import os
import webview
import platform
import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

version = "0.0.1"
wiki_url_base = "https://prices.runescape.wiki/api/v1/osrs/" # Must be followed by one of the following: latest, mapping, 5m, 1h, timeseries
osrsbox_url_base = "https://api.osrsbox.com/"
headers = {
        "User-Agent": "OSRS-Market-tool-"+version+"-By-RSN-IrnLandon"
        }
session = requests.Session()
osrsBoxMeta= {}
wikiLatest = {}
wiki5m = {}
wikiMeta = {}

HTML = """
[$HTML$]
"""

def WikiAPI(endpoint: str):
    response = session.get(wiki_url_base+endpoint, headers=headers, verify=False)
    return json.loads(response.content)

def OSRSBoxMeta():
    page = 1
    max_results = 50
    endpoint = "{}items?max_results={}&page={}"
    # OSRSBox paginates their items endpoint so I cache the most recent items in
    # items.json. I check whether items have been added by fetching page 1 with a
    # single item in it. Then I can compare _meta: total in the local file and the
    # fetched page. If the fetched page has a larger value, I download everything
    # again
    if os.path.isfile("items.json"):
        items = json.loads(open("items.json",'r').read())
        items_check = json.loads(session.get(endpoint.format(osrsbox_url_base,1,page), headers=headers, verify=False).content)
        if items_check["_meta"]["total"] == items["_meta"]["total"]:
            return items

    items = {}
    response = session.get(endpoint.format(osrsbox_url_base,max_results,page), headers=headers, verify=False)
    osrsBoxMeta = json.loads(response.content)
    page+=1
    while page <= math.ceil(osrsBoxMeta["_meta"]["total"] / max_results):
        response = session.get(endpoint.format(osrsbox_url_base,max_results,page), headers=headers, verify=False)
        osrsBoxMeta.update(json.loads(response.content))
        page+=1

    open('items.json','w').write(json.dumps(OSRSBox(), indent=4))
    return items

def init():
    """
    Initializes python environment

    """
    pass

def checkos():
    print(platform.system())

def FetchData():
    """
    Fetches and crafts a JSON object that gets passed back to the document for
    processing.

    """
    wikiLatest = WikiAPI("latest")
    wiki5m = WikiAPI("5m")
    wikiMetaUnord = WikiAPI("mapping")
    osrsBoxMeta = OSRSBoxMeta()

    for item in wikiMetaUnord:
        wikiMeta[str(item["id"])] = {}
        for (index, value) in item.items():
            wikiMeta[str(item["id"])][str(index)] = value

    # Pruning items
    wikiLatestTemp = []
    for item in wikiLatest['data']:
        if item not in wikiMeta:
            wikiLatestTemp.append(item)
    for item in wikiLatestTemp:
        wikiLatest['data'].pop(item)

    return wikiLatest

def SaveSettings():
    """
    Saves settings to a JSON object in user's Application Data directory. This
    is determined by the appdirs module in a platform-independent way.

    """
    pass

def on_closing():
    pass

def on_closed():
    pass

if __name__ == '__main__':
    window = webview.create_window("Landon's Merching Tool", html=HTML)
    window.closing += on_closing
    window.closed += on_closed
    window.expose(checkos)
    window.expose(init)
    window.expose(FetchData)
    window.expose(SaveSettings)
    webview.start(debug=True)
