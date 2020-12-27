import pandas as pd
import geocoder
import folium
import webbrowser as wb

#function that handles geocoding operation
def geocoderFunc():
    #creating a new csv to write geocoded values
    f = open('geocoded_latlng.csv', 'w+')
    #adding the heading row
    f.write("label;address;lat;lng\n")
    #reading raw data to be geocoded
    data = pd.read_csv('basvuru_noktalari.csv',sep=";", engine='python', header=0)
    #reading, converting and writing row by row
    for ind in data.index:
        #adding city column to the address to be looked for to get better results
        completeAddress=data['adress'][ind]+" , "+data['city'][ind]

        #bing geocoder first option, works faster but requires api key, that's why I commented it out
        #coord= geocoder.bing(completeAddress, key='AmJGP7kiFBbJLXZ-JScwvJpNm3BWmDcJS3JiNoxJKT0HqvqgBgLFyEGE1MRhxdTu')

        #arcgis geocoder 2nd option, slower but it doesn't require any api key
        coord= geocoder.arcgis(completeAddress)
        #writing values into a new text file defined at the beginning
        f.write(data['label'][ind])
        f.write(';')
        f.write(completeAddress)
        f.write(';')
        f.write(str(coord.latlng[0]))
        f.write(';')
        f.write(str(coord.latlng[1]))
        f.write('\n')


#this function helps overlaying geocoded coordinates on a map to visually check the final output
def mapToCheckFunc():
    #read data from recently created latlng file
    data = pd.read_csv('geocoded_latlng.csv', sep=";", engine='python', header=0)
    #adjusting map view accordingly
    map = folium.Map(location=[data['lat'][0],data['lng'][0]], zoom_start=10, control_scale=True)
    #reading coordinates and locating them on the map in order
    for ind in data.index:
        folium.Marker([data['lat'][ind], data['lng'][ind]], popup=folium.Popup(data['address'][ind], max_width=200)).add_to(map)
    #saving the output to an html file
    map.save(outfile='map.html')
    #automatically opening the test map on the browser to see the results
    url='map.html'
    wb.open(url, new=2)


geocoderFunc()
mapToCheckFunc()









