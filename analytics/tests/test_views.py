from django.test import TestCase, RequestFactory
from datetime import date
from analytics.models import Source, Campaign, Data
from analytics.tests.factories import DataFactory, SourceFactory, CampaignFactory
from analytics.views import DataListView


class ViewTest(TestCase):

    @staticmethod
    def setup_view(view, request, *args, **kwargs):
        """
        Mimic ``as_view()``, but returns view instance.
        Use this function to get view instances on which you can run unit tests,
        by testing specific methods.
        """

        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_view_filter_campaigns_without_get(self):
        campaign1 = CampaignFactory.create(name='test1')
        campaign2 = CampaignFactory.create(name='test2')
        DataFactory.create(campaign=campaign1)
        DataFactory.create(campaign=campaign2)

        request = RequestFactory().get('/')
        view = self.setup_view(DataListView(), request)
        qs = Campaign.objects.all()
        new_qs = view._filter_campaigns(qs)
        self.assertEqual(qs, new_qs)

    def test_view_filter_campaigns_with_get(self):
        campaign1 = CampaignFactory.create(name='test1')
        campaign2 = CampaignFactory.create(name='test2')
        campaign3 = CampaignFactory.create(name='test3')

        data_c1 = DataFactory.create(campaign=campaign1)
        data_c2 = DataFactory.create(campaign=campaign2)
        DataFactory.create(campaign=campaign3)

        request = RequestFactory().get('/', data={'campaigns': [str(campaign1.id), str(campaign2.id)]})
        view = self.setup_view(DataListView(), request)
        qs = Data.objects.all()
        new_qs = view._filter_campaigns(qs)
        self.assertEqual([data_c1, data_c2], list(new_qs.all()))

    def test_view_filter_sources_without_get(self):
        source1 = SourceFactory.create(name='test1')
        source2 = SourceFactory.create(name='test2')
        DataFactory.create(source=source1)
        DataFactory.create(source=source2)

        request = RequestFactory().get('/')
        view = self.setup_view(DataListView(), request)
        qs = Source.objects.all()
        new_qs = view._filter_sources(qs)
        self.assertEqual(qs, new_qs)

    def test_view_filter_sources_with_get(self):
        source1 = SourceFactory.create(name='test1')
        source2 = SourceFactory.create(name='test2')
        source3 = SourceFactory.create(name='test3')

        data_c1 = DataFactory.create(source=source1)
        data_c2 = DataFactory.create(source=source2)
        DataFactory.create(source=source3)

        request = RequestFactory().get('/', data={'sources': [str(source1.id), str(source2.id)]})
        view = self.setup_view(DataListView(), request)
        qs = Data.objects.all()
        new_qs = view._filter_sources(qs)
        self.assertEqual([data_c1, data_c2], list(new_qs.all()))

    def test_get_queryset_without_filter(self):
        data_date = date(2019, 1, 1)
        d1 = DataFactory.create(date=data_date, clicks=1, impressions=2)
        d2 = DataFactory.create(date=data_date, clicks=3, impressions=6)
        d3 = DataFactory.create(date=data_date, clicks=5, impressions=10)

        request = RequestFactory().get('/')
        view = self.setup_view(DataListView(), request)
        qs = view.get_queryset()
        results = qs.all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['sum_clicks'], d1.clicks + d2.clicks + d3.clicks)
        self.assertEqual(results[0]['sum_impressions'], d1.impressions + d2.impressions + d3.impressions)

    def test_get_queryset_with_filter(self):
        data_date = date(2019, 1, 1)
        s1 = SourceFactory.create()
        s2 = SourceFactory.create()
        s3 = SourceFactory.create()
        c1 = CampaignFactory.create()
        c2 = CampaignFactory.create()
        c3 = CampaignFactory.create()
        d1 = DataFactory.create(date=data_date, clicks=1, impressions=2, source=s1, campaign=c1)
        d2 = DataFactory.create(date=data_date, clicks=3, impressions=6, source=s2, campaign=c2)
        d3 = DataFactory.create(date=data_date, clicks=9, impressions=18, source=s1, campaign=c2)
        d4 = DataFactory.create(date=data_date, clicks=12, impressions=24, source=s2, campaign=c1)
        DataFactory.create(date=data_date, clicks=5, impressions=10, source=s3, campaign=c3)

        request = RequestFactory().get('/', data={'sources': [str(s1.id), str(s2.id)],
                                                  'campaigns': [str(c1.id), str(c2.id)]})
        view = self.setup_view(DataListView(), request)
        qs = view.get_queryset()
        results = qs.all()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['sum_clicks'], d1.clicks + d2.clicks + d3.clicks + d4.clicks)
        self.assertEqual(results[0]['sum_impressions'],
                         d1.impressions + d2.impressions + d3.impressions + d4.impressions)

    def test_get_context_data(self):
        s1 = SourceFactory.create()
        s2 = SourceFactory.create()
        SourceFactory.create()
        c1 = CampaignFactory.create()
        c2 = CampaignFactory.create()
        CampaignFactory.create()
        get_data = {'sources': [str(s1.id), str(s2.id)], 'campaigns': [str(c1.id), str(c2.id)]}
        request = RequestFactory().get('/', data=get_data)
        view = self.setup_view(DataListView(), request)
        view.object_list = Data.objects.all()
        context = view.get_context_data()
        self.assertEqual(list(context['campaigns']), list(Campaign.objects.all()))
        self.assertEqual(context['selected_campaigns'], get_data['campaigns'])
        self.assertEqual(list(context['sources']), list(Source.objects.all()))
        self.assertEqual(context['selected_sources'], get_data['sources'])
