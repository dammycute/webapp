# urls.py
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<int:pk>/', ActivateAccountView.as_view(), name='activate'),
    path('login-token/', LoginView.as_view(), name='token_obtain_pair'),
    path('password-reset-otp/', SendOtpView.as_view(), name='send_otp'),
    path('confirm-otp/', ConfirmOtpView.as_view(), name='confirm-otp'),
    path('password-change/', ResetPasswordView.as_view(), name='password-reset'),
    path('customer-details/', CustomerView.as_view(), name='customer'),
    # path('google-login/', login_with_google, name='customer'),
    # path('login/facebook/', FacebookLoginView.as_view(), name='social_login_facebook'),
]

