from django.urls import path

from .views import calculate_distance_view

app_name = 'projectapp'

urlpatterns = [
    path('',calculate_distance_view,name= 'calculate_distance_view')
]
