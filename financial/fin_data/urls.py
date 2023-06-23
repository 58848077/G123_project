from django.urls import path
from .views import FinancialDataView, StatisticsView
urlpatterns = [
    path('financial_data/', FinancialDataView.as_view()),
    path('statistics/', StatisticsView.as_view()),
]