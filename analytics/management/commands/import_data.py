import uuid
from django.core.management.base import BaseCommand
from analytics.loader import DataLoader


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            default="http://adverity-challenge.s3-website-eu-west-1.amazonaws.com/DAMKBAoDBwoDBAkOBAYFCw.csv",
            help='Overwrite the default url',
        )

    def handle(self, url, *args, **options):
        file_path = f"{uuid.uuid4()}.csv"
        loader = DataLoader(url, file_path)
        loader.process()
