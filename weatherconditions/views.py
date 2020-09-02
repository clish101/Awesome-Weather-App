import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import City
from .forms import CreateForm
from django.contrib import messages


def home(request):
    cities = City.objects.all().order_by('-id')
    form = CreateForm()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e32113a1ea5313da25e1151fa87874c1'
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data.get('name')
            new_city_count = City.objects.filter(name=new_city).count()
            print('This is the number of cities with that name ', new_city_count)
            if new_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                    return redirect('home')
                else:
                    messages.warning(
                        request, f'There was an error retrieving city named {new_city}')
            else:
                messages.warning(
                    request, f'The city with the name {new_city} has already been added')

    weathercities = []
    for city in cities:
        try:
            # city = 'Nairobi'
            r = requests.get(url.format(city)).json()
            city_weather = {
                'id': city.pk,
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon']

            }
            print(city_weather)
            weathercities.append(city_weather)

        except Exception as e:

            messages.warning(
                request, f'There was a problem retrieving data for {city} city')
        finally:
            print("The request was successfully performed")
    context = {'city_weather': weathercities, 'form': form}
    return render(request, 'weatherconditions/weather.html', context)


def delete(request, city_pk):
    City.objects.get(id=city_pk).delete()
    return redirect('home')
