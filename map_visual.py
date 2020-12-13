from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple


def map_values(y: int, locations: Dict[str, Tuple[float]], data: Dict[str, Dict[int, List[float]]]) -> None:
    """Map state temperature and wildfire location in given year. """

    map = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
                  projection='lcc', lat_1=32, lat_2=45, lon_0=-95)
    map.readshapefile('st99_d00', name='states', drawbounds=True)
    map.drawcoastlines()
    map.drawstates()
    map.drawcountries()

    states = map.__dict__['states']
    states_info = map.__dict__['states_info']

    state_names = []
    for shape_dict in states_info:
        state_names.append(shape_dict['NAME'])

    ax = plt.gca()

    for state in data:

        wildfires = data[state][y][2]
        latitude = locations[state][0]
        longitude = locations[state][1]
        temp = data[state][y][0]

        seg = states[state_names.index(state)]
        poly = Polygon(seg, facecolor=get_colour(temp), edgecolor='black')
        poly.set_alpha(100)
        ax.add_patch(poly)

        if wildfires > 0:
            map.scatter(longitude, latitude, latlon=True, s=100 + (wildfires * 10), c='gray')


def get_colour(temp: float) -> str:
    """Provide colour of state based on temperature data."""

    colour = ''
    if temp < 40:
        colour = 'navy'
    elif 40 <= temp < 45:
        colour = 'mediumblue'
    elif 45 <= temp < 50:
        colour = 'cyan'
    elif 50 <= temp < 55:
        colour = 'gold'
    elif 55 <= temp < 60:
        colour = 'orange'
    elif 60 <= temp <= 70:
        colour = 'red'
    elif 70 < temp:
        colour = 'firebrick'
    return colour
