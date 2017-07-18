from django.conf.urls import *
from django.views.generic import TemplateView

urlpatterns = [
                url(r'^get/$', 'locations.views.get_location_using_query', name='get_locations'),
]
