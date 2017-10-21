# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
from . import models


class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        # New user created
        user = User.objects.create(
            username="testing", password="madTest1!")
        # Check that a RoleProfile instance has been crated
        self.assertIsInstance(user.profile, models.Profile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        user.save()
        self.assertIsInstance(user.profile, models.Profile)
