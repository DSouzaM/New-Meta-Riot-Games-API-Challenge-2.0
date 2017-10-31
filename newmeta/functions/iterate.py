from apps.main.models import Match, Region, Version, Gamemode, Champion, Item
from functions.util import assertVersionGamemodeRegion
import json

"""
We use this module to iterate through all of our data to tally up totals,
ex. how many picks a champion has.
"""


def count_champ(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))

    # if gamemode == "NORMAL_5X5" and region == "NA":
    #     return

    region_object = Region.objects.get(name=region)
    version_object = Version.objects.get(name=version)
    gamemode_object = Gamemode.objects.get(name=gamemode)

    matches = Match.objects.filter(
        region=region_object,
        version=version_object,
        gamemode=gamemode_object
    )
    total = matches.count()

    champions = Champion.objects.filter(
        region=region_object,
        version=version_object,
        gamemode=gamemode_object
    )
    champions.update(wins=0, picks=0)

    for i in xrange(total):

        print "Counting champion for match {i} / {total}".format(i=i, total=total)

        match = matches[i]
        data = json.loads(match.data)

        teams = {
            data['teams'][0]['teamId']: data['teams'][0]['winner'],
            data['teams'][1]['teamId']: data['teams'][1]['winner']
        }

        for player in data['participants']:

            champ_id = player['championId']
            team_id = player['teamId']

            champ = champions.get(key=champ_id)

            champ.picks += 1

            if teams[team_id]:
                champ.wins += 1

            champ.save()


def count_item(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))

    region_object = Region.objects.get(name=region)
    version_object = Version.objects.get(name=version)
    gamemode_object = Gamemode.objects.get(name=gamemode)

    matches = Match.objects.filter(
        region=region_object,
        version=version_object,
        gamemode=gamemode_object
    )
    total = matches.count()

    items = Item.objects.filter(
        region=region_object,
        version=version_object,
        gamemode=gamemode_object
    )
    items.update(wins=0, picks=0)

    for i in xrange(total):

        print "Counting item for match {i} / {total}".format(i=i, total=total)

        match = matches[i]
        data = json.loads(match.data)

        teams = {
            data['teams'][0]['teamId']: data['teams'][0]['winner'],
            data['teams'][1]['teamId']: data['teams'][1]['winner']
        }

        for player in data['participants']:

            team_id = player['teamId']

            for i in xrange(7):

                item = 'item' + str(i)
                itemId = int(player['stats'][item])

                if itemId:
                    try:
                        item = items.get(key=itemId)
                    except:
                        continue

                    item.picks += 1

                    if teams[team_id]:
                        item.wins += 1

                    item.save()
