from rest_framework import serializers

from api import models
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'last_login')

class TechnicianSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Profile
        fields = ('user', 'user_type', 'avatar', 'lon', 'lat')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Profile
        fields = ('user', 'user_type', 'avatar')

class SpareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Spare
        fields = ('partID', 'name', 'stock')
class SpareDetailSerializer(serializers.ModelSerializer):
    spare = SpareSerializer(many=False)

    class Meta:
        model = models.SpareDetail
        fields = ('spare', 'quantity', 'drawn')

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Aircraft
        fields = ('regn', 'acType', 'inbound', 'outbound', 'ETA', 'ETD', 'bay')

class UpdateSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    class Meta:
        model = models.Update
        fields = ('author', 'details', 'created')

class DefectSerializer(serializers.ModelSerializer):
    plane = AircraftSerializer(many=False)
    techsAssigned = TechnicianSerializer(many=True)
    spares = SpareDetailSerializer(many=True)
    updates = UpdateSerializer(many=True)
    class Meta:
        model = models.Defect
        fields = ('plane', 'techsAssigned',
                'header', 'description', 'dateReported',
                'classCode', 'category', 'img', 'priority',
                'spares', 'updates')
