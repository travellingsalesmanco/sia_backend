from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from api import models
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'last_login')

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
class OutputSpareDetailSerializer(serializers.ModelSerializer):
    spare = SpareSerializer(many=False)
    class Meta:
        model = models.SpareDetail
        fields = ('id', 'spare', 'quantity', 'drawn')

class InputSpareDetailSerializer(serializers.ModelSerializer):
    # Allow specification of primary key, which will mean an update to existing
    # spare detail
    id = serializers.IntegerField(required=False)
    class Meta:
        model = models.SpareDetail
        fields = ('id', 'spare', 'quantity', 'drawn')

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Aircraft
        fields = ('regn', 'acType', 'inbound', 'outbound', 'ETA', 'ETD', 'bay')

class UpdateSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    class Meta:
        model = models.Update
        fields = ('author', 'details', 'created')

class OutputDefectSerializer(serializers.ModelSerializer):
    """ Full details of defects, for viewing """
    plane = AircraftSerializer(many=False)
    techsAssigned = TechnicianSerializer(many=True)
    spares = OutputSpareDetailSerializer(many=True)
    updates = UpdateSerializer(many=True)
    class Meta:
        model = models.Defect
        fields = ('id', 'header', 'description', 'plane', 'techsAssigned',
                'dateReported', 'dateResolved', 'closed',
                'classCode', 'category', 'img', 'priority',
                'spares', 'updates')

class InputDefectSerializer(serializers.ModelSerializer):
    """ For processing inputs """
    spares = InputSpareDetailSerializer(many=True)
    class Meta:
        model = models.Defect
        fields = ('header', 'classCode', 'category', 'plane', # Required fields
                'description', 'techsAssigned',
                'dateReported', 'dateResolved', 'closed', 'img', 'priority',
                'spares')

    def create(self, validated_data):
        spares_data = validated_data.pop('spares')
        defect = Defect.objects.create(**validated_data)
        # Create the SpareDetails
        for spare_data in spares_data:
            SpareDetail.objects.create(defect=defect, **spare_data)
        return defect

    def update(self, instance, validated_data):
        # Handle spares
        spares_data = validated_data.pop('spares', None)
        for spare_data in spares_data:
            # If primary key is provided, edit the entry
            pk = spare_data.get('id', None)
            if pk is not None:
                try:
                    sd = SpareDetail.objects.get(id=pk)
                    sd.spare = spare_data.get('spare', sd.spare)
                    sd.quantity = spare_data.get('quantity', sd.quantity)
                    sd.drawn = spare_data.get('drawn', sd.drawn)
                    sd.save()
                except ObjectDoesNotExist:
                    print("No such spare detail.")
            # Otherwise create a new SpareDetail
            else:
                SpareDetail.objects.create(defect=defect, **spare_data)
        # Handle techsAssigned
        techs_data = validated_data.pop('techsAssigned', None)
        if techs_data is not None:
            instance.techsAssigned.add(techs_data)

        # Update the rest of the data
        Defect.objects.filter(id=instance.id).update(**validated_data)

        # Non of the updates here call the .save() method, if we use a post_save
        # signal, include the following line to trigger the signals at the end
        # of an update:
        # instance.save()

# --------------- Raw defects ----------------
class RawSpareDetailSerializer(serializers.ModelSerializer):
    spare = SpareSerializer(many=False)
    id = serializers.IntegerField(required=False)
    class Meta:
        model = models.RawSpareDetail
        fields = ('id', 'spare', 'quantity')

class RawDefectSerializer(serializers.ModelSerializer):
    plane = AircraftSerializer(many=False)
    spares = RawSpareDetailSerializer(many=True)
    class Meta:
        model = models.RawDefect
        fields = ('id', 'header', 'description', 'plane',
                'dateReported', 'classCode', 'category', 'img', 'priority',
                'spares')
