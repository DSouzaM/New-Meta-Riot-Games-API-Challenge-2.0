from iterate import count_champ, count_item
# from kmeans import *
# from pull import *
from export import exportChampions, exportItems

"""
This module contains scripts to run overnight.
"""


def download():
    # regions = ['BR', 'EUNE', 'EUW', 'KR', 'LAN']
    # regions = ['NA', 'LAS', 'OCE', 'RU', 'TR']
    regions = ['NA', 'LAS']
    queues = ['NORMAL_5X5', 'RANKED_SOLO']
    versions = [5.11, 5.14]

    for region in regions:
        for queue in queues:
            for version in versions:

                # getMatchData(version, queue, region)
                # getChampions(version, queue, region)
                # getItems(version,queue,region)
                # getIteration(8, version, queue, region)
                # generateChampionRoles(version, queue, region)
                # count_champ(version, queue, region)
                pass
            exportChampions(queue, region)


def gary_temp():
    count_champ(5.11, 'RANKED_SOLO', 'NA')
    count_champ(5.14, 'RANKED_SOLO', 'NA')
    exportChampions('RANKED_SOLO', 'NA')
    count_item(5.11, 'RANKED_SOLO', 'NA')
    count_item(5.14, 'RANKED_SOLO', 'NA')
    exportItems('RANKED_SOLO', 'NA')
