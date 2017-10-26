# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.http import JsonResponse

from api import models
from api import serializers as s

import datetime

class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        # Raw user created
        user = User.objects.create(
            username="testing", password="madTest1!")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, models.Profile)

class TestAll(TestCase):
    def setUp(self):
        print(repr(models.Defect.objects.all()))
        User = get_user_model()
        """ Set up our test db """
        self.user = User.objects.create(
            username="testing", password="madTest1!",
            first_name='John', last_name='Alpaca')
        self.user.set_password('Passw0rd1')
        self.user.save()
        self.spare = models.Spare.objects.create(partID='VFRTGB', name='chair')
        dtETA = datetime.datetime(2017, 10, 26, 12, 00)
        dtETD = datetime.datetime(2017, 10, 26, 16, 00)
        self.ac = models.Aircraft.objects.create(regn='SWZ', acType='77W', inbound='238',
                                    outbound='237', ETA=dtETA, ETD=dtETD, bay='A13/A13/C20')
        self.user.profile.user_type = 2
        self.user.save()

        self.defect = models.Defect.objects.create(plane=self.ac, header="SEAT 24D LEGREST INOP",
                                    classCode='premium', category='seats')
        self.spareDetail = models.SpareDetail.objects.create(spare=self.spare, defect=self.defect)
        self.spareDetailBurst = models.SpareDetail.objects.create(spare=self.spare, defect=self.defect, quantity=11)
        self.defect.techsAssigned.add(self.user.profile)
        self.testUpdate = models.Update.objects.create(defect=self.defect, author=self.user.profile,
                                                    details="Whole chair broken, need extra parts")
    def test_profile_change(self):
        """ Test that making changes to a profile via a user and saving the
            user causes the profile to be saved as well """
        self.user.profile.lon = 1.352083
        self.user.profile.lat = 103.819836
        self.user.save()
        self.assertEqual(self.user.profile.lon, 1.352083)
        self.assertEqual(self.user.profile.lat, 103.819836)

    def test_spares(self):
        """ Test that the in stock / out of stock property works """
        self.assertTrue(self.spareDetail.inStock)
        self.assertFalse(self.spareDetailBurst.inStock)
        self.spareDetailBurst.drawn = True
        self.spareDetailBurst.save()
        self.assertTrue(self.spareDetailBurst.inStock)
        self.spareDetailBurst.drawn = False
        self.spareDetailBurst.save()

    def test_serializers(self):
        """ Test that serializers work """
        def printJson(header, testSerializer):
            print("---------------------------{}---------------------------".format(header))
            print(JsonResponse(testSerializer.data, safe=False))
            print("\n")
        acSerializer = s.AircraftSerializer(self.ac)
        printJson("Aircraft Data", acSerializer)
        spareSerializer = s.SpareSerializer(self.spare)
        printJson("Spare Data", spareSerializer)
        sDet = s.OutputSpareDetailSerializer(self.spareDetail)
        printJson("Spare Detail Data", sDet)
        userSerializer = s.UserSerializer(self.user)
        printJson("User Data", userSerializer)
        profileSerializer = s.ProfileSerializer(self.user.profile)
        printJson("Normal Profile Data", profileSerializer)
        techProfileSerializer = s.TechnicianSerializer(self.user.profile)
        printJson("Technician Profile Data", techProfileSerializer)
        updateSerializer = s.UpdateSerializer(self.testUpdate)
        printJson("Update Data", updateSerializer)
        defectSerializer = s.OutputDefectSerializer(self.defect)
        printJson("Defect Data", defectSerializer)

    def test_queryset(self):
        self.defect.techsAssigned.add(self.user.profile)
        self.anotherDefect = models.Defect.objects.create(plane=self.ac, header="SEAT 24D LEGREST INOP",
                                    classCode='premium', category='seats')
        self.anotherDefect.techsAssigned.add(self.user.profile)
        self.closedDefect = models.Defect.objects.create(plane=self.ac, header="HOHOHOHO",
                                    classCode='premium', category='seats', closed=True)
        self.closedDefect.techsAssigned.add(self.user.profile)
        #queryset = [defect for defect in self.user.profile.defectsAssigned.all() if defect.closed==False]
        queryset = self.user.profile.defectsAssigned.filter(closed=False)
        defectSerializer = s.OutputDefectSerializer(queryset, many=True)
        #print(defectSerializer.data)

    # def test_rawDefect(self):
    #     self.rawDefect = models.RawDefect.objects.create(plane=self.ac, classCode='first')
    #     rawDefectListSerializer = s.RawDefectListSerializer(self.rawDefect)
    #     self.rawSpareDetail = models.RawSpareDetail.objects.create(spare=self.spare, rawDefect=self.rawDefect)
    #     #print(rawDefectListSerializer.data)

    def test_auth(self):
        from rest_framework.test import APIClient
        client = APIClient()
        res = client.post('/auth', {'username':'12', 'password':'Passw0rd1'})
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        pass
