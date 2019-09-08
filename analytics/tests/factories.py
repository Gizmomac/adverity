import datetime
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyDate
from analytics.models import Data, Campaign, Source


class CampaignFactory(DjangoModelFactory):
    class Meta:
        model = Campaign

    name = Sequence(lambda n: "Campaign #%s" % n)


class SourceFactory(DjangoModelFactory):
    class Meta:
        model = Source

    name = Sequence(lambda n: "Source #%s" % n)


class DataFactory(DjangoModelFactory):
    class Meta:
        model = Data

    date = FuzzyDate(datetime.date(2018, 1, 1))
    campaign = SubFactory(CampaignFactory)
    source = SubFactory(SourceFactory)
    clicks = FuzzyInteger(0, 42)
    impressions = FuzzyInteger(0, 42)
