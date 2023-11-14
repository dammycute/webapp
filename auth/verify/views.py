from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import *
import uuid
import requests
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .tasks import *
from django.http import HttpResponse



# Create your views here.


class VerifyNIN(generics.CreateAPIView):
    serializer_class = NinVerificationSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        

        # Step 1: Obtain an authorization code
        auth_code_url = "https://api.qoreid.com/token"
        auth_code_payload = {
            "secret": "ebde58d50dbd4fe19fbc6747c1f8bdd2",
            "clientId": "FNERU8BH03TA4K3L6VX6"
        }
        auth_code_headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        try:
            response = requests.post(auth_code_url, json=auth_code_payload, headers=auth_code_headers)
            if response.status_code == 201:
                auth_response = json.loads(response.text)  # Parse the JSON response
                authorization_code = auth_response.get("accessToken")
                # print(auth_response)
            else:
                return Response({"error": "Failed to obtain authorization code"}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException:
            return Response({"error": "Failed to connect to the authorization endpoint"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 2: Use the authorization code for NIN verification
        idNumber = serializer.validated_data["idNumber"]
        firstname = serializer.validated_data["firstname"]
        lastname = serializer.validated_data["lastname"]

        customer = CustomerDetails.objects.get(user=request.user)
        
        ninverify = NinModel.objects.create(
            customer=customer,
            is_verified=False,
            transaction_id=uuid.uuid4().hex,
        )
        
        nin_url = f"https://api.qoreid.com/v1/ng/identities/virtual-nin/{idNumber}"
        nin_payload = {"firstname": firstname, "lastname": lastname}
        nin_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {authorization_code}"
        }

        try:
            response = requests.post(nin_url, json=nin_payload, headers=nin_headers)
            if response.status_code == 200:
                response_data = json.loads(response.text)  # Parse the JSON response
                applicant = response_data.get("applicant")
                firstName = applicant.get("firstname")
                lastName = applicant.get("lastname")
                if firstName == firstname and lastName == lastname:
                    msg = "Yea your details are correct"
                    print(response_data)
                    return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Failed to verify NIN"}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException:
            return Response({"error": "Failed to connect to the NIN verification endpoint"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def qoreid_webhook_handler(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        event_type = data['eventType']
        transaction_id = data['transactionId']
        verification_status = data['status.status']

        if event_type == 'verification_completed':
            # Update the NinModel instance based on the verification status
            nin_model = NinModel.objects.get(transaction_id=transaction_id)
            nin_model.is_verified = True
            nin_model.save()

            # Send a notification to the user if the verification was successful
            if verification_status:
                send_nin_verification_success_notification(user=nin_model.customer.user, transaction_id=transaction_id)
            else:
                send_nin_verification_failure_notification(user=nin_model.customer.user, transaction_id=transaction_id)

        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)





class BvnVerificationView(generics.CreateAPIView):
    serializer_class = BvnVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idNumber = serializer.validated_data["idNumber"]
        firstname = serializer.validated_data["firstname"]
        lastname = serializer.validated_data["lastname"]

        # User = request.user
        customer = CustomerDetails.objects.get(user=request.user)
        bvnverify = BvnModel.objects.create(
            customer=customer,
            is_verified=False,
            transaction_id=uuid.uuid4().hex,
        )

        url = f"https://api.qoreid.com/v1/ng/identities/bvn-basic/{idNumber}"

        payload = {"firstname": firstname, "lastname": lastname}

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzaVgtaEFrS3RmNUlsYWhRcElrNWwwbFBRVlNmVnpBdG9WVWQ4UXZ1OHJFIn0.eyJleHAiOjE2OTk0MTkzOTksImlhdCI6MTY5OTQxMjE5OSwianRpIjoiYjQyYzAxNWYtYjA2OS00NDZjLWJkNzEtNTMyNjRlN2JmY2NjIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnFvcmVpZC5jb20vYXV0aC9yZWFsbXMvcW9yZWlkIiwiYXVkIjpbInFvcmVpZGFwaSIsImFjY291bnQiXSwic3ViIjoiMzdlOTM1MTItNmZhYi00ODYxLWJiNWMtZmU2MTg2ODliZDI5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiRk5FUlU4QkgwM1RBNEszTDZWWDYiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXFvcmVpZCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7InFvcmVpZGFwaSI6eyJyb2xlcyI6WyJ2ZXJpZnlfdmlydHVhbF9uaW5fc3ViIiwidmVyaWZ5X29jcl9zdWIiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsImVudmlyb25tZW50Ijoic2FuZGJveCIsImNsaWVudEhvc3QiOiIxOTIuMTY4LjEzMi4yMDEiLCJjbGllbnRJZCI6IkZORVJVOEJIMDNUQTRLM0w2Vlg2IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJvcmdhbmlzYXRpb25JZCI6MjE1MDQzLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtZm5lcnU4YmgwM3RhNGszbDZ2eDYiLCJhcHBsaWNhdGlvbklkIjoxNzcxMSwiY2xpZW50QWRkcmVzcyI6IjE5Mi4xNjguMTMyLjIwMSJ9.HjEaKASH-CbEjYWrRmhgft2lj6y0anm9SxOTEvN5gAghM_n8rFBpSmh-Lt4k0Gam04901Y5KBv8-K0nfaOKk6IJWV_xBA-z6yQXJfM0tVRMKHEOQOXHJOryPaG52C3ugOzrYeUL6HXE6zpdAdVNM17x3RhExGkhz3pKFFCyam3yuNmSgoIlOBaHHfJLAJEG3Jg1KNLXhjVCgGdwfZUXrrh-4x4FG5Hho6YFFtfeMcSeSTI6WYSwyQSFLeDD8De3JGXPbmfDsBKQI0w9HbyTZnimlb1CKXeQKBqI1DEN2c8JftM-IlRUHL5qQUs4xFXhtgmVCo_YtJF2toOxGuNQUjg",
        }

        response = requests.post(url, json=payload, headers=headers)

        return Response(response.text)

class AuthGet(APIView):
    def post(self, request):
        auth_code_url = "https://api.qoreid.com/token"
        auth_code_payload = {
            "secret": "ebde58d50dbd4fe19fbc6747c1f8bdd2",
            "clientId": "FNERU8BH03TA4K3L6VX6"
        }
        auth_code_headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        try:
            response = requests.post(auth_code_url, json=auth_code_payload, headers=auth_code_headers)
            if response.status_code == 201:
                auth_response = json.loads(response.text)  # Parse the JSON response

                authorization_code = auth_response.get("accessToken")
                print(authorization_code)
                return Response(response)
        except:
            return Response("pass")
        #     else:
        #         return Response({"error": "Failed to obtain authorization code"}, status=status.HTTP_400_BAD_REQUEST)
        # except requests.exceptions.RequestException:
        #     return Response({"error": "Failed to connect to the authorization endpoint"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)