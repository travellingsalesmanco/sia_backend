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

class Aircraft(models.Model):
    # Attribute: Aircraft registration ID
    regn = models.CharField(max_length=10, primary_key=True)

    # Attribute: Aircraft type
    acType = models.CharField(max_length=10)

    # Attribute: Inbound flight number
    inbound = models.IntegerField()

    # Attribute: Outbound flight number
    outbound = models.IntegerField()

    # Attribute: Ground time (ETA/ETD stored seperately)
    ETA = models.DateTimeField()
    ETD = models.DateTimeField()

    # Attribute: Aircraft bay Location
    bay = models.CharField(max_length=50)

class Spare(models.Model):
    # Attribute: Part ID
    partID = models.CharField(max_length=20, primary_key=True)

    # Attribute: Part name
    name = models.CharField(max_length=50)

    # Attribute: Amount in inventory
    stock = models.PositiveIntegerField(default=10)

class Defect(models.Model):
    CLASS_CODES = (
        ('economy', 'Economy'),
        ('premium', 'Premium'),
        ('buisness', 'Buisness'),
        ('first', 'First')
    )
    CATEGORIES = (
        ('seats', 'Seats'),
        ('galley', 'Galley'),
        ('lavatory', 'Lavatory')
    )

    # Relationship: ManyToMany with Profile
    techsAssigned = models.ManyToManyField(Profile, related_name='defectsAssigned')

    # Relationship: ManyToOne with Aircraft
    plane = models.ForeignKey(Aircraft, related_name='defects')

    # Attribute: defect number
    # id = models.AutoField(primary_key=True)
    # NOTE: This field is defined by default for every model

    # Attrubute: Defect header
    header = models.CharField(max_length=150)

    # Attribute: Action to take
    action = models.TextField()

    # Attribute: Resolution status
    closed = models.BooleanField(default=False)

    # Attribute: Date reported (updated automatically when defect is created)
    dateReported = models.DateTimeField(auto_now_add=True)

    # Attribute: Date resolved
    dateResolved = models.DateTimeField(null=True, blank=True)

    # Attribute: Class
    classCode = models.CharField(choices=CLASS_CODES)

    # Attribute: Category
    category = models.CharField(choices=CATEGORIES)

    # TODO: Attribute: History

    # Attribute: Image of Defect
    img = models.ImageField(null=True, blank=True)

    # Attribute: Priority of defect (e.g. safety item / HHQ flagged impt)
    # NOTE: 0 - low priority, 2 - high priority
    priority = models.IntegerField(max_length=2, default=0)


class SpareDetail(models.Model):
    # Relationship: ManyToOne with Spare (each SpareDetail is tagged to 1 spare)
    spare = models.ForeignKey(Spare, related_name='uses')

    # Relationship: ManyToOne with Defect (each SpareDetail is tagged to 1 defect)
    defect = models.ForeignKey(Defect, related_name='spares')

    # Attribute: Amount required
    quantity = models.PositiveIntegerField(default=1)

    # Attribute: Stores have been removed from inventory
    drawn = models.BooleanField(default=False)

    # Custom property: Whether there is stock remaining
    @property
    def inStock(self):
        return (self.spare.stock >= quantity) if not drawn else True
