from django.urls import path
from .views import *

urlpatterns = [
    path('verify-nin/', NinVerificationView.as_view(), name='verify-nin'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]