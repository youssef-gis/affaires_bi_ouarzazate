import sqlite3
import pandas as pd
import subprocess
import streamlit as st  



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


def launch_app(df):
	subprocess.Popen(["C:/Program Files/QGIS 3.22.3/bin/qgis-bin"])


