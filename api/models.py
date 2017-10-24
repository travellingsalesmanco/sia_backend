# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

class BaseProfile(models.Model):
    USER_TYPES = (
        (0, 'Planner'),
        (1, 'Supervisor'),
        (2, 'Technician')
    )
    # Relationship: OneToOne with a User
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True,
                                related_name='profile',
                                on_delete=models.CASCADE)

    # Custom property userID, which is really the username in the User model
    @property
    def userID(self):
        return self.user.username

    # Attribute: Type of user
    user_type = models.IntegerField(max_length=2, null=True,
                                    choices=USER_TYPES)

    # Attribute: User profile pic
    avatar = models.ImageField(null=True, blank=True)
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

    # Attribute: Location of user (stored seperately as lon, lat)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    class Meta:
        abstract = True

class Profile(TechnicianProfile, SupervisorProfile, PlannerProfile, BaseProfile):
    pass

class Defect(models.Model):
    # Relationship: ManyToMany with Profile
    techsAssigned = models.ManyToManyField(Profile, related_name='defectsAssigned')

    # Attribute: defect id
    # id = models.AutoField(primary_key=True)
    # NOTE: This field is defined by default for every model

    # Attrubute: Defect header
    header = models.CharField(max_length=150)

    # Attribute: Plane ID
    plane = models.CharField(max_length=10)

    # Attribute: Aircraft bay Location
    bayLocation = models.CharField(max_length=50)

    # Attribute: Action to take
    action = models.TextField()

    # TODO: Attribute: Spares required

    # Attribute: Resolution status
    closure = models.BooleanField(default=False)


    # Attribute: Ground time (i.e. window of work, ETA-ETD stored seperately)
    ETA = models.DateTimeField()
    ETD = models.DateTimeField()

    # Attribute: Date reported (updated automatically when defect is created)
    dateReported = models.DateTimeField(auto_now_add=True)

    # Attribute: Date resolved
    dateResolved = models.DateTimeField(null=True, blank=True)

    # TODO: Attribute: History

    # Attribute: Image of Defect
    img = models.ImageField(null=True, blank=True)

    # Attribute: Priority of defect (e.g. safety item / HHQ flagged impt)
    # NOTE: 0 - low priority, 2 - high priority
    priority = models.IntegerField(max_length=2, default=0)
