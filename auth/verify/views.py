from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import *
import uuid
import requests
from rest_framework.response import Response

# Create your views here.


class NinVerificationView(generics.CreateAPIView):
    serializer_class = NinVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idNumber = serializer.validated_data["idNumber"]
        firstname = serializer.validated_data["firstname"]
        lastname = serializer.validated_data["lastname"]

        # User = request.user
        customer = CustomerDetails.objects.get(user=request.user)
        ninverify = NinModel.objects.create(
            customer=customer,
            is_verified=False,
            transaction_id=uuid.uuid4().hex,
        )

        url = f"https://api.qoreid.com/v1/ng/identities/virtual-nin/{idNumber}"

        payload = {"firstname": firstname, "lastname": lastname}

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzaVgtaEFrS3RmNUlsYWhRcElrNWwwbFBRVlNmVnpBdG9WVWQ4UXZ1OHJFIn0.eyJleHAiOjE2OTk0MTkzOTksImlhdCI6MTY5OTQxMjE5OSwianRpIjoiYjQyYzAxNWYtYjA2OS00NDZjLWJkNzEtNTMyNjRlN2JmY2NjIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnFvcmVpZC5jb20vYXV0aC9yZWFsbXMvcW9yZWlkIiwiYXVkIjpbInFvcmVpZGFwaSIsImFjY291bnQiXSwic3ViIjoiMzdlOTM1MTItNmZhYi00ODYxLWJiNWMtZmU2MTg2ODliZDI5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiRk5FUlU4QkgwM1RBNEszTDZWWDYiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXFvcmVpZCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7InFvcmVpZGFwaSI6eyJyb2xlcyI6WyJ2ZXJpZnlfdmlydHVhbF9uaW5fc3ViIiwidmVyaWZ5X29jcl9zdWIiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsImVudmlyb25tZW50Ijoic2FuZGJveCIsImNsaWVudEhvc3QiOiIxOTIuMTY4LjEzMi4yMDEiLCJjbGllbnRJZCI6IkZORVJVOEJIMDNUQTRLM0w2Vlg2IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJvcmdhbmlzYXRpb25JZCI6MjE1MDQzLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtZm5lcnU4YmgwM3RhNGszbDZ2eDYiLCJhcHBsaWNhdGlvbklkIjoxNzcxMSwiY2xpZW50QWRkcmVzcyI6IjE5Mi4xNjguMTMyLjIwMSJ9.HjEaKASH-CbEjYWrRmhgft2lj6y0anm9SxOTEvN5gAghM_n8rFBpSmh-Lt4k0Gam04901Y5KBv8-K0nfaOKk6IJWV_xBA-z6yQXJfM0tVRMKHEOQOXHJOryPaG52C3ugOzrYeUL6HXE6zpdAdVNM17x3RhExGkhz3pKFFCyam3yuNmSgoIlOBaHHfJLAJEG3Jg1KNLXhjVCgGdwfZUXrrh-4x4FG5Hho6YFFtfeMcSeSTI6WYSwyQSFLeDD8De3JGXPbmfDsBKQI0w9HbyTZnimlb1CKXeQKBqI1DEN2c8JftM-IlRUHL5qQUs4xFXhtgmVCo_YtJF2toOxGuNQUjg",
        }

        response = requests.post(url, json=payload, headers=headers)

        return Response(response.text)