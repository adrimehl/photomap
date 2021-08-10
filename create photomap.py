# -*- coding: utf-8 -*-
"""
Created on Tue Aug 7 16:29:01 2021

@author: Adrian Mehl
"""


from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import pandas as pd
import base64
import folium
from folium import IFrame
from folium.plugins import LocateControl, MarkerCluster


#initialize
Folder=r'...' #Folder with pictures

custommarker=True  #use a customized marker
if custommarker==True:
    cluster_img = r'...' #Link to marker picture
    
clustering=True #choose if marker should be clustered or not

startlocation=[51.3, 13.3065] #center of location when map opens



#get picture Data
def get_exif(filename):
    exif = Image.open(filename)._getexif()

    if exif is not None:
        for key, value in exif.items():
            name = TAGS.get(key, key)
            exif[name] = exif.pop(key)

        if 'GPSInfo' in exif:
            for key in exif['GPSInfo'].keys():
                name = GPSTAGS.get(key,key)
                exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)
            for key in exif['GPSInfo'].keys():
                name = GPSTAGS.get(key,key)
                exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)

    return exif

#extract coordinates and transform into decimal
def get_decimal_coordinates(info):
    for key in ['Latitude', 'Longitude']:
        if 'GPS'+key in info:
            e = info['GPS'+key]
            info[key] = ( e[0][0]/e[0][1] +
                          e[1][0]/e[1][1] / 60 +
                          e[2][0]/e[2][1] / 3600
                        )

    if 'Latitude' in info and 'Longitude' in info:
        return [info['Latitude'], info['Longitude']]
    



points = []
filelocation=[]
time = []
for r, d, f in os.walk(Folder):
    for file in f:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(r, file)
            exif = get_exif(filepath)
            if exif is not None and 'GPSInfo' in exif:
                latlong = get_decimal_coordinates(exif['GPSInfo'])
                if latlong is not None:
                    points.append(latlong)
                    filelocation.append(filepath) #für gecroppte Fotos..
                    time.append(exif['DateTimeOriginal'])
                
time=pd.to_datetime(time, format='%Y:%m:%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')           



 
 
MyMap = folium.Map(location=startlocation, tiles='openstreetmap', zoom_start=5, max_zoom=19, control_scale=True)




if clustering==True:
    # Create marker cluster to help define clusters. Cluster will separate into individual markers at zoom level 13.
    cluster = MarkerCluster(options={'showCoverageOnHover': False,
                                        'zoomToBoundsOnClick': True,
                                        'spiderfyOnMaxZoom': False,
                                        'disableClusteringAtZoom': 13})


#Add Markers with picture to map
for i in range (0,len(points)):
    
    name = time[i] #Name of the picture
   
    encoded = base64.b64encode(open(filelocation[i], 'rb').read())
    html = '<img src="data:image/png;base64,{}">'.format
    iframe = IFrame(html(encoded.decode('UTF-8')), width=450, height=430)
    popup = folium.Popup(iframe, max_width=450)
    if custommarker==True:
        # Create custom icon with Marker
        custom_icon = folium.CustomIcon(cluster_img, icon_size=(35, 35), popup_anchor=(0, -22))
        custom_marker = folium.Marker(location=points[i], icon=custom_icon, tooltip=name, popup=popup) 
    elif custommarker==False:
        custom_marker = folium.Marker(location=points[i], icon=folium.Icon(color = 'gray'), tooltip=name, popup=popup)     
    
    if clustering==True:
        custom_marker.add_to(cluster)
    elif clustering==False:
        custom_marker.add_to(MyMap)


if clustering==True:
# Add cluster to the map
    cluster.add_to(MyMap)    

# Enable geolocation button on map.
LocateControl(auto_start=False).add_to(MyMap)

# Define webpage title html and add to script.
tab_title = '<title>' + Folder.split('\\')[-1] + '</title>'
MyMap.get_root().html.add_child(folium.Element(tab_title))

 # Save map to HTML
MyMap.save(Folder+'\\'+ Folder.split('\\')[-1] + '.html')
