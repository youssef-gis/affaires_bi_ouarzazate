import sqlite3
import pandas as pd
import pyproj 

import streamlit as st  
from geopy.distance import distance #type:ignore
import geopandas as gpd
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import Geocoder, Fullscreen
from folium.plugins import MarkerCluster
from shapely.geometry import Point
from shapely import wkt

conn = sqlite3.connect('bi_ouarzazate.db',check_same_thread=False)
c = conn.cursor()


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS prestationtable(numero_sequentiel INTEGER PRIMARY KEY AUTOINCREMENT, requisition_ou_titre TEXT,date_bornage DATE, zone_projection INTEGER, x REAL, y REAL, nature_d_affaire TEXT, affaires TEXT, cloture TEXT, observation TEXT, commune TEXT, mois_dexecution DATE, periode_d_execution TEXT, dxf_path TEXT)')

# Function to import data from Excel to SQLite table
def import_data(file_dxf_path):
	df = pd.read_excel(file_dxf_path)
	df['date_bornage'] = pd.to_datetime(df['date_bornage']).dt.strftime('%Y-%m-%d')
	df['mois_dexecution'] = pd.to_datetime(df['mois_dexecution']).dt.strftime('%Y-%m-%d')
	# print(df.head())
	df.to_sql('prestationtable', conn, if_exists='append', index=False)


def add_data(numero_sequentiel,n_requisition,date_bornage,zone_projection,x,y, nature_d_affaire, affaires, cloture, observation, commune, mois_dexecution, periode_d_execution, dxf_path ):
	c.execute('INSERT INTO prestationtable(numero_sequentiel, requisition_ou_titre, date_bornage, zone_projection, x, y, nature_d_affaire, affaires, cloture, observation, commune, mois_dexecution, periode_d_execution, dxf_path) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(numero_sequentiel,n_requisition,date_bornage,zone_projection,x,y, nature_d_affaire, affaires, cloture, observation, commune, mois_dexecution, periode_d_execution, dxf_path ))
	conn.commit()

def view_all_data():
	c.execute('SELECT * FROM prestationtable')
	data = c.fetchall()
	return data

def view_all_task_names():
	c.execute('SELECT DISTINCT requisition_ou_titre FROM prestationtable')
	data = c.fetchall()
	return data

def get_task(n_requisition):
	c.execute('SELECT * FROM prestationtable WHERE requisition_ou_titre="{}"'.format(n_requisition))
	data = c.fetchall()
	return data

def edit_task_data(new_numero_sequentiel,new_n_requisition,new_date_bornage,new_zone_projection,new_x,new_y,new_nature_de_l_affaire,new_affaires, new_status_projet, new_observation, new_commune, new_mois_d_execution, new_periode_d_execution,new_dxf_path, n_requisition):
	c.execute("UPDATE prestationtable SET numero_sequentiel=?,requisition_ou_titre =?,date_bornage=?,zone_projection=?,x=?,y=?,nature_d_affaire=?,affaires=?,cloture=?,observation=?,commune=?,mois_dexecution=?, periode_d_execution=?, dxf_path=? WHERE requisition_ou_titre =? ",(new_numero_sequentiel,new_n_requisition,new_date_bornage,new_zone_projection,new_x,new_y,new_nature_de_l_affaire,new_affaires, new_status_projet, new_observation, new_commune, new_mois_d_execution, new_periode_d_execution, new_dxf_path, n_requisition))
	conn.commit()
	data = c.fetchall()
	
	return data

def delete_data(requisition_ou_titre):
	c.execute('DELETE FROM prestationtable WHERE requisition_ou_titre="{}"'.format(requisition_ou_titre))
	conn.commit()


def find_closest_points(point, gdf, num_points=3):
    
	# Define the target CRS for the projection
    # target_crs = 'EPSG:26191'  # UTM zone 32N
    # point = Point(point)
    # gdf['geometry'] = gdf['geometry'].apply(wkt.loads)
    
# Create a Transformer object for the coordinate transformation
    # transformer = pyproj.Transformer.from_crs(gdf.crs, target_crs, always_xy=True)
    
    # Project the reference point to the target CRS
    # ref_point_proj = Point(transformer.transform(point.x, point.y))
    
    # Project the geometry column to the target CRS
    # gdf_proj = gdf.to_crs(target_crs)
    
    # Calculate the distance between the reference point and each point in the geopandas dataframe
	
    gdf['distance'] = gdf.geometry.apply(lambda  x: point.distance(x))
    # gdf_proj = gdf.to_crs('EPSG:4326')
    # sort the dataframe by distance and select the closest points
    closest_points = gdf.sort_values(by='distance').head(num_points)
    # print(closest_points)

    return closest_points
