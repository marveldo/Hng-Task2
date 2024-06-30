from django.urls import path
from .views import *


urlpatterns = [
    path('hello',AboutUserview.as_view())
]