import folium
import pandas as pd
import argparse
import os
import geopandas as gpd
from folium import plugins
from IPython.display import HTML


def parse_opt(known=False):
	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type=str, help = 'input html file')
	parser.add_argument('--input2',type=str, default='', help='addon dataframe')
	#parser.add_argument('--app', type=list,nargs='+', help='approach') #format is [app,(x),(y)], eg [app1,1,2]
	return parser.parse_known_args()[0] if known else parser.parse_args()

def get_file(file_format):
    if file_format=='':
        return pd.DataFrame()
    else:
        _, file_ext = os.path.splitext(file_format)
        file = file_ext[1:]
        if file == "xlsx":
            df = pd.read_excel(file_format)
            return df
        elif file == "csv":
            df = pd.read_csv(file_format)
            return df
        else:
            print('file can only be excel or csv')

def isNaN(string):
    return string != string

def main(opt):
    # Create a map centered around the first location
    df = get_file(opt.input)
    df2 = get_file(opt.input2)
    map_center = [df['Latitude'][0], df['Longitude'][0]]
    map_zoom = 10


    # Create a map object
    map_obj = folium.Map(location=map_center, zoom_start=map_zoom)

    # Add markers to the map for each location
    for index, row in df.iterrows():
        name= row['name']
        add = row['address']
        lat = row['Latitude']
        lon = row['Longitude']
        link =row['website']
        link2 = f'https://{link}'
        if isNaN(link):
                 marker = folium.Marker(location=[lat, lon], tooltip=name, popup=name)       
        else:     
                 link2 = f'https://{link}'
                #tooltip = folium.Popup(f'<a href="{link}" target="_blank">{name}</a>', max_width=300)
                 marker = folium.Marker(location=[lat, lon], tooltip=name, popup=f'<a href="{link2}" target="_blank">{name}</a>')        
        marker.add_to(map_obj)

    # Creating a buffer
    df_geo = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326")
    buff = df_geo.to_crs(crs=3857) 
    buff["buffer"] = buff.buffer(800)
    buff = buff.to_crs(crs=4326) 
    folium.GeoJson(buff["buffer"]).add_to(map_obj)

    if not df2.empty:
        for index, row in df2.iterrows():
            name= row['name']
            add = row['address']
            lat = row['Latitude']
            lon = row['Longitude']
            link =row['website']
            if isNaN(link):
                 marker = folium.CircleMarker(location=[lat, lon], tooltip=name, color='red', radius=2, weight=7, popup=name)      
            else:     
                 link2 = f'https://{link}'
                #tooltip = folium.Popup(f'<a href="{link}" target="_blank">{name}</a>', max_width=300)
                 marker = folium.CircleMarker(location=[lat, lon], tooltip=name, color='red', radius=2, weight=7, popup=f'<a href="{link2}" target="_blank">{name}</a>')        
            marker.add_to(map_obj)

    # Display the map
    map_obj.save('cafe_map.html')  # Save the map to an HTML file
    map_obj

if __name__=='__main__':
	opt=parse_opt()
	main(opt)
