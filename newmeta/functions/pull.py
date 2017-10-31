from apps.main.models import *
from functions.util import *
import requests
import urllib


############################################################
#  I think the newer versions of the requests module give  #
#  annoying request warnings, we will disable them here.   #
############################################################

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


###################################################
#                       VARS                      #
###################################################

API_MATCH_URL = "https://{region}.api.pvp.net/api/lol/{region}/v2.2/match/{match_id}?api_key={api_key}"
API_STATIC_DATA_URL = "https://{region}.api.pvp.net/api/lol/static-data/{region}/v1.2/{data_type}/?api_key={api_key}"
API_KEY = "7ef5d6cc-917a-4ffe-b31e-1abd46f70374"


###################################################
#                GET DATA FROM API                #
###################################################

def getMatchData(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))

    initAllVersionGamemodeRegion()

    region_object = Region.objects.get(name=region)
    version_object = Version.objects.get(name=version)
    gamemode_object = Gamemode.objects.get(name=gamemode)

    matchIDs = getMatchIDs(version, gamemode, region)

    while matchIDs:

        numMatches = len(matchIDs)
        errorMatches = []

        for i in range(numMatches):

            print "Downloading match {i} / {total} with {n} errors".format(
                i=i,
                total=numMatches,
                n=len(errorMatches)
            ),

            match_id = matchIDs[i]

            try:
                if Match.objects.filter(match_id=match_id, region__name=region):
                    print "~ skipping (already have)"
                    continue

                r = requests.get(
                    API_MATCH_URL.format(
                        region=region.lower(),
                        match_id=match_id,
                        api_key=API_KEY
                    )
                )

                if r.status_code is not 200:
                    raise ValueError(
                        "ERROR, HTTP {s_code}".format(s_code=r.status_code))

                Match(
                    match_id=match_id,
                    region=region_object,
                    version=version_object,
                    gamemode=gamemode_object,
                    data=r.text
                ).save()

                print "~ success"

            except Exception as e:
                print "~ " + str(e)
                errorMatches.append(match_id)
                continue

        matchIDs = errorMatches


def getChampions(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))

    initAllVersionGamemodeRegion()

    region_object = Region.objects.get(name=region)
    version_object = Version.objects.get(name=version)
    gamemode_object = Gamemode.objects.get(name=gamemode)

    r = requests.get(
        API_STATIC_DATA_URL.format(
            region=region.lower(),
            data_type='champion',
            api_key=API_KEY
        )
    )

    if r.status_code is not 200:
        print "HTTP ERROR {s_code}".format(s_code=r.status_code)
        return

    data = r.json()['data']

    for champ in data:

        champ_id = data[champ]['id']
        champ_name = data[champ]['name']

        got, created = Champion.objects.get_or_create(
            key=champ_id,
            name=champ_name,
            region=region_object,
            version=version_object,
            gamemode=gamemode_object
        )


def getItems(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))

    initAllVersionGamemodeRegion()

    region_object = Region.objects.get(name=region)
    version_object = Version.objects.get(name=version)
    gamemode_object = Gamemode.objects.get(name=gamemode)

    r = requests.get(
        API_STATIC_DATA_URL.format(
            region=region.lower(),
            data_type='item',
            api_key=API_KEY
        )
    )

    if r.status_code is not 200:
        print "HTTP ERROR {s_code}".format(s_code=r.status_code)
        return

    data = r.json()['data']

    for item in data:

        item_id = data[item]['id']
        item_name = data[item]['name']

        got, created = Item.objects.get_or_create(
            key=item_id,
            name=item_name,
            region=region_object,
            version=version_object,
            gamemode=gamemode_object
        )


"""
Notice how getChampions and getItems is almost identical?
We can make it better, but that that is of low priority right now.
"""


def getChampionIcons():

    champs = Champion.objects.filter(
        region__name='NA', version__name=5.11, gamemode__name='NORMAL_5X5')
    total = champs.count()

    for i in xrange(total):

        print "Downlading champion icon {i} / {total}".format(i=i, total=total)

        champ = champs[i]
        name = champ.name.replace(" ", "")
        urllib.urlretrieve("http://ddragon.leagueoflegends.com/cdn/5.2.1/img/champion/" +
                           name + ".png", "./img/" + name + ".png")
