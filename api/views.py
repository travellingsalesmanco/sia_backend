# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from api import models
from api import serializers as s
import datetime

# Create your views here.


###------------------------------ PROFILE VIEWS --------------------------------------------------------------------####
#Request with username
class TechnicianProfile(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username')
        queryset = Profile.objects.get(userID=username)
        serialised_query = s.TechnicianSerializer(queryset)
        return Response(serialised_query.data)

#Request with username
class OtherProfile(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username')
        queryset = Profile.objects.get(userID=username)
        serialised_query = s.ProfileSerializer(queryset)
        return Response(serialised_query.data)

##------------------------------- GENERAL APIS -------------------------------------------------------------##
#Request with id
class TechProfilefromID(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username')
        queryset = Profile.objects.get(userID=username)
        serialised_query = s.TechnicianSerializer(queryset)
        return Response(serialised_query.data)

#Request with id
class DefectInfofromID(APIView):
    def get(self, request, format=None):
        defect_id = request.data["id"]
        queryset = Defect.objects.get(id=defect_id)
        serialised_query = s.DefectSerializer(queryset)
        return Response(serialised_query.data)

#------------------------------- SUPERVISOR/PLANNER APIS -------------------------------------------------------------##

class TechnicianList(APIView):
    def get(self, request, format=None):
        queryset = Profile.objects.filter(user_type=2)
        serialised_query = s.TechnicianSerializer(queryset, many=True)
        return Response(serialised_query.data)

class AllDefects(APIView):
    def get(self, request, format=None):
        queryset = Defect.objects.filter(closed=False)
        serialised_query = s.DefectSerializer(queryset, many=True)
        return Response(serialised_query.data)


class AssignTechnician(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        defect_id = request.data.get('id')
        Technician = Profile.objects.get(userID=username)
        Defect = Profile.objects.get(id=defect_id)
        Defect.techsAssigned.add(Technician)
        Defect.save()
        return Response({'received data': request.data})


# ------------------------------- TECHNICIAN APIS -------------------------------------------------------------##


#Request with username, return all defects associated with username
class TechnicianDefects(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username')
        queryset = Profile.objects.get(id=defect_id).prefetch_related('techsAssigned').filter(closed=False)
        serialised_query = s.DefectSerializer(queryset, many=True)
        return Response(serialised_query.data)

#Request with username, lon, lat
class TechUpdateLocation(APIView):
    def post(self, request, format=None):
        lon = request.data.get('lon')
        lat = request.data.get('lat')
        username = request.data.get('username')
        technician = Profile.objects.get(userID=username)
        technician.lon = lon
        technician.lat = lat
        technician.save()
        return Response({'received data': request.data})

#def techUpdate():

#def supUpdate():

#def plannerUpdate():