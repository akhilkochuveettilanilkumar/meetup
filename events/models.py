from django.db import models

from locations.models import Locations

# Create your models here.

class EventDetails(models.Model):
    '''
        Following are the mandatory params:
            * name
            * duration
            * start_time
            * end_time
    '''

    name = models.CharField(max_length=500)
    link = models.URLField(max_length=1000, null=True, blank=True,)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    fee = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=25, null=True, blank=True)
    group = models.CharField(max_length=250, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Locations, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
