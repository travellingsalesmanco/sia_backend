# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import timezone

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
    user_type = models.IntegerField(null=True, choices=USER_TYPES)

    # Attribute: User profile pic
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
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
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    class Meta:
        abstract = True

class Profile(TechnicianProfile, SupervisorProfile, PlannerProfile, BaseProfile):
    pass

class Aircraft(models.Model):
    # Attribute: Aircraft registration ID
    regn = models.CharField(max_length=10, primary_key=True)

    # Attribute: Aircraft type
    acType = models.CharField(max_length=10, blank=True)

    # Attribute: Inbound flight number
    inbound = models.IntegerField(null=True, blank=True)

    # Attribute: Outbound flight number
    outbound = models.IntegerField(null=True, blank=True)

    # Attribute: Ground time (ETA/ETD stored seperately)
    ETA = models.DateTimeField(null=True, blank=True)
    ETD = models.DateTimeField(null=True, blank=True)

    # Attribute: Aircraft bay Location
    bay = models.CharField(max_length=50, blank=True)

class RawDefect(models.Model):
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

    # Relationship: ManyToOne with Aircraft
    plane = models.ForeignKey(Aircraft, related_name='rawDefects', blank=True)

    # Attribute: defect number
    # id = models.AutoField(primary_key=True)
    # NOTE: This field is defined by default for every model

    # Attrubute: Defect header
    header = models.CharField(max_length=150, blank=True)

    # Attribute: Additional Info
    description = models.TextField(blank=True)

    # Attribute: Date reported
    dateReported = models.DateTimeField(default=timezone.now)

    # Attribute: Class
    classCode = models.CharField(max_length=15, choices=CLASS_CODES, blank=True)

    # Attribute: Category
    category = models.CharField(max_length=15, choices=CATEGORIES, blank=True)

    # Attribute: Image of Defect
    img = models.ImageField(upload_to='defects', null=True, blank=True)

    # Attribute: Priority of defect (e.g. safety item / HHQ flagged impt)
    # NOTE: 0 - low priority, 2 - high priority
    priority = models.IntegerField(default=0)

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
    techsAssigned = models.ManyToManyField(Profile, related_name='defectsAssigned', blank=True)

    # Relationship: ManyToOne with Aircraft
    plane = models.ForeignKey(Aircraft, related_name='defects')

    # Attribute: defect number
    # id = models.AutoField(primary_key=True)
    # NOTE: This field is defined by default for every model

    # Attrubute: Defect header
    header = models.CharField(max_length=150)

    # Attribute: Additional Info
    description = models.TextField(blank=True)

    # Attribute: Resolution status
    closed = models.BooleanField(default=False)

    # Attribute: Date reported
    dateReported = models.DateTimeField(default=timezone.now)

    # Attribute: Date resolved
    dateResolved = models.DateTimeField(null=True, blank=True)

    # Attribute: Class
    classCode = models.CharField(max_length=15, choices=CLASS_CODES)

    # Attribute: Category
    category = models.CharField(max_length=15, choices=CATEGORIES)

    # Attribute: Image of Defect
    img = models.ImageField(upload_to='defects', null=True, blank=True)

    # Attribute: Priority of defect (e.g. safety item / HHQ flagged impt)
    # NOTE: 0 - low priority, 2 - high priority
    priority = models.IntegerField(default=0)

class Spare(models.Model):
    # Attribute: Part ID
    partID = models.CharField(max_length=20, primary_key=True)

    # Attribute: Part name
    name = models.CharField(max_length=50)

    # Attribute: Amount in inventory
    stock = models.PositiveIntegerField(default=10)

class SpareDetailBase(models.Model):
    # Relationship: ManyToOne with Spare (each SpareDetail is tagged to 1 spare)
    spare = models.ForeignKey(Spare, related_name='uses')

    # Attribute: Amount required
    quantity = models.PositiveIntegerField(default=1)

    # Attribute: Stores have been removed from inventory
    drawn = models.BooleanField(default=False)

    # Custom property: Whether there is stock remaining
    @property
    def inStock(self):
        return (self.quantity <= self.spare.stock) if not self.drawn else True

    class Meta:
        abstract = True

class SpareDetail(SpareDetailBase):
    # Relationship: ManyToOne with Defect (each SpareDetail is tagged to 1 defect)
    defect = models.ForeignKey(Defect, related_name='spares')

class RawSpareDetail(SpareDetailBase):
    # Relationship: ManyToOne with Spare (each SpareDetail is tagged to 1 spare)
    spare = models.ForeignKey(Spare, related_name='rawUses')
    # Relationship: ManyToOne with Defect (each SpareDetail is tagged to 1 defect)
    rawDefect = models.ForeignKey(RawDefect, related_name='spares')

class Update(models.Model):
    # Relationship: ManyToOne with Defect
    defect = models.ForeignKey(Defect, related_name='updates')

    # Relationship: ManyToOne with Profile
    author = models.ForeignKey(Profile, related_name='history')

    # Attribute: Description
    details = models.TextField()

    # Attribute: Time stamp created
    created = models.DateTimeField(auto_now_add=True)
