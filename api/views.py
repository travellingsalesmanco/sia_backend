# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from api import models as m
from api import serializers as s
import datetime

# Create your views here.


###------------------------------ PROFILE VIEWS --------------------------------------------------------------------####
#Request with id
# class TechnicianProfile(APIView):
#     def get(self, request, format=None):
#         username = request.query_params.get('id')
#         queryset = m.Profile.objects.get(user=username)
#         serialised_query = s.TechnicianSerializer(queryset)
#         return Response(serialised_query.data)

#Request with id
class OtherProfileDetail(generics.RetrieveAPIView):
    queryset = m.Profile.objects.all()
    serializer_class = s.ProfileSerializer
    
class OtherProfileList(generics.ListAPIView):
    queryset = m.Profile.objects.all()
    serializer_class = s.ProfileSerializer

##------------------------------- GENERAL APIS -------------------------------------------------------------##
#Request with id
class TechDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve or update a technician's details via GET/PUT/PATCH """
    queryset = m.Profile.objects.filter(user_type=2)
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return s.TechnicianSerializer
        return s.InputTechnicianSerializer

class DefectDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Edit or view a single defect details using GET/PUT/PATCH/DELETE """
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return s.OutputDefectSerializer
        return s.InputDefectSerializer
    queryset = m.Defect.objects.all()
    # Default lookup field is primary key, default arg is pk

    def perform_update(self, serializer):
        instance = serializer.save()
        # Add timestamp if update closed
        if instance.closed and instance.dateResolved == None:
            instance.dateResolved = timezone.now()
            instance.save()

#------------------------------- SUPERVISOR/PLANNER APIS -------------------------------------------------------------##

class TechnicianList(generics.ListAPIView):
    """ GET list of technicians """
    queryset = m.Profile.objects.filter(user_type=2)
    serializer_class = s.TechnicianSerializer

class DefectsList(generics.ListCreateAPIView):
    """ List or create Defects via GET/POST """
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return s.InputDefectSerializer
        return s.OutputDefectSerializer
    queryset = m.Defect.objects.filter(closed=False)


# ------------------------------- TECHNICIAN APIS -------------------------------------------------------------##


#Request with username, return all defects associated with username
class TechnicianDefects(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('id')
        queryset = m.Profile.objects.get(user=username).defectsAssigned.filter(closed=False).order_by('priority', 'dateReported')
        serialised_query = s.OutputDefectSerializer(queryset, many=True)
        return Response(serialised_query.data)

class TechnicianHistory(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('id')
        queryset = m.Profile.objects.get(user=username).defectsAssigned.filter(closed=True).order_by('-id')[:10]
        serialised_query = s.OutputDefectSerializer(queryset, many=True)
        return Response(serialised_query.data)


#TODO: input defects (from planner) and updating of defects from all parties
# ------------------------------ POST API -----------------------------------------------------------------------------


class AddOrRemoveUpdate(APIView):
    def get_defect(self, pk):
        try:
            return m.Defect.objects.get(id=pk)
        except m.Defect.DoesNotExist:
            raise Http404
    def get_update(self, pk):
        try:
            return m.Update.objects.get(id=pk)
        except m.Update.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        serializer = s.InputUpdateSerializer(data=request.data)
        defect = self.get_defect(pk)
        if serializer.is_valid():
            serializer.save(defect=defect)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        # Delete the entire update

        #defect = self.get_defect(pk)
        update = self.get_update(request.data.get('id'))
        update.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddOrRemoveTechnician(APIView):
    """ Add or remove technician from a defect """
    def get_defect(self, pk):
        try:
            return m.Defect.objects.get(id=pk)
        except m.Defect.DoesNotExist:
            raise Http404
    def get_technician(self, pk):
        try:
            return m.Profile.objects.get(user=pk)
        except m.Update.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        defect = self.get_defect(pk)
        technician = self.get_technician(request.data.get('id'))
        defect.techsAssigned.add(technician)
        defect.save()
        return Response({'received data': request.data})
    def delete(self, request, pk, format=None):
        # Remove the relation
        defect = self.get_defect(pk)
        technician = self.get_technician(request.data.get('id'))
        defect.techsAssigned.remove(technician)
        defect.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddOrRemoveSpareDetail(APIView):
    def get_defect(self, pk):
        try:
            return m.Defect.objects.get(id=pk)
        except m.Defect.DoesNotExist:
            raise Http404
    def get_spareDetail(self, pk):
        try:
            return m.SpareDetail.objects.get(id=pk)
        except m.Update.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        defect = self.get_defect(pk)
        serializer = s.InputSpareDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(defect=defect)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        # Delete the entire spare detail

        # defect = self.get_defect(pk)
        spareDetail = self.get_spareDetail(request.data.get('id'))
        spareDetail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
