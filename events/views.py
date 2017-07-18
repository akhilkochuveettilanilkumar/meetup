import requests
import datetime
import json
import string

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse

from .models import EventDetails
from locations.models import Locations

# Create your views here.

EPOCH = datetime.datetime.utcfromtimestamp(0)


def convert_time_millisecond_since_epoch(datetime_obj):
    '''
        Method finds difference between the give time and epoch and
        convert the result to millseconds.
    '''

    # Taking difference since epoch
    total_seconds = (datetime_obj - EPOCH).total_seconds()

    # Converting to millisecond for api handling
    milliseconds = total_seconds * 1000

    return milliseconds


def get_events_based_on_coordinates(lat, lon):
    '''
        Method extracts data from meetup using latitude and longitude
        with radius set to 50
    '''

    all_events = []

    api_base_url = 'https://api.meetup.com'

    linking_url = '/find/events?sign=true&photo-host=public&key=%s&' %(
        settings.MEETUP_API_KEY)

    query = 'lon=%s&radius=50&lat=%s' % (lon, lat)

    url = api_base_url + linking_url + query

    response = requests.get(url)
    if response.status_code == 200:
        events = response.json()

        for event in events[:20]:
            tmp = {}
            loc = ''
            tmp['name'] = event.get('name', '')
            tmp['name'] = tmp['name'].encode('ascii',errors='ignore')
            tmp['link'] = event.get('link', '')
            tmp['event_id'] = event.get('id', '')
            tmp['description'] = event.get('description', '')
            tmp['description'] = tmp['description'].encode(
                'ascii',errors='ignore')

            tmp['fee'] = event.get('fee', '')
            tmp['currency'] = ''
            if tmp['fee']:
                tmp['currency'] = tmp['fee'].get('currency', '')
                tmp['fee'] = tmp['fee'].get('amount', '')

            tmp['status'] = event.get('status', '')

            try:
                tmp['group'] = event.get('group').get(
                    'name').encode('ascii',errors='ignore')
            except:
                tmp['group'] = ''

            tmp['address'] = event.get('venue', '')
            if tmp['address']:
                venue_lat = tmp['address'].get('lat', '')
                venue_lon = tmp['address'].get('lon', '')

                if venue_lat and venue_lon:
                    loc, created = Locations.objects.get_or_create(
                            latitude=venue_lat,
                            longitude=venue_lon)
                # Binds street, city and country to single field.
                address = ''
                if tmp['address'].get('name', ''):
                    address = address + ', %s' %(tmp['address']['name'])

                if tmp['address'].get('address_1', ''):
                    address = address + ', %s' %(tmp['address']['address_1'])
                if tmp['address'].get('address_2', ''):
                    address = address + ', %s' %(tmp['address']['address_2'])
                if tmp['address'].get('address_3', ''):
                    address = address + ', %s' %(tmp['address']['address_3'])

                if tmp['address'].get('city', ''):
                    if loc:
                        loc.city = str(tmp['address']['city'])
                    address = address + ', %s' %(tmp['address']['city'])

                if tmp['address'].get('localized_country_name', ''):
                    if loc:
                        loc.localized_country_name = str(
                            tmp['address']['localized_country_name'])
                    address = address + ', %s' %(tmp['address']['localized_country_name'])

                if loc:
                    if tmp['address'].get('state', ''):
                        loc.state = str(tmp['address']['state'])

                    if tmp['address'].get('country', ''):
                        loc.country_code = str(tmp['address']['country'])

                    if tmp['address'].get('id', ''):
                        loc.venue_id = str(tmp['address']['id'])

                    if tmp['address'].get('zip', ''):
                        loc.country_code = str(tmp['address']['zip'])    

                    loc.save()
                tmp['address'] = address


            tmp['address'] = tmp['address'].encode('ascii',errors='ignore').strip()
            if tmp['address'].startswith(','):
                tmp['address'] = tmp['address'][1:].strip()

            # Converting unicode to string for better data handling.
            tmp = [dict([key, str(value)] for key, value in tmp.iteritems())][0]

            if tmp['fee']:
                tmp['fee'] = float(tmp['fee'])
            else:
                tmp.pop('fee')

            # Since time is provided by this api in milliseconds with
            # respect to epoch. Below done code retrivves actual time
            # from epoch.

            duration = event.get('duration', 0)
            tmp['duration'] = datetime.timedelta(
                milliseconds=duration)

            tmp['start_time'] = event.get('time', 0)
            if tmp['start_time']:
                tmp['start_time'] = EPOCH + datetime.timedelta(
                    milliseconds=tmp['start_time'])

            tmp['end_time'] = tmp['start_time'] + datetime.timedelta(
                milliseconds=duration)

            # Create new instance if its not present otherwise
            # update existing entry
            event_instance, created = EventDetails.objects.get_or_create(
                name__iexact=tmp['name'], link=tmp['link'], 
                duration=tmp['duration'], start_time=tmp['start_time'], 
                end_time=tmp['end_time'] )
            event_instance.__dict__.update(tmp)
            if loc:
                event_instance.location = loc
            else:
                print "No loc..", event_instance.id 
            event_instance.save()

            # Converting datetime fields to string for json serialization.

            tmp['duration'] = str(tmp['duration'].seconds)

            tmp['start_time'] = datetime.datetime.strftime(
                tmp['start_time'], '%Y-%m-%dT%H:%M:%S')

            tmp['end_time'] = datetime.datetime.strftime(
                tmp['end_time'], '%Y-%m-%dT%H:%M:%S')

            all_events.append(tmp)

        return all_events


def home(request):
    if str(request.method) == 'GET':
        return render(request, 'events/home.html', {})

    lat = request.POST.get('lat', '')
    lon = request.POST.get('lon', '')
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')

    if not all([lat, lon]):
        return HttpResponse(json.dumps({'events': []}),
                        content_type="application/json")

    all_events = []

    if not start_date and not end_date:
        # Retirive data from meetup
        all_events = get_events_based_on_coordinates(lat, lon)

    if start_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        start = convert_time_millisecond_since_epoch(start_date)

    if end_date:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        end_date = end_date + datetime.timedelta(days=1)
        end = convert_time_millisecond_since_epoch(end_date)

    return HttpResponse(json.dumps({'events': all_events}),
                        content_type="application/json")
