from apps.main.models import Version, Gamemode, Region
import json


###################################################
#                       VARS                      #
###################################################

VERSIONS = [5.11, 5.14]
GAMEMODES = ["NORMAL_5X5", "RANKED_SOLO"]
REGIONS = ["BR", "EUNE", "EUW", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]


###################################################
#                    ASSERTIONS                   #
###################################################

def assertVersionGamemodeRegion(version=None, gamemode=None, region=None):

    if version and version not in VERSIONS:
        return False

    if gamemode and gamemode not in GAMEMODES:
        return False

    if region and region not in REGIONS:
        return False

    return True


###################################################
#                     FILE I/O                    #
###################################################

def readEntireFile(filename):

    with open(filename, 'r') as my_file:
        return my_file.read()


def writeAllToFile(filename, content):

    with open(filename, 'w') as my_file:
        my_file.write(content)


def getMatchIDs(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))

    filename = 'AP_ITEM_DATASET/{v}/{g}/{r}.json'.format(
        v=version, g=gamemode, r=region)

    return json.loads(readEntireFile(filename))


###################################################
#                      INITS                      #
###################################################

def initAllVersionGamemodeRegion():

    for version in VERSIONS:
        got, created = Version.objects.get_or_create(name=version)

    for gamemode in GAMEMODES:
        got, created = Gamemode.objects.get_or_create(name=gamemode)

    for region in REGIONS:
        got, created = Region.objects.get_or_create(name=region)


def initKMeansRoleJson(filename):

    roles = {}

    roles['marksman'] = [{3031: 1.0}, {3046: 1.0}, {3046: 1.0}, {
        3153: 1.0}, {3087: 1.0}, {3072: 1.0}, {3006: 1.0}]
    roles['support'] = [{2045: 1.0}, {2049: 1.0}, {3401: 1.0}, {
        3069: 1.0}, {3092: 1.0}, {3190: 1.0}, {3222: 1.0}]
    roles['mage'] = [{3089: 1.0}, {3157: 1.0}, {3285: 1.0},
                     {3116: 1.0}, {3135: 1.0}, {3165: 1.0}, {3174: 1.0}]
    roles['tank'] = [{3083: 1.0}, {3143: 1.0}, {3065: 1.0},
                     {3102: 1.0}, {3075: 1.0}, {3068: 1.0}, {3110: 1.0}]
    roles['fighter'] = [{3078: 1.0}, {3153: 1.0}, {3071: 1.0}, {
        3142: 1.0}, {3035: 1.0}, {3074: 1.0}, {3155: 1.0}]

    dataToWrite = json.dumps(roles, sort_keys=True,
                             indent=4, separators=(',', ': '))
    writeAllToFile(filename, dataToWrite)
