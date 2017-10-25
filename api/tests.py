# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
from api import models
from api import serializers as s
import datetime

class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        # New user created
        user = User.objects.create(
            username="testing", password="madTest1!")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, models.Profile)

class TestSerializers(TestCase):
    def setUp(self):
        User = get_user_model()
        """ Set up our test db """
        self.user = User.objects.create(
            username="testing", password="madTest1!",
            first_name='John', last_name='Alpaca')
        self.spare = models.Spare.objects.create(partID='XYZ123', name='chair')
        dtETA = datetime.datetime(2017, 10, 26, 12, 00)
        dtETD = datetime.datetime(2017, 10, 26, 16, 00)
        self.ac = models.Aircraft.objects.create(regn='SWT', acType='77W', inbound='238',
                                    outbound='237', ETA=dtETA, ETD=dtETD, bay='A13/A13/C20')
        self.user.profile.user_type = 2
        self.user.save()

        self.defect = models.Defect.objects.create(plane=self.ac, header="SEAT 24D LEGREST INOP",
                                    classCode='premium', category='seats')
        self.spareDetail = models.SpareDetail.objects.create(spare=self.spare, defect=self.defect)
        self.spareDetailBurst = models.SpareDetail.objects.create(spare=self.spare, defect=self.defect, quantity=11)

    def test_profile_change(self):
        self.user.profile.lon = 1.352083
        self.user.profile.lat = 103.819836
        self.user.save()
        self.assertEqual(self.user.profile.lon, 1.352083)
        self.assertEqual(self.user.profile.lat, 103.819836)

    def test_spares(self):
        self.assertTrue(self.spareDetail.inStock)
        self.assertFalse(self.spareDetailBurst.inStock)
        self.spareDetailBurst.drawn = True
        self.spareDetailBurst.save()
        self.assertTrue(self.spareDetailBurst.inStock)
        self.spareDetailBurst.drawn = False
        self.spareDetailBurst.save()

    def test_serializer(self):
        acSerializer = s.AircraftSerializer(self.ac)
        print(acSerializer.data)
        spareSerializer = s.SpareSerializer(self.spare)
        print(spareSerializer.data)
        sDet = s.SpareDetailSerializer(self.spareDetail)
        print(sDet.data)
        userSerializer = s.UserSerializer(self.user)
        print(userSerializer.data)
        profileSerializer = s.ProfileSerializer(self.user.profile)
        print(profileSerializer.data)
        techProfileSerializer = s.TechnicianSerializer(self.user.profile)
        print(techProfileSerializer.data)

        defectSerializer = s.DefectSerializer(self.defect)
        print(defectSerializer.data)
        print("------")
        self.defect.techsAssigned.add(self.user.profile)
        self.testUpdate = models.Update.objects.create(defect=self.defect, author=self.user.profile,
                                                    details="Whole chair broken, need extra parts")
        updateSerializer = s.UpdateSerializer(self.testUpdate)
        print(updateSerializer.data)
        print("------")
        defectSerializer = s.DefectSerializer(self.defect)
        print(defectSerializer.data)

    def tearDown(self):
        pass
