from apps.main.models import Champion, Match
from functions.util import assertVersionGamemodeRegion, readEntireFile, getMatchIDs, writeAllToFile, initKMeansRoleJson
import json
import os

#######################################################
#                        VARS                         #
#######################################################

# Items we potentially want to ignore
ITEMS_TO_IGNORE = set([2041, 2003, 2004, 2047, 2052, 2010])


###################################################
#                 HELPER FUNCTIONS                #
###################################################

"""
This returns a list of dictionaries containing a player's champion id and his items
"""


def getMatchItems(match_id, region):

    region = region.upper()
    assertVersionGamemodeRegion(region=region)

    match = Match.objects.get(match_id=match_id, region__name=region)

    data = json.loads(match.data)
    result = []

    for player in data['participants']:

        player_dict = {
            'champion': int(player['championId']),
            'items': []
        }

        for i in xrange(7):

            item = 'item' + str(i)
            itemId = int(player['stats'][item])

            if itemId:
                player_dict['items'].append(itemId)

        result.append(player_dict)

    return result


"""
Returns the score of a player's item set relative to a role
"""


def getScore(player, role):

    score = 0.0

    for role_item in role:

        for item_id, points in role_item.iteritems():

            if int(item_id) in player['items']:
                score += points

    return score


"""
Returns the best role for a player's item set given the scores for each role.

If the best role has a score of 0, or there is a tie we will skip this player.

A better way to implement this function is to sort descending,
take [0], and see if [1]'s score is the same.
"""


def getBestRole(scores):

    best_role_score = [None, 0.0]
    numberOfTopRoles = 0

    for role_score in scores:

        if role_score[1] > best_role_score[1]:
            best_role_score = role_score

    for role_score in scores:

        if role_score[1] == best_role_score[1]:
            numberOfTopRoles += 1

    if numberOfTopRoles != 1:
        return None
    else:
        return best_role_score[0]


###################################################
#                SECONDARY FUNCTIONS              #
###################################################

"""
Creates clusters of players into roles.
"""


def getClusters(match_ids, region, roles):

    clusters = {'marksman': [], 'support': [],
                'mage': [], 'tank': [], 'fighter': []}

    total = len(match_ids)

    for i in xrange(total):

        print "Processing match {i} / {total}".format(i=i, total=total)

        match_id = match_ids[i]
        playerList = getMatchItems(match_id, region)

        for player in playerList:

            scores = []

            for role in roles:

                score = getScore(player, roles[role])
                scores.append([role, score])

            bestRole = getBestRole(scores)

            if bestRole:
                clusters[bestRole].append(player)

    return clusters


"""
Using the old cluster data, generate a new set of data.
"""


def generateNextIteration(iteration, version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))
    assert(iteration >= 0)

    if not os.path.exists('./jsons/kmeans/{ver}'.format(ver=version)):
        os.makedirs('./jsons/kmeans/{ver}'.format(ver=version))
    if not os.path.exists('./jsons/kmeans/{ver}/{gm}'.format(ver=version, gm=gamemode)):
        os.makedirs(
            './jsons/kmeans/{ver}/{gm}'.format(ver=version, gm=gamemode))
    if not os.path.exists('./jsons/kmeans/{ver}/{gm}/{reg}'.format(ver=version, gm=gamemode, reg=region)):
        os.makedirs(
            './jsons/kmeans/{ver}/{gm}/{reg}'.format(ver=version, gm=gamemode, reg=region))
    if not os.path.exists('./jsons/kmeans/{ver}/{gm}/{reg}/0.json'.format(ver=version, gm=gamemode, reg=region)):
        initKMeansRoleJson(
            './jsons/kmeans/{ver}/{gm}/{reg}/0.json'.format(ver=version, gm=gamemode, reg=region))

    roles = {'marksman': [], 'support': [],
             'mage': [], 'tank': [], 'fighter': []}

    roles_data = readEntireFile('./jsons/kmeans/{ver}/{gm}/{reg}/{it}.json'.format(
        ver=version, gm=gamemode, reg=region, it=iteration))
    match_ids = getMatchIDs(version, gamemode, region)

    clusters = getClusters(match_ids=match_ids,
                           region=region, roles=json.loads(roles_data))

    for cluster, data in clusters.items():

        items = []

        for dataset in data:
            items += dataset['items']

        unique_items = set(items) - ITEMS_TO_IGNORE

        for item in unique_items:
            roles[cluster].append(
                {item: float(items.count(item)) / float(len(items))})

    dataToWrite = json.dumps(roles, sort_keys=True,
                             indent=4, separators=(',', ': '))
    writeAllToFile('./jsons/kmeans/{ver}/{gm}/{reg}/{it}.json'.format(
        ver=version, gm=gamemode, reg=region, it=iteration + 1), dataToWrite)


###################################################
#                PRIMARY FUNCTIONS                #
###################################################

"""
Finds the newest iteration of data, and creates the next one.
"""


def getIteration(iteration, version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))
    assert(iteration >= 0)

    i0 = 0

    if os.path.exists('./jsons/kmeans/{ver}/{gm}/{reg}/0.json'.format(ver=version, gm=gamemode, reg=region)):

        file_list = os.listdir(
            './jsons/kmeans/{ver}/{gm}/{reg}'.format(ver=version, gm=gamemode, reg=region))

        for my_file in file_list:

            ix = int(my_file.split('.')[0])
            if ix > i0:
                i0 = ix

    if iteration <= i0:
        print "Already done!"
        return

    for i in xrange(i0, iteration):
        generateNextIteration(i, version, gamemode, region)


"""
Finds puts each player into clusters, calculates a champions role percentage using the players' champion id
"""


def generateChampionRoles(version, gamemode, region):

    gamemode = gamemode.upper()
    region = region.upper()
    assert(assertVersionGamemodeRegion(
        version=version, gamemode=gamemode, region=region))

    i0 = 0

    if os.path.exists('./jsons/kmeans/{ver}/{gm}/{reg}/0.json'.format(ver=version, gm=gamemode, reg=region)):

        file_list = os.listdir(
            './jsons/kmeans/{ver}/{gm}/{reg}'.format(ver=version, gm=gamemode, reg=region))

        for my_file in file_list:

            ix = int(my_file.split('.')[0])
            if ix > i0:
                i0 = ix

    roles_data = readEntireFile(
        './jsons/kmeans/{ver}/{gm}/{reg}/{it}.json'.format(ver=version, gm=gamemode, reg=region, it=i0))
    match_ids = getMatchIDs(version, gamemode, region)

    clusters = getClusters(match_ids=match_ids,
                           region=region, roles=json.loads(roles_data))

    champs = Champion.objects.filter(
        version__name=version, gamemode__name=gamemode, region__name=region)

    champs.update(roles="")

    total = champs.count()

    for i in xrange(total):

        print "Processing champion {i} / {total}".format(i=i, total=total)

        champ = champs[i]
        scores = {}

        for cluster, data in clusters.items():

            score = 0.0

            for player in data:

                if player['champion'] == champ.key:

                    score += 1.0

            scores[cluster] = score

        total_score = 0.0

        for k, v in scores.iteritems():
            total_score += v

        if total_score == 0.0:
            continue

        for k in scores.keys():
            scores[k] = round((scores[k] / total_score) * 100, 2)

        champ.roles = json.dumps(scores)
        champ.save()
