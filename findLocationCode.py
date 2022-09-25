import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area[name="İstanbul"];
(node(area)[amenity=restaurant][name];
way(area)[amenity=restaurant][name];
rel(area)[amenity=restaurant][name];
);
out center;
"""
response = requests.get(overpass_url,
                        params={'data': overpass_query})
data = response.json()


print(data)
coords = []
for element in data['elements']:
  if element['type'] == 'node':
    lon = element['lon']
    lat = element['lat']
    coords.append((lon, lat))
  elif 'center' in element:
    lon = element['center']['lon']
    lat = element['center']['lat']
    coords.append((lon, lat))

print(coords)


