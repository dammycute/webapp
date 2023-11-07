from django.urls import path
from .views import *
urlpatterns = [
    path('post-property/', CreatePropertyView.as_view()),
    path('post-property/<int:id>/', UpdatePropertyView.as_view()),
    path('primary-market/', PrimaryMarketView.as_view()),
    path('property-lists/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    # path('investments/<int:pk>/sell/', Sell.as_view(), name='investment-sell'),
    path('primary-buy/<int:product_id>/', PrimaryBuyView.as_view(), name='buy'),
    path('investments/', InvestmentListView.as_view(), name='investment-list'),
]