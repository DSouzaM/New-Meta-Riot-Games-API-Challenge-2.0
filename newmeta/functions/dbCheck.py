from apps.main.models import Match
regions = ['EUNE', 'EUW', 'KR', 'LAN']
queues = ['NORMAL_5X5', 'RANKED_SOLO']
versions = [5.11, 5.14]


def dbCheck():
    for region in regions:
        for queue in queues:
            for version in versions:
                print region, queue, version, Match.objects.filter(region__name=region, version__name=version, gamemode__name=queue).count()
