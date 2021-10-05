from urllib.error import HTTPError

from django.shortcuts import render, redirect
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request

from django.urls import reverse

from .models import Location

def index(request):
    data = {}
    if request.method == 'GET' and 'city' in request.GET.keys():
        city = request.GET['city'].title()
        ''' api key might be expired use your own api_key
            place api_key in place of appid ="your_api_key_here "  '''

        # source contain JSON data from API
        try:
            source = urllib.request.urlopen(
                'http://api.openweathermap.org/data/2.5/weather?q='
                + city + '&appid=8f0981e79e7f236c337190e9782f7219').read()
        except HTTPError:
            data = {"bob": 'bob'}
        else:
            # converting JSON data to a dictionary
            list_of_data = json.loads(source)

            # data for variable list_of_data
            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ', '
                              + str(list_of_data['coord']['lat']),
                "temp": str(round((list_of_data['main']['temp']) - 273.15)) + 'C',
                "weather": list_of_data['weather'],
                "pressure": str(list_of_data['main']['pressure']) + ' hPa',
                "humidity": str(list_of_data['main']['humidity']) + '%',
                "city_name": city
            }
            if Location.objects.filter(name=city).count():
                data.update({"pen": 'pen'})
    elif request.method == 'POST':
        if 'city' in request.POST.keys():
            city = request.POST['city']
            if city:
                location = Location()
                location.user = request.user
                location.name = city
                location.save()
            return redirect(reverse('home') + '?city=' + city)


    data['locs'] = Location.objects.all()

    return render(request, "main/index.html", data)
