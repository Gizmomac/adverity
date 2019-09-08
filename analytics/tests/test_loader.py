import mock
from django.test import TestCase
from datetime import date
from analytics.models import Source, Campaign, Data
from analytics.tests.factories import SourceFactory, CampaignFactory
from analytics.loader import DataLoader
from django.conf import settings


class LoaderTest(TestCase):
    test_url = "http://example.com/date.csv"
    test_file_path = settings.BASE_DIR + "/analytics/tests/test.csv"

    def test_convert_date(self):
        string_date = "19.01.2019"
        date_date = date(2019, 1, 19)
        result = DataLoader._convert_date(string_date)
        self.assertEqual(result, date_date)

    def test_get_source_create_database(self):
        name = "source_name"
        self.assertIsNone(Source.objects.filter(name=name).first())
        loader = DataLoader(self.test_url, self.test_file_path)
        source_id = loader._get_source(name)
        source = Source.objects.filter(name=name).first()
        self.assertEqual(source_id, source.id)
        self.assertEqual(loader.sources[name], source.id)

    def test_get_source_from_database(self):
        name = "source_name"
        source = SourceFactory.create(name=name)
        loader = DataLoader(self.test_url, self.test_file_path)
        source_id = loader._get_source(name)
        self.assertEqual(source.id, source_id)
        self.assertEqual(loader.sources[name], source.id)

    def test_get_source_from_cache(self):
        name = "source_name"
        source_id = 999
        loader = DataLoader(self.test_url, self.test_file_path)
        loader.sources[name] = source_id
        self.assertEqual(loader._get_source(name), source_id)

    def test_get_campaign_create_database(self):
        name = "campaign_name"
        self.assertIsNone(Campaign.objects.filter(name=name).first())
        loader = DataLoader(self.test_url, self.test_file_path)
        campaign_id = loader._get_campaign(name)
        campaign = Campaign.objects.filter(name=name).first()
        self.assertEqual(campaign_id, campaign.id)
        self.assertEqual(loader.campaigns[name], campaign.id)

    def test_get_campaign_from_database(self):
        name = "campaign_name"
        campaign = CampaignFactory.create(name=name)
        loader = DataLoader(self.test_url, self.test_file_path)
        campaign_id = loader._get_campaign(name)
        self.assertEqual(campaign.id, campaign_id)
        self.assertEqual(loader.campaigns[name], campaign.id)

    def test_get_campaign_from_cache(self):
        name = "campaign_name"
        campaign_id = 999
        loader = DataLoader(self.test_url, self.test_file_path)
        loader.campaigns[name] = campaign_id
        self.assertEqual(loader._get_campaign(name), campaign_id)

    def test_load_data(self):
        loader = DataLoader(self.test_url, self.test_file_path)
        loader._load_data()
        self.assertEqual(Data.objects.all()[0].date, date(2019, 1, 1))
        self.assertEqual(Data.objects.all()[0].clicks, 1)
        self.assertEqual(Data.objects.all()[0].impressions, 2)
        self.assertEqual(Data.objects.all()[0].source.name, "Facebook Ads")
        self.assertEqual(Data.objects.all()[0].campaign.name, "Like Ads")
        self.assertEqual(Data.objects.all()[1].date, date(2019, 1, 1))
        self.assertEqual(Data.objects.all()[1].clicks, 5)
        self.assertIsNone(Data.objects.all()[1].impressions)
        self.assertEqual(Data.objects.all()[1].source.name, "Google Adwords")
        self.assertEqual(Data.objects.all()[1].campaign.name, "B2B - Leads")

    @mock.patch("analytics.loader.DataLoader._cleanup")
    @mock.patch("analytics.loader.DataLoader._load_data")
    @mock.patch("analytics.loader.DataLoader._download")
    def test_process(self, mock_download, mock_load_data, mock_cleanup):
        loader = DataLoader(self.test_url, self.test_file_path)
        loader.process()
        self.assertEqual(mock_download.call_count, 1)
        self.assertEqual(mock_load_data.call_count, 1)
        self.assertEqual(mock_cleanup.call_count, 1)

    @mock.patch("analytics.loader.DataLoader._cleanup")
    @mock.patch("analytics.loader.DataLoader._load_data")
    @mock.patch("analytics.loader.DataLoader._download")
    def test_process_clean_after_download_failure(self, mock_download, mock_load_data, mock_cleanup):
        loader = DataLoader(self.test_url, self.test_file_path)
        mock_download.side_effect = Exception("excepted error")
        with self.assertRaises(Exception):
            loader.process()
        self.assertEqual(mock_download.call_count, 1)
        self.assertEqual(mock_load_data.call_count, 0)
        self.assertEqual(mock_cleanup.call_count, 1)

    @mock.patch("analytics.loader.DataLoader._cleanup")
    @mock.patch("analytics.loader.DataLoader._load_data")
    @mock.patch("analytics.loader.DataLoader._download")
    def test_process_clean_after_data_load_failure(self, mock_download, mock_load_data, mock_cleanup):
        loader = DataLoader(self.test_url, self.test_file_path)
        mock_load_data.side_effect = Exception("excepted error")
        with self.assertRaises(Exception):
            loader.process()
        self.assertEqual(mock_download.call_count, 1)
        self.assertEqual(mock_load_data.call_count, 1)
        self.assertEqual(mock_cleanup.call_count, 1)
