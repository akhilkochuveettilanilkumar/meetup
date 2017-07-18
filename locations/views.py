import json
import requests

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import HttpResponse

from .models import Locations

# Create your views here.

def get_location_using_query(request):
	if request.method == 'POST':
		return HttpResponse(json.dumps({'error': 'invalid request'}),
                                    content_type="application/json")

    query = request.GET.get('query', '')
    lat = request.GET.get('lat', '')
    lon = request.GET.get('lon', '')

    if lat and lon:
    	location_instance = Locations.objects.filter(latitude=lat, longitude=lon)
        if location_instance.exists():
        	place = location_instance.first().__dict__()
        	return HttpResponse(json.dumps({'data', place}),
                                    content_type="application/json")

    api_base_url = 'https://api.meetup.com'

    linking_url = '/2/cities?query=%s&sign=true&key=%s' % (query, settings.MEETUP_API_KEY)

    url = api_base_url + linking_url

    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        
        print response