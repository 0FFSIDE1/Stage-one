from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
import os
import geocoder
# Create your views here.

class ApiView(APIView):
    def get(self, request):
        name = request.GET.get('visitor_name', 'Anonymous')
        ip_address = self.get_client_ip(request)   
        temp_url = 'https://api.openweathermap.org/data/2.5/weather?'
        try:
            location = self.get_location(ip_address)
        except Exception as e:
            location = request.GET.get('location', 'Unknown')
        else:
            parameter = {
            'lat': location.get('lat', 'Unknown'),
            'lon': location.get('lng', 'Unknown'),
            'appid' : 'ff331be1723434bf388539d1db89d94b',
            }
            print(parameter['appid'])
            temp = requests.get(url=temp_url, params=parameter)
            temp_data = temp.json()
            print(temp)
        finally:
            temperature = round((temp_data['main']['temp'] - 273.15))
            location = f"{location.get('city', 'unknown')}"
            greeting = f"Hello, {name}!, the temperature is {temperature} degrees Celsius in {location}"
            context = {
                'greetings': greeting,
                'location': location,
                'client_ip': ip_address,
            }
        return Response(context)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_location(self, ip):
        try:
            g = geocoder.ip(ip)
            print(g)
            if g.ok:
                return {
                    'city': g.city,
                    'lat': g.latlng[0],
                    'lng': g.latlng[1]
                }
            else:
                return {'city': 'Unknown', 'lat': 'Unknown', 'lng': 'Unknown'}
        except Exception as e:
            return {'city': 'Unknown', 'lat': 'Unknown', 'lng': 'Unknown'}
    
    
            
        
