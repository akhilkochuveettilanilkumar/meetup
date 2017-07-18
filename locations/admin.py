from django.contrib import admin
from .models import Locations

# Register your models here.

class LocationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'country_code', 'localized_country_name',
                    'state', 'latitude', 'longitude', 'zip_code',
                    'created_on', 'updated_on', 
    	            )


admin.site.register(Locations, LocationsAdmin)
