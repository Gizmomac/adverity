import os
import wget
import csv
import datetime
from analytics.models import Campaign, Source, Data
from datetime import datetime
from django.db import transaction


class DataLoader:
    """
    Loader class what handle data import from a given http address.
    """

    def __init__(self, url: str, file_path: str) -> None:
        self.url = url
        self.file_path = file_path
        self.sources = {}
        self.campaigns = {}

    def process(self) -> None:
        """
        Download the csv from the url, load the content to the database
        """
        try:
            self._download()
            self._load_data()
        finally:
            self._cleanup()

    def _cleanup(self) -> None:
        """
        If file exists on self.file_path, delete it.
        """
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def _download(self) -> None:
        wget.download(self.url, self.file_path)

    @transaction.atomic
    def _load_data(self) -> None:
        """
        Open csv from file_path, process the lines and insert into database.
        """
        data = []
        with open(self.file_path, newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                source = self._get_source(row['Datasource'])
                campaign = self._get_campaign(row['Campaign'])
                date = self._convert_date(row['Date'])
                impressions = int(row['Impressions']) if row['Impressions'] else None
                clicks = int(row['Clicks'])
                analytics = Data(date=date, source_id=source, campaign_id=campaign, clicks=clicks,
                                 impressions=impressions)
                data.append(analytics)
        Data.objects.bulk_create(data)

    @staticmethod
    def _convert_date(date: str) -> datetime.date:
        """
        Convert string date to Date

        :param date: sting date in the given format "%d.%m.%Y"
        :return: converted Date object
        """
        return datetime.strptime(date, "%d.%m.%Y").date()

    def _get_source(self, source_name: str) -> int:
        """
        Get source from cache or database, create and cache if it's not exists.

        :param source_name: Name of the source
        :return: pk of the Source
        """
        source_id = self.sources.get(source_name)
        if source_id:
            return source_id
        source, _ = Source.objects.get_or_create(name=source_name)
        self.sources[source.name] = source.id
        return source.id

    def _get_campaign(self, campaign_name: str) -> int:
        """
        Get campaign from cache or database, create and cache if it's not exists.

        :param campaign_name: Name of the campaign
        :return: pk of the Campaign
        """
        campaign_id = self.campaigns.get(campaign_name)
        if campaign_id:
            return campaign_id
        campaign, _ = Campaign.objects.get_or_create(name=campaign_name)
        self.campaigns[campaign.name] = campaign.id
        return campaign.id
