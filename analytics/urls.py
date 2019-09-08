from django.urls import path
from analytics.views import DataListView

urlpatterns = [
    path('', DataListView.as_view(), name='data-list'),
]
