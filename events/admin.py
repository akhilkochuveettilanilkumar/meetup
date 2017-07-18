from django.contrib import admin
from .models import EventDetails

# Register your models here.

class EventDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'duration',
                    'start_time', 'end_time', 'fee', 'currency',
                    'status', 'group', 'address', 'created_on',
                    'updated_on'
    	            )


admin.site.register(EventDetails, EventDetailsAdmin)
