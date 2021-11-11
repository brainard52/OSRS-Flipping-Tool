# coding: utf-8
from __future__ import unicode_literals

version = "0.0.1"

import sys
import uno
import time
import threading
import json
from datetime import datetime # wtf is this module structure??
from com.sun.star.sheet import CellFlags

doc = XSCRIPTCONTEXT.getDocument()
cellStd = doc.Sheets['Messages']['A1']
cellErr = doc.Sheets['Messages']['A2']
cellMsg = doc.Sheets['Messages']['A3']

# Operating systems tested on:
# macOS - pip3 installed: yes
# Ubuntu - pip3 installed: yes
# Windows - pip3 installed: no, can install bootstrap pip3: no
try: import requests
except ModuleNotFoundError:
    cellErr.setString("Unable to import requests. Attempting to install it")
    try: import pip
    except ModuleNotFoundError:
        cellErr.setString("Please install the Requests module manually. For instructions on this, please see the Instructions sheet.")
        sys.exit(1)
    else:
        from pip._internal.cli.main import main as pip_entry_point
        pip_entry_point(['install', 'requests'])
        import requests

wiki_url_base = "https://prices.runescape.wiki/api/v1/osrs/"
osrsbox_url_base = "https://api.osrsbox.com/"
headers = {
        "User-Agent": "OSRS-Market-Sheet-"+version+"-By-RSN-IrnLandon",
        }
session = requests.Session()
item_meta = ""

def SpreadsheetStartup():
    x = threading.Thread(target=SpreadsheetDaemon) # Not daemonizing because the main python thread isn't being used for anything. Doing it this way allows a separate thread without the LibreOffice interface waiting for the script to finish. If I were to daemonize the python thread, it would halt as soon as the return after x.start() was hit.
    x.start()
    return

def SpreadsheetDaemon():
    item_meta = OSRSBoxMeta()
    timer_scale = 5
    while(True):
        PopulateItemData()
        time.sleep(30)

    return

def WikiAPI(endpoint="latest"):
    response = session.get(wiki_url_base+endpoint, headers=headers, verify=False)
    cellMsg.setString(response.status_code)
    return json.loads(response.content)

def OSRSBoxMeta():
    endpoint = "items?max_results=50&page="
    page = "1"
    response = session.get(osrsbox_url_base+endpoint+page, headers=headers, verify=False)
    # TODO: Fetch item metadata and craft a list to return
    return

def PopulateItemData():
    dataSheet = doc.Sheets['Data']
    cellName = ""
    cellID = ""
    cellHigh = ""
    cellHighTime = ""
    cellLow = ""
    cellLowTime = ""

    pricesLatest = WikiAPI("latest")
    prices5m = WikiAPI("5m")

    row = 1
    cellName            = dataSheet['A'+str(row)]
    cellID              = dataSheet['B'+str(row)]
    cellAvgHigh         = dataSheet['C'+str(row)]
    cellNewHigh         = dataSheet['D'+str(row)]
    cellNewHighTime     = dataSheet['E'+str(row)]
    cellHighPriceVolume = dataSheet['F'+str(row)]
    cellAvgLow          = dataSheet['G'+str(row)]
    cellNewLow          = dataSheet['H'+str(row)]
    cellNewLowTime      = dataSheet['I'+str(row)]
    cellLowPriceVolume  = dataSheet['J'+str(row)]

    dataSheet.clearContents(CellFlags.ANNOTATION | CellFlags.DATETIME | CellFlags.FORMULA | CellFlags.OBJECTS | CellFlags.STRING | CellFlags.STYLES | CellFlags.VALUE)
    cellName.setString("Item Name")
    cellID.setString("Item ID")
    cellAvgHigh.setString("Average High Price")
    cellNewHigh.setString("Newest High Price")
    cellNewHighTime.setString("New High Price Time")
    cellHighPriceVolume.setString("High Price Volume")
    cellAvgLow.setString("Average Low Price")
    cellNewLow.setString("New Low Price")
    cellNewLowTime.setString("New Low Price Time")
    cellLowPriceVolume.setString("Low Price Volume")
    row +=1

    cellStd.setString("Latest: " + str(len(pricesLatest['data'])) + ", 5m: " + str(len(prices5m['data'])))

    for i in pricesLatest['data']:
        cellMsg.setString(str(i))
        cellName            = dataSheet['A'+str(row)]
        cellID              = dataSheet['B'+str(row)]
        cellAvgHigh         = dataSheet['C'+str(row)]
        cellNewHigh         = dataSheet['D'+str(row)]
        cellNewHighTime     = dataSheet['E'+str(row)]
        cellHighPriceVolume = dataSheet['F'+str(row)]
        cellAvgLow          = dataSheet['G'+str(row)]
        cellNewLow          = dataSheet['H'+str(row)]
        cellNewLowTime      = dataSheet['I'+str(row)]
        cellLowPriceVolume  = dataSheet['J'+str(row)]

        cellName.setString("N/A")
        cellID.setValue(i)

        cellNewHigh.setValue(-1 if pricesLatest['data'][i]['high'] == None
                else pricesLatest['data'][i]['high'])
        cellNewHighTime.setString(datetime.utcfromtimestamp(0).strftime('%Y-%m-%d %H:%M:%S') if pricesLatest['data'][i]['highTime'] == None
                else datetime.utcfromtimestamp(pricesLatest['data'][i]['highTime']).strftime('%Y-%m-%d %H:%M:%S'))
        cellNewLow.setValue(-1 if pricesLatest['data'][i]['low'] == None
                else pricesLatest['data'][i]['low'])
        cellNewLowTime.setString(datetime.utcfromtimestamp(0).strftime('%Y-%m-%d %H:%M:%S') if pricesLatest['data'][i]['lowTime'] == None
                else datetime.utcfromtimestamp(pricesLatest['data'][i]['lowTime']).strftime('%Y-%m-%d %H:%M:%S'))

        if i in prices5m['data']:
            cellAvgHigh.setValue(-2 if prices5m['data'][i]['avgHighPrice'] == None
                    else prices5m['data'][i]['avgHighPrice'])
            cellHighPriceVolume.setValue(-2 if prices5m['data'][i]['highPriceVolume'] == None
                    else prices5m['data'][i]['highPriceVolume'])
            cellAvgLow.setValue(-2 if prices5m['data'][i]['avgLowPrice'] == None
                    else prices5m['data'][i]['avgLowPrice'])
            cellLowPriceVolume.setValue(-2 if prices5m['data'][i]['lowPriceVolume'] == None
                    else prices5m['data'][i]['lowPriceVolume'])
        else:
            cellAvgHigh.setValue(-1)
            cellHighPriceVolume.setValue(-1)
            cellAvgLow.setValue(-1)
            cellLowPriceVolume.setValue(-1)



        row+=1
    return
