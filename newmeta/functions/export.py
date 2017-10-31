from apps.main.models import Champion, Item
from functions.util import assertVersionGamemodeRegion, writeAllToFile, readEntireFile
import json

"""
This module contains functions which exports our data into JSONs.
"""


def exportChampions(gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(gamemode=gamemode, region=region))

    pre_champs = Champion.objects.filter(
        version__name=5.11,
        gamemode__name=gamemode,
        region__name=region
    ).order_by("name")

    result = []

    for pre_champ in pre_champs:

        if pre_champ.wins == 0 or pre_champ.picks == 0:
            continue

        try:
            post_champ = Champion.objects.get(
                key=pre_champ.key,
                version__name=5.14,
                gamemode__name=gamemode,
                region__name=region
            )
        except:
            continue

        if post_champ.wins == 0 or post_champ.picks == 0:
            continue

        f_pre_picks = float(pre_champ.picks)
        f_pre_wins = float(pre_champ.wins)

        f_post_picks = float(post_champ.picks)
        f_post_wins = float(post_champ.wins)

        dict_to_add = {
            'name': pre_champ.name,
            'id': pre_champ.key,
            'pre_wr': round((f_pre_wins / f_pre_picks) * 100, 2),
            'post_wr': round((f_post_wins / f_post_picks) * 100, 2),
            'pre_pr': round(f_pre_picks / 100.0, 2),
            'post_pr': round(f_post_picks / 100.0, 2),
            'pre_roles': json.loads(pre_champ.roles),
            'post_roles': json.loads(post_champ.roles)
        }
        dict_to_add['d_wr'] = round(
            dict_to_add['post_wr'] - dict_to_add['pre_wr'], 2)
        dict_to_add['d_pr'] = round(
            dict_to_add['post_pr'] - dict_to_add['pre_pr'], 2)

        result.append(dict_to_add)

    dataToWrite = json.dumps(result, sort_keys=True,
                             indent=4, separators=(',', ': '))
    writeAllToFile("./jsons/" + gamemode + "_" + region +
                   "_" + "CHAMPIONS.json", dataToWrite)


def exportItems(gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(gamemode=gamemode, region=region))

    pre_items = Item.objects.filter(
        version__name=5.11,
        gamemode__name=gamemode,
        region__name=region
    ).order_by("name")

    result = []

    for pre_item in pre_items:

        if pre_item.wins == 0 or pre_item.picks == 0:
            continue

        try:
            post_item = Item.objects.get(
                key=pre_item.key,
                version__name=5.14,
                gamemode__name=gamemode,
                region__name=region
            )
        except:
            continue

        if post_item.wins == 0 or post_item.picks == 0:
            continue

        f_pre_picks = float(pre_item.picks)
        f_pre_wins = float(pre_item.wins)

        f_post_picks = float(post_item.picks)
        f_post_wins = float(post_item.wins)

        dict_to_add = {
            'name': pre_item.name,
            'id': pre_item.key,
            'pre_wr': round((f_pre_wins / f_pre_picks) * 100, 2),
            'post_wr': round((f_post_wins / f_post_picks) * 100, 2),
            'pre_pr': round(f_pre_picks / 100.0, 2),
            'post_pr': round(f_post_picks / 100.0, 2)
        }
        dict_to_add['d_wr'] = round(
            dict_to_add['post_wr'] - dict_to_add['pre_wr'], 2)
        dict_to_add['d_pr'] = round(
            dict_to_add['post_pr'] - dict_to_add['pre_pr'], 2)

        result.append(dict_to_add)

    dataToWrite = json.dumps(result, sort_keys=True,
                             indent=4, separators=(',', ': '))
    writeAllToFile("./jsons/" + gamemode + "_" + region +
                   "_" + "ITEMS.json", dataToWrite)


"""
Both funtions are pretty much identical, we can make this better.
"""


def exportRoleItems(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))

    roles_data = readEntireFile(
        './jsons/kmeans/{ver}/{gm}/{reg}/{it}.json'.format(ver=version, gm=gamemode, reg=region, it=8))
    roles_data = json.loads(roles_data)

    result = {}
    roles = ['fighter', 'mage', 'marksman', 'support', 'tank']

    for role in roles[0:1]:

        temp = {}

        for item_set in roles_data[role]:

            for k, v in item_set.iteritems():
                temp[k] = v

        for name, score in sorted(temp.iteritems(), key=lambda (k, v): (-v, k))[:10]:
            print name, score

    print result

#     #dataToWrite = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
#     #writeAllToFile("./jsons/" + gamemode + "_" + region + "_" + str(version) + "_" + "_ROLE_ITEMS.json", dataToWrite)
