from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=3)

    def __unicode__(self):
        return self.name


class Version(models.Model):
    name = models.CharField(max_length=4)

    def __unicode__(self):
        return self.name


class Gamemode(models.Model):
    name = models.CharField(max_length=11)

    def __unicode__(self):
        return self.name


class Match(models.Model):
    match_id = models.IntegerField()

    region = models.ForeignKey(Region, default=1)
    version = models.ForeignKey(Version, default=1)
    gamemode = models.ForeignKey(Gamemode, default=1)

    data = models.TextField()

    def __unicode__(self):
        return "{mid} {r} {v} {g}".format(
            mid=self.match_id,
            r=self.region.name,
            v=self.version.name,
            g=self.gamemode.name
        )

    class Meta:
        unique_together = (('region', 'match_id'),)


class Champion(models.Model):
    region = models.ForeignKey(Region, default=1)
    version = models.ForeignKey(Version, default=1)
    gamemode = models.ForeignKey(Gamemode, default=1)

    key = models.IntegerField()
    name = models.CharField(max_length=16)

    wins = models.IntegerField(default=0)
    picks = models.IntegerField(default=0)

    roles = models.TextField(default="{}")

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('region', 'version', 'gamemode', 'key'),)


class Item(models.Model):
    region = models.ForeignKey(Region, default=1)
    version = models.ForeignKey(Version, default=1)
    gamemode = models.ForeignKey(Gamemode, default=1)

    key = models.IntegerField()
    name = models.CharField(max_length=16)

    wins = models.IntegerField(default=0)
    picks = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('region', 'version', 'gamemode', 'key'),)
