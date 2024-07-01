from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
import os
# Create your views here.

class ApiView(APIView):
    def get(self, request):
        name = request.GET.get('name', 'Anonymous')
        print(name)
        ip_address = self.get_client_ip(request)   
        url = 'https://apiip.net/api/check'
        ACCESS_KEY = os.environ.get('ACCESS_KEY')
        params = {
            'ip': ip_address,
            'accessKey': ACCESS_KEY
        }
        temp_url = 'https://api.openweathermap.org/data/2.5/weather?'
        try:
            response = requests.get(url=url, params=params)
        except Exception as e:
            location = request.GET.get('location', 'Unknown')
        else:
            data = response.json()
            parameter = {
            'lat': data['latitude'],
            'lon': data['longitude'],
            'appid' : os.environ.get('appid'),
            }
            temp = requests.get(url=temp_url, params=parameter)
            temp_data = temp.json()
        finally:
            temperature = round((temp_data['main']['temp'] - 32) * 5/9)
            location = f"{data['city']}, {data['countryName']}"
            greeting = f"Hello, {name}!, the temperature is {temperature} degrees Celsius in {location}"
            context = {
                'name': name,
                'location': location,
                'greetings': greeting,
                'ip': ip_address,
            }
        return Response(context)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
            
        
