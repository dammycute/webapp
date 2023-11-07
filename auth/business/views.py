from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from .models import *
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from rest_framework import exceptions
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.generics import get_object_or_404
from rest_framework import status
from django.urls import reverse
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from .serializers import *
from .tasks import *

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

# View to create Property, only admins have the authorization to create it
class CreatePropertyView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

# Edit property created by yourself. Only the creator of the property will be able to edit

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


# This is the primary market view, it consist of the list of available properties for purchase 
class PrimaryMarketView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for property_data in response.data:
            url = reverse('property-detail', args=[property_data['id']])
            full_url = request.build_absolute_uri(url)
            property_data['url'] = full_url
        return response

# This is a detailed info of a specified property 
class PropertyDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'pk'




# ======= Primary Buy View ==========

from django.db import transaction

class PrimaryBuyView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Investment.objects.select_related('product').all()
    serializer_class = InvestmentSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            product_id = kwargs['product_id']  # Get the product ID from the URL
            product = Property.objects.get(pk=product_id)
            slots = int(request.data.get('slots'))
            if slots <= 0:
                raise ValidationError({'slots': 'Slots must be greater than zero'})
            
            if product.slots_available < slots:
                raise ValidationError({slots: f'Only {product.slots_available} slots available'})
            product.slots_available -= slots
            product.save()

            total_price = product.price_per_slot * slots
            roi = product.roi
            
            # wallet = Wallet.objects.select_for_update().get(user=self.request.user)
            # if wallet.balance < total_price:
            #     raise ValidationError({'wallet': 'Insufficient funds'})
            # wallet.balance -= total_price
            # wallet.save()

            investment = Investment.objects.create(
                user=self.request.user,
                product=product,
                slots=slots,
                start_date=datetime.date.today(),
                end_date=datetime.date.today() + relativedelta(months=product.duration),
            )
            today = datetime.date.today()
            investment.total_price = total_price
            investment.roi = roi
            elapsed_months = (today.year - investment.start_date.year) * 12 + (today.month - investment.start_date.month)
            investment.current_value = total_price * (1 + ((roi / 12) / 100) * elapsed_months)
            investment.save()

            

            result = {
                'product': product.property_name,
                'amount': investment.current_value,
                'slots': slots,
                'investment_id': investment.id,
                'message': f"You've purchased {slots} slot(s) of {product.property_name} successfully",
            }

            if product.slots_available == 0:
                result['message'] = f"All {product.property_name} slots have been sold"
            else:
                result['message'] = f"You've purchased {slots} slot(s) of {product.property_name} successfully"

            # Trigger Celery task to update current value each month
            # update_investment_value.apply_async(args=[investment.id], eta=investment.end_date.replace(day=1))
            return Response(result, status=status.HTTP_201_CREATED)
        except Property.DoesNotExist:
            raise ValidationError({'property': 'Invalid property id'})
        
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_400_BAD_REQUEST)


# ==================== This is the Endpoint that list out the investments of the user===========

class InvestmentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,IsOwnerOfObject]
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)