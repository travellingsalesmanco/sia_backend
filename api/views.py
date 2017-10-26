# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api import models as m
from api import serializers as s
import datetime

# Create your views here.


###------------------------------ PROFILE VIEWS --------------------------------------------------------------------####
#Request with id
class TechnicianProfile(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('id')
        queryset = m.Profile.objects.get(user=username)
        serialised_query = s.TechnicianSerializer(queryset)
        return Response(serialised_query.data)

#Request with id
class OtherProfile(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('id')
        queryset = m.Profile.objects.get(user=username)
        serialised_query = s.ProfileSerializer(queryset)
        return Response(serialised_query.data)

##------------------------------- GENERAL APIS -------------------------------------------------------------##
#Request with id
class TechProfilefromID(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('id')
        queryset = m.Profile.objects.get(user=username)
        serialised_query = s.TechnicianSerializer(queryset)
        return Response(serialised_query.data)

#Request with id
class DefectInfofromID(APIView):
    def get(self, request, format=None):
        defect_id = request.query_params.get('id')
        queryset = m.Defect.objects.get(id=defect_id)
        serialised_query = s.OutputDefectSerializer(queryset)
        return Response(serialised_query.data)

#------------------------------- SUPERVISOR/PLANNER APIS -------------------------------------------------------------##

class TechnicianList(APIView):
    def get(self, request, format=None):
        queryset = m.Profile.objects.filter(user_type=2)
        serialised_query = s.TechnicianSerializer(queryset, many=True)
        return Response(serialised_query.data)

class AllDefects(APIView):
    def get(self, request, format=None):
        queryset = m.Defect.objects.filter(closed=False)
        serialised_query = s.OutputDefectSerializer(queryset, many=True)
        return Response(serialised_query.data)


# ------------------------------- TECHNICIAN APIS -------------------------------------------------------------##


#Request with username, return all defects associated with username
class TechnicianDefects(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('id')
        queryset = m.Profile.objects.get(user=username).defectsAssigned.filter(closed=False)
        serialised_query = s.OutputDefectSerializer(queryset, many=True)
        return Response(serialised_query.data)

# #Request with username, lon, lat
# class TechUpdateLocation(APIView):
#     def post(self, request, format=None):
#         lon = request.data.get('lon')
#         lat = request.data.get('lat')
#         username = request.data.get('username')
#         technician = Profile.objects.get(user__username=username)
#         technician.lon = lon
#         technician.lat = lat
#         technician.save()
#         return Response({'received data': request.data})

#TODO: input defects (from planner) and updating of defects from all parties
# ------------------------------ POST API -----------------------------------------------------------------------------#
class CreateOrUpdateDefect(APIView):
    def get_object(self, pk):
        try:
            return m.Defect.objects.get(id=pk)
        except m.Defect.DoesNotExist:
            raise Http404
    def post(self, request, format=None):
        serializer = s.InputDefectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk, format=None):
        defect = self.get_object(pk)
        serializer = s.InputDefectSerializer(defect, data=request.data, partial_update=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddUpdate(APIView):
    def post(self, request, format=None):
        serializer = s.InputUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignTechnician(APIView):
    def post(self, request, format=None):
        username = request.data.get('u_id')
        defect_id = request.data.get('d_id')
        Technician = m.Profile.objects.get(user=username)
        defect = m.Defect.objects.get(id=defect_id)
        defect.techsAssigned.add(Technician)
        defect.save()
        return Response({'received data': request.data})




        # class CreateRawDefect(APIView):
#     def post(self, request, format=None):