from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    # referrer_code = serializers.CharField(required=False)
    password = serializers.CharField(max_length = 255, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'referrer_code', 'id']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 255, write_only=True)



class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=6, min_length=6)


class ResetOtpModelSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(max_length = 255, write_only=True)


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length = 255, write_only=True)
    new_password = serializers.CharField(max_length = 255, write_only=True)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = ('id', 'user', 'first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'zipcode', 'birth_date')
        read_only_fields = ('id', 'user')


class PictureSerializer(serializers.ModelSerializer):
    # picture = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)

    class Meta:
        model = CustomerDetails
        fields = ['picture']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = "__all__"