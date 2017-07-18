from django.db import models

# Create your models here.

class Locations(models.Model):
    city  = models.CharField(max_length=1000, null=True, blank=True)
    country_code = models.CharField(max_length=50, null=True, blank=True)
    localized_country_name = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=1000, null=True, blank=True)
    latitude = models.FloatField(default=None)
    longitude = models.FloatField(default=None)
    zip_code = models.CharField(null=True, blank=True, max_length=50)
    venue_id = models.CharField(null=True, blank=True, max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
    	if self.city:
            return self.city
        elif self.state:
        	return self.state