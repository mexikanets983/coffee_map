import json
import requests
from geopy import distance
import folium
from flask import Flask


with open("coffee.json", "r", encoding="CP1251") as my_file:
    file_content = my_file.read()

data = json.loads(file_content)

apikey = 'a3c0d8fd-8046-4544-af59-a6047dfdb37c'

address = input("Где вы находитесь?:")
address_2 = address
coffee_data = []


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


coords = fetch_coordinates(apikey, address)
coords_2 = fetch_coordinates(apikey, address_2)
print('Ваши координаты:', coords)


for coffee_shop in data:
    name = coffee_shop['Name']
    width = coffee_shop["Latitude_WGS84"]
    longitude = coffee_shop["Longitude_WGS84"]

    coords = (float(width), float(longitude))
    distance_to_vadim = distance.distance(coords, (float(coords_2[0]), float(coords_2[1]))).km

    coffee_info = {
        'name': name,
        'distance': distance_to_vadim,
        'latitude': width,
        'longitude': longitude
    }

    coffee_data.append(coffee_info)

coffee_data_sorted = sorted(coffee_data, key=lambda k: k['distance'])


for coffee_info in coffee_data_sorted[:5]:
    print(coffee_info['name'])
    print(f"Расстояние: {round(coffee_info['distance'], 2)} км")
    print(f"Широта: {coffee_info['latitude']}")
    print(f"Долгота: {coffee_info['longitude']}")
    print()
    latitude = coffee_info['latitude']
    longitude = coffee_info['longitude']
    m = folium.Map(location=[longitude, latitude], zoom_start=13)
    folium.Marker(
        location=[latitude, longitude],
        popup=coffee_info['name'],
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    m.save("index.html")

m = folium.Map(location=[float(coords_2[0]), float(coords_2[1])], zoom_start=13)


for coffee_info in coffee_data_sorted[:5]:
    print(coffee_info['name'])
    print(f"Расстояние: {round(coffee_info['distance'], 2)} км")
    print(f"Широта: {coffee_info['latitude']}")
    print(f"Долгота: {coffee_info['longitude']}")
    print()

    latitude = coffee_info['latitude']
    longitude = coffee_info['longitude']

    folium.Marker(
        location=[latitude, longitude],
        popup=coffee_info['name'],
        icon=folium.Icon(color="green", icon="info-sign"),
    ).add_to(m)

m.save("index.html")


def coffe_map():
    with open('index.html') as file:
        return file.read()


app = Flask(__name__)
app.add_url_rule('/', 'coffemap', coffe_map)
app.run('0.0.0.0')
