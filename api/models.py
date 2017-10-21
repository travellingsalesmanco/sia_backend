# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

class Defect(models.Model):
    blah


class BaseProfile(models.Model):
    USER_TYPES = (
        (0, 'Planner'),
        (1, 'Supervisor'),
        (2, 'Technician')
    )
    # Relationship: OneToOne with a User
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True)
    # Attribute: Type of user
    user_type = models.IntegerField(max_length=2, null=True,
                                    choices=USER_TYPES)

    class Meta:
        abstract = True

class PlannerProfile(models.Model):
    # Stuff specific to planner goes here
    class Meta:
        abstract = True
class SupervisorProfile(models.Model):
    # Stuff specific to Supervisor goes here
    class Meta:
        abstract = True
class TechnicianProfile(models.Model):
    # Stuff specific to Technician goes here
    class Meta:
        abstract = True

class Profile(TechnicianProfile, SupervisorProfile, PlannerProfile, BaseProfile):
    pass
