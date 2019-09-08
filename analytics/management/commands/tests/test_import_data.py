import mock
from django.core.management import call_command
from django.test import TestCase
from analytics.management.commands.import_data import DataLoader


class CommandsTestCase(TestCase):

    @mock.patch("analytics.management.commands.import_data.uuid.uuid4")
    @mock.patch.object(DataLoader, "__init__")
    @mock.patch.object(DataLoader, "process")
    def test_import_data_with_url(self, mock_process, mock_init, mock_uuid4):
        test_url = "http://example.com/test.csv"
        test_uuid = "4b348e0d-d431-4c7c-944f-b6efae28f1a6"
        mock_uuid4.return_value = test_uuid
        mock_init.return_value = None
        call_command("import_data", url=test_url)
        self.assertEqual(mock_init.call_count, 1)
        self.assertEqual(mock_init.call_args[0][0], test_url)
        self.assertEqual(mock_init.call_args[0][1], f"{test_uuid}.csv")
        self.assertEqual(mock_process.call_count, 1)

    @mock.patch("analytics.management.commands.import_data.uuid.uuid4")
    @mock.patch.object(DataLoader, "__init__")
    @mock.patch.object(DataLoader, "process")
    def test_import_data_without_url(self, mock_process, mock_init, mock_uuid4):
        default_url = "http://adverity-challenge.s3-website-eu-west-1.amazonaws.com/DAMKBAoDBwoDBAkOBAYFCw.csv"
        test_uuid = "4b348e0d-d431-4c7c-944f-b6efae28f1a6"
        mock_uuid4.return_value = test_uuid
        mock_init.return_value = None
        call_command("import_data", url=default_url)
        self.assertEqual(mock_init.call_count, 1)
        self.assertEqual(mock_init.call_args[0][0], default_url)
        self.assertEqual(mock_init.call_args[0][1], f"{test_uuid}.csv")
        self.assertEqual(mock_process.call_count, 1)
