from django.contrib.gis.geoip2 import GeoIP2

#helper funvtions

def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country,city,lat,lon


def get_center_coordinates(latA, longA ,latB=None, longB=None):
    cord = (latA , longA)
    if latB:
        cord = [(latA+latB)/2, (longA+longB)/2]

    return cord


def get_zoom(distance):
    if distance <= 100:
        return 12
    elif distance >100 and distance <= 700:
        return 8
    elif distance >700 and distance <=3000:
        return 5

    else:
        return 3

