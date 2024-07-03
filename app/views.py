import os
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
import geocoder
# Create your views here.

class ApiView(APIView):
    def get(self, request):
        name = request.GET.get('visitor_name', 'Anonymous')
        ip_address = self.get_client_ip(request)   
        print(ip_address)
        temp_url = 'https://api.openweathermap.org/data/2.5/weather?'
        location = self.get_location(ip_address)
        appid = os.environ.get('appid')
        try:
            place = location['city']
            parameter = {
            'q': place,
            'appid' : appid,
            }
            temp = requests.get(url=temp_url, params=parameter)
            temp_data = temp.json()
            temperature = round((temp_data['main']['temp'] - 273.15))
            greeting = f"Hello, {name}!, the temperature is {temperature} degrees Celsius in {place}"
        except KeyError:
            temperature = 0
            place = 'Unknown'
            greeting = f"Hello, {name}!, the temperature is {temperature} degrees Celsius in {place}"
        finally:
            context = {
                'greetings': greeting,
                'location': place,
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
        g = geocoder.ip(ip)
        if g.status == 'OK':
            return g.json
        else:
            return {'city': 'Unknown'}
            
    
            
