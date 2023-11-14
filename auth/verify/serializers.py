from rest_framework import serializers

class NinVerificationSerializer(serializers.Serializer):
    idNumber = serializers.CharField(write_only=True)
    firstname = serializers.CharField(max_length = 255, write_only = True)
    lastname = serializers.CharField(max_length = 255, write_only = True)


class BvnVerificationSerializer(serializers.Serializer):
    idNumber = serializers.CharField(write_only=True)
    firstname = serializers.CharField(max_length = 255, write_only = True)
    lastname = serializers.CharField(max_length = 255, write_only = True)