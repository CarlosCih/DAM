from django.urls import path
from . import api_views

urlpatterns = [
    path('metrics/summary/', api_views.MetricsSummaryView.as_view(), name='metrics-summary'),
    path('metrics/timeseries/', api_views.MetricsTimeSeriesView.as_view(), name='metrics-timeseries'),
    path('metrics/breakdown/', api_views.MetricsBreakdownView.as_view(), name='metrics-breakdown'),
]