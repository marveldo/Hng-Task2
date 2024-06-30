from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import renderers
from rest_framework.response import Response
import requests
import json
from rest_framework import status
# Create your views here.


class AboutUserview(APIView):
    renderer_classes = [renderers.JSONRenderer]

    
    
       
    
    def get_weather(self,city) :
        current_temp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=a8e71c9932b20c4ceb0aed183e6a83bb&units=imperial')
        temp = current_temp.json()['main']['temp']
      
        return temp
    
    def convert_to_celsius(self, farenheit):
        return f"{(farenheit - 32) * 5.0/9.0 : .2f}"
    
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('visitor_name'):
           name = self.request.GET.get('visitor_name')
           ip = json.loads(requests.get('https://api.ipify.org?format=json').text)
           city = json.loads(requests.get(f'http://ip-api.com/json/{ip["ip"]}').text)['city']
           temp = self.get_weather(city)
           res = {'client_ip' : ip["ip"] ,
               'location' : city,
               'greeting': f'hello {name}! the temperature is {self.convert_to_celsius(temp)} in {city}'
        
               }
           return Response(res, status=status.HTTP_200_OK)
        else:
            return Response('Visitor name not used', status=status.HTTP_400_BAD_REQUEST)
    

