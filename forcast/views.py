from django.shortcuts import render
import requests
from .models import City
from django.contrib import messages

def weather_dashboard(request):
    weather_data = None 
    if request.method == 'POST':
        city_name = request.POST.get('city', '')
        api_key = '9863c041524cfd45538f437b7a9f53ad' 
        base_url = "http://api.openweathermap.org/data/2.5/weather"

        params = {
            'q': city_name,
            'appid': api_key,
            'units': 'metric',  
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            weather_data = response.json()

            # Check for the presence of 'cod' key
            if 'cod' in weather_data:
                if weather_data['cod'] != '200':
                    # Check for the presence of 'message' key before accessing it
                    error_message = weather_data.get('message', 'An error occurred.')
                    messages.error(request, f"Error: {error_message}")
                else:
                    return render(request, 'index.html', {'weather_data': weather_data})
            else:
                messages.error(request, "Invalid API response. Please try again.")

        except requests.RequestException as e:
            messages.error(request, f"Error: {str(e)}")
            
    return render(request, 'index.html', {'weather_data': weather_data})
