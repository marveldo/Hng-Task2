from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import renderers
from rest_framework.response import Response
import requests
import json
import geocoder
from rest_framework import status
from ipware import get_client_ip
# Create your views here.


class AboutUserview(APIView):
    renderer_classes = [renderers.JSONRenderer]
    
    def get_ip(self,request):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if not ip_address:
           ip_address = request.META.get('REMOTE_ADDR')
        return ip_address
    def get_city(self, ip):
       
        location = geocoder.ip(ip)
        city = location.city
        print(city)
        return city
       
    
    def get_weather(self,city) :
        current_temp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=a8e71c9932b20c4ceb0aed183e6a83bb&units=imperial')
        temp = current_temp.json()['main']['temp']
      
        return temp
    
    def convert_to_celsius(self, farenheit):
        return f"{(farenheit - 32) * 5.0/9.0 : .2f}"
    
    def get(self, request, *args, **kwargs):

        if self.request.GET.get('visitor_name'):
           name = self.request.GET.get('visitor_name')
           ip = self.get_ip(request)
           city = self.get_city(ip)
           temp = self.get_weather(city)
           res = {'client_ip' : ip,
               'location' : city,
               'greeting': f'hello {name}! the temperature is {self.convert_to_celsius(temp)} celsius in {city}'
        
               }
           return Response(res, status=status.HTTP_200_OK)
        else:
            return Response('Visitor name not used', status=status.HTTP_400_BAD_REQUEST)
    

