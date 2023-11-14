from django.urls import path
from .views import *

urlpatterns = [
    path('verify-nin/', VerifyNIN.as_view(), name='verify-nin'),
    path('auth-get/', AuthGet.as_view(), name='verify-nin'),
    path('verify-webhook/', qoreid_webhook_handler, name='webhook'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]