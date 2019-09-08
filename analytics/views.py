from analytics.models import Data, Campaign, Source
from django.views.generic.list import ListView
from django.db.models import Count, Sum
from django.db.models.query import QuerySet
from typing import Any


class DataListView(ListView):
    model = Data

    def get_context_data(self, **kwargs: Any) -> dict:
        """
        Extend the context data with campaigns, sources, selected_campaigns and selected_sources.
        """
        context = super().get_context_data(**kwargs)
        context['campaigns'] = Campaign.objects.all()
        context['sources'] = Source.objects.all()
        context['selected_campaigns'] = self.request.GET.getlist('campaigns', [])
        context['selected_sources'] = self.request.GET.getlist('sources', [])
        return context

    def get_queryset(self) -> QuerySet:
        """
        Filter the queryset for campaigns and sources, group by date and sum the clicks and impressions.

        :return: filtered and modified Queryset
        """
        qs = super(DataListView, self).get_queryset()
        qs = self._filter_campaigns(qs)
        qs = self._filter_sources(qs)
        qs = qs.values('date').annotate(dcount=Count('date'),
                                        sum_clicks=Sum('clicks'),
                                        sum_impressions=Sum('impressions')).order_by('date')
        return qs

    def _filter_campaigns(self, queryset: QuerySet) -> QuerySet:
        """
        Filter the queryset for campaigns from the GET parameters.

        :param queryset: Analytics Queryset
        :return: filtered queryset
        """
        campaigns = self.request.GET.getlist('campaigns')
        if campaigns:
            return queryset.filter(campaign_id__in=list(map(int, campaigns)))
        return queryset

    def _filter_sources(self, queryset: QuerySet) -> QuerySet:
        """
        Filter the queryset for sources from the GET parameters.

        :param queryset: Analytics Queryset
        :return: filtered queryset
        """
        sources = self.request.GET.getlist('sources')
        if sources:
            return queryset.filter(source_id__in=list(map(int, sources)))
        return queryset
