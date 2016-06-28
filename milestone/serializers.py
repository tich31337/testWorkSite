from rest_framework import serializers
from .models import MilCamera, MilLogin2

class CameraSerializer(serializers.ModelSerializer):

    class Meta:
        model= MilCamera
        fields = ('ipAddress', 'CameraName')

    # def update_or_create(self, validated_data):
        # instance.ipAddress =
    # ipAddress = serializers.IPAddressField()
    # CameraName = serializers.CharField(max_length = 150)
    #
    # def create(self, validated_data):
    #     return MilCamera.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.ipAddress = validated_data.get('ipAddress', instance.ipAddress)
    #     instance.CameraName = validated_data.get('CameraName', instance.CameraName)
    #     instance.save()
    #     return instance