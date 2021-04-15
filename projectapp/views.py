from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Photon
from geopy.distance import geodesic
from .utils import get_geo, get_center_coordinates, get_zoom
import folium

# Create your views here.
# def home(request):
# return render(request,"index.html")


def calculate_distance_view(request):
    distance = None
    destination = None
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Photon(user_agent='projectapp')

    ip = '103.98.78.198'
    country, city, lat, lon = get_geo(ip)
    #print('location country',country)
    #print('location city',city)
    #print('location lat,lon',lat,lon)

    location = geolocator.geocode(city)
    # print('###', location)

    # location coordinates

    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

   # initial folium map
    m = folium.Map(width=1120, height=640,
                   location=get_center_coordinates(l_lat, l_lon), zoom_start=8)

    # location marker

    folium.Marker([l_lat, l_lon], tooltip='click here for more',
                  popup=city['city'], icon=folium.Icon(color='red')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        # print(destination)
        d_lat = (destination.latitude)
        d_lon = (destination.longitude)

        pointB = (d_lat, d_lon)

        distance = round(geodesic(pointA, pointB).km, 2)

        # folium map modification

        m = folium.Map(width=1000, height=600, location=get_center_coordinates(
            l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distance))

        # location marker

        folium.Marker([l_lat, l_lon], tooltip='click here for more',
                      popup=city['city'], icon=folium.Icon(color='red')).add_to(m)

        # destination marker

        folium.Marker([d_lat, d_lon], tooltip='click here for more',
                      popup=destination, icon=folium.Icon(color='blue', icon='cloud')).add_to(m)

        # line between location and destination
        line = folium.PolyLine(
            locations=[pointA, pointB], weight=2,  color='blue')
        m.add_child(line)

        instance.location = location
        instance.distance = distance
        instance.save()

    m = m._repr_html_()

    context = {
        'distance': distance,
        'destination': destination,
        'form': form,
        'map': m,
    }

    return render(request, 'measurements/main.html', context)
