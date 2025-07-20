import requests
from django.shortcuts import render
from decouple import config

def index(request):
    weather_data = {}
    city = 'Delhi'  # Default city
    
    if request.method == 'POST':
        city = request.POST.get('city', 'Delhi').strip()

    api_key = config("OPENWEATHER_API_KEY")  # Replace with your OpenWeatherMap API key
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'city': city.title(), 
                'country_code': data['sys']['country'],
                'coordinate': f"{data['coord']['lon']}, {data['coord']['lat']}",
                'temp': f"{data['main']['temp']} °C",
                'pressure': f"{data['main']['pressure']} hPa",
                'humidity': f"{data['main']['humidity']}%",
                'icon': data['weather'][0]['icon'],
            }
        else:
            weather_data = {
                'city': city.title(),
                'error': data.get('message', 'Could not retrieve weather data')
            }

    except Exception as e:
        weather_data = {'error': str(e)}

    return render(request, 'main/index.html', weather_data)
