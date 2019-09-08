from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Data(models.Model):
    date = models.DateField()
    campaign = models.ForeignKey(Campaign, on_delete=models.DO_NOTHING, db_constraint=False)
    source = models.ForeignKey(Source, on_delete=models.DO_NOTHING, db_constraint=False)
    clicks = models.IntegerField()
    impressions = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.campaign.name} - {self.source.name}"
