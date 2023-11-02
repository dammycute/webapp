from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from .models import *
from rest_framework.exceptions import ValidationError, PermissionDenied


from .serializers import *

# Create your views here.
# class DashboardView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         wallet = Wallet.objects.filter(user=request.user).first()
#         investments = Investment.objects.filter(user=request.user).aggregate(total_amount=Sum('current_value'))['total_amount']

#         data = {
#             'wallet_balance': wallet.balance if wallet else None,
#             'investment': investments,
#         }

#         return Response(data)

class IsOwnerOfObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class CreatePropertyView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

class UpdatePropertyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser, IsOwnerOfObject]
    
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_staff or serializer.instance.owner == user:
            serializer.save(owner=user)
        else:
            raise PermissionDenied(detail="You do not have permission to update this property.")