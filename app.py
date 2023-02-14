import pandas as pd  
import streamlit as st  
from db_fxns import * 
from datetime import datetime
import geopandas as gpd
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import Geocoder, Fullscreen

date_format = "%Y-%m-%d"



def main():
    st.title('PRESTATION TOPOGRAPHIQUES')
    menu = ["Importer les requisitions", "Afficher les requisitions", "Modifier les requisitions", 
            "Supprimer les requisitions", "Exporter les requisitions", "Rédiger le pv de Récéption"
            ]
    
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun 
            
        return df.to_csv( sep=';',index=False).encode('latin1') 

    if choice == "Importer les requisitions":
        st.subheader("Ajouter une requisition")
        with st.expander("Importer les données Manuellement:", expanded=True):
            col1,col2 = st.columns(2)
            with col1:
                numero_sequentiel = st.number_input("Entrer le numéro séquentiel de la requisition: ")
                n_requisition = st.text_input("Enter numero de requisition ou le titre:")
                observation = st.text_area("Observation:")
                mois_d_execution = st.date_input("La date de la réalisation du projet:")
                periode_d_execution = st.text_input("L'identifiant du trimestre de la réalisation du projet:")
                x= st.number_input("Entrer la valeur de x")
                y= st.number_input("Entrer la valeur de y")
                
            with col2:
                commune =st.text_input("La commune concernée: ")
                status_projet = st.selectbox("cloturer",["OUI","NON"])
                zone_projection = st.selectbox("zone de projection",[1,2])
                date_bornage = st.date_input("Date de bornage")
                nature_de_l_affaire = st.selectbox("La nature de l'affaire: ", ['Livrée', 'Rejetée', 'En cours : Dessin et Cal', 'En cours : pas encore Levé', 'Non levé'])
                affaires = st.text_input("L'affaire: ")
                dxf_path = st.text_input("Selectionner le chemin du fichier dxf/dwg approprier")

            if st.button("Ajouter la prestation"):
                add_data(numero_sequentiel, n_requisition, date_bornage, zone_projection, x, y, nature_de_l_affaire, affaires, status_projet, observation, commune, mois_d_execution, periode_d_execution, dxf_path)
                st.success('La requisition {} a etait ajoutee'.format(n_requisition))
            
        with st.expander("Importer les données depuis un fichier Excel:"):
            file_path = st.file_uploader("Upload an Excel file", type=["xlsx"])
            if file_path:
                import_data(file_path)
                st.success("Les données sont bien importées")
    elif choice == "Afficher les requisitions":
         st.subheader("Voire une requisition")
         result = view_all_data()
         df = pd.DataFrame(result,columns=["Numéro_Séquentiel","requisition_ou_titre","date_bornage", "zone_projection","x", "y", "nature_d_affaire" ,"affaires", "cloture", "observation", "commune", "mois_dexecution", "periode_d_execution", "dxf_path"])

         with st.expander("Voir La requisition", expanded=True):
            unique_list1 = [i[0] for i in view_all_task_names()]
            view_by_requisition_name =  st.selectbox("Selectionner une requisition",unique_list1)
            filtered_df = df[(df['requisition_ou_titre'] == view_by_requisition_name)]
           
            placeholder0 = st.empty()
            with placeholder0.container():
                requisition_ou_titre = filtered_df.iloc[0]['requisition_ou_titre']
                st.markdown("Le numéro de l'affaire: "+ str(requisition_ou_titre))

                nature_d_affaire = filtered_df.iloc[0]['nature_d_affaire']
                st.markdown("La nature de l'affaire: "+ str(nature_d_affaire))

                affaires = filtered_df.iloc[0]['affaires']
                st.markdown("L'état de l'affaire: "+ str(affaires))

                cloture = filtered_df.iloc[0]['cloture']
                st.markdown("L'affaire est-il cloturer?: "+ str(cloture))

                
                observation = filtered_df.iloc[0]['observation']
                st.markdown("Observation sur l'affaire: "+ str(observation))

                commune = filtered_df.iloc[0]['commune']
                st.markdown("Le lieu de l'affaire: "+ str(commune))

                periode_d_execution = filtered_df.iloc[0]['periode_d_execution']
                mois_dexecution = filtered_df.iloc[0]['mois_dexecution']
                st.markdown("La date de la récéption de l'affaire:  mois "+str(mois_dexecution.split('-')[2])+ "|"  + str(periode_d_execution))

         with st.expander("Indices sur l'état d'avencement des travaux"):
            duration_filter = st.selectbox("Selectionner la periode des travaux: ", pd.unique(df["periode_d_execution"]))
            task_df = df[df["periode_d_execution"] == duration_filter]
            task_df = task_df.reset_index()
            
            n_affaire_total = len(task_df)

            n_affaire_cloturer = len(task_df[(task_df["cloture"]=="OUI")])
            prct_n_affaire_cloturer = n_affaire_cloturer/len(task_df["cloture"])

            n_affaire_livree = len(task_df[(task_df["affaires"]=="Livrée")])
            prct_n_affaire_livree = n_affaire_livree/len(task_df["affaires"])

            n_affaire_rejetee = len(task_df[(task_df["affaires"]=="Rejetée")])
            prct_n_affaire_rejetee = n_affaire_rejetee/len(task_df["affaires"])

            placeholder0 = st.empty()
            placeholder1 = st.empty()
            placeholder2 = st.empty()
            placeholder3 = st.empty()
           
            with placeholder0.container():
        

                kpi0,  = st.columns(1)

                                # fill in those three columns with respective metrics or KPIs
                kpi0.metric(
                    label="Nombre Total d'affaires Traitées durant ce trimestre:",
                    value=round(n_affaire_total, 2)
                            )

            with placeholder1.container():


    #         # create three columns
                kpi1, kpi2= st.columns(2)

            # fill in those three columns with respective metrics or KPIs

                kpi1.metric(
                label="Nombre d'affaires clôturer:",
                value=round(n_affaire_cloturer, 2)
                            )
            
                kpi2.metric(
                label="Pourcentage d'affaires clôturer:",
                value= round(prct_n_affaire_cloturer*100, 2)
                )


            with placeholder2.container():

    #         # create three columns
                kpi3, kpi4 = st.columns(2)

                kpi3.metric(
                label="Nombre d'affaires Livrée:",
                value=round(n_affaire_livree, 2)
                            )
            
                kpi4.metric(
                label="Pourcentage d'affaires Livrée:",
                value= round(prct_n_affaire_livree*100, 2)
                )

            with placeholder3.container():

    #         # create three columns
                kpi5, kpi6 = st.columns(2)

                kpi5.metric(
                label="Nombre d'affaires Rejetée:",
                value=round(n_affaire_rejetee, 2)
                            )
            
                kpi6.metric(
                label="Pourcentage d'affaires Rejetée:",
                value= round(prct_n_affaire_rejetee*100, 2)
                )

         with st.expander("Visualiser les données sur une carte ", expanded=True):
        
                        # Create a filter in Streamlit
            min_index = st.slider("Le premier dossier dans le marché:", 1, int(df.Numéro_Séquentiel.max()), 0)
            max_index = st.slider("Le dernier dossier dans le marché:", 1, int(df.Numéro_Séquentiel.max()), 0)

            # unique_list_0 = [i[0] for i in view_all_task_names()]
            # view_by_task_name =  st.selectbox("Selectionner une requisition à afficher:",unique_list_0)  



            filtered_df = df[(df['requisition_ou_titre'] == view_by_requisition_name) | ((df.Numéro_Séquentiel >= min_index) & (df.Numéro_Séquentiel <= max_index)) ]
                        
            # Create a geometry column from latitude and longitude
            df_na=filtered_df.dropna(subset=['x', 'y'])
       
            df_zone_1 = df_na[df_na['zone_projection'] == 1]
            df_zone_2 = df_na[df_na['zone_projection'] == 2]
            
            # Create a GeoPandas DataFrame from the Pandas DataFrame
            gdf_1 = gpd.GeoDataFrame(df_zone_1, geometry=gpd.points_from_xy(df_zone_1.x, df_zone_1.y))# type: ignore
            gdf_1.crs = 'epsg:26191'
            gdf_1 = gdf_1.to_crs('epsg:4326')

            df1 = pd.DataFrame(gdf_1)
            # df1.to_csv('zone_1.csv', index=False).encode('latin1') 
            csv1 = convert_df(df1)
          


            gdf_2 = gpd.GeoDataFrame(df_zone_2, geometry=gpd.points_from_xy(df_zone_2.x, df_zone_2.y))# type: ignore
            gdf_2.crs = 'epsg:26192'
            gdf_2 = gdf_2.to_crs( 'epsg:4326')
            

            df2 = pd.DataFrame(gdf_2)
            # df2.to_csv('zone_2.csv', index=False).encode('latin1') 
            csv2 = convert_df(df2)

                        # Create a Folium map
            # print(gdf_1)
            m = folium.Map(location=[30.9377651615862, -6.948154455820113], zoom_start=5, control_scale=True, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",attr="Google Satellite Hybrid")#type:ignore

            Fullscreen(
                position="topright",
                title="Expand me",
                title_cancel="Exit me",
                force_separate_button=True,
            ).add_to(m)

            Geocoder(collapsed=True).add_to(m)

            for index, row in gdf_1.iterrows():#type:ignore
                            popup_content = "Numéro sequentiel : " + str(row["Numéro_Séquentiel"]) + "<br>" +"La requisition: " + row["requisition_ou_titre"] + "<br>" + "Cloturée: " + row["cloture"] + "<br>" + "L'état de l'affaire: " + row["affaires"] + "<br>" + "Date de la réalisation: " +row["mois_dexecution"].split('-')[2] +'|'+ row["periode_d_execution"]
                                                
                            if row["cloture"] == "OUI":
                                color= "#00FF00"
                                
                            elif row["affaires"] == "Rejetée":  
                                color="#FF0000" 

                            elif row["affaires"] == "Livrée":
                                color="#ffff00"  
            
                            else :
                                color=  "#ffffff"
                                    
                            folium.Marker(
                                location=[row.geometry.y, row.geometry.x],
                                popup=folium.Popup(popup_content, max_width='250'),
                            icon=folium.Icon(icon_color=color),
                            ).add_to(m)

            for index, row in gdf_2.iterrows():#type:ignore
                            popup_content = "Numero sequentiel : " + str(row["Numéro_Séquentiel"]) + "<br>" +"La requisition: " + row["requisition_ou_titre"] + "<br>" + "Cloturée: " + row["cloture"] + "<br>" + "Statut de l'affaire: " + row["affaires"]  + "<br>" + "Date de la réalisation: " +row["mois_dexecution"].split('-')[2] +'|'+ row["periode_d_execution"]
                                                
                            if row["cloture"] == "OUI":
                                color= "#00FF00"
                                
                            elif row["affaires"] == "Rejetée":  
                                color="#FF0000" 

                            elif row["affaires"] == "Livrée":
                                color="#ffff00"  
            
                            else :
                                color=  "#ffffff"
                                    
                            folium.Marker(
                                location=[row.geometry.y, row.geometry.x],
                                popup=folium.Popup(popup_content, max_width='250'),
                            icon=folium.Icon(icon_color=color),
                            ).add_to(m)
                
            #m.save("index.html")

            folium_static(m)



            # Show a download button to download the CSV file
            if st.button("Télécharger Les données cartographiées"):
                st.write("Fichier CSV  exporté.")
                st.download_button(
                    label="Télécharger",
                    data=csv1+csv2,
                    file_name='bi_ouarzazate_cartographier.csv'
                )


    elif choice ==  "Modifier les requisitions":
        st.subheader("Modifier une requisition")
        with st.expander("Prestation Actuelle"):
            result = view_all_data()
            clean_df = pd.DataFrame(result,columns=["Numéro_Séquentiel","requisition_ou_titre","date_bornage", "zone_projection","x", "y", "nature_d_affaire" ,"affaires", "cloture", "observation", "commune", "mois_dexecution", "periode_d_execution", "dxf_path"])
            
        list_of_tasks = [i[0] for i in view_all_task_names()]
        selected_task = st.selectbox("Numéro de la requisition ou du titre",list_of_tasks)
        task_result = get_task(selected_task)
	
        if task_result:
            numero_sequentiel = task_result[0][0]
            n_requisition  = task_result[0][1]
            date_bornage = task_result[0][2]
            zone_projection = task_result[0][3]
            x = task_result[0][4]
            y = task_result[0][5]
            nature_de_l_affaire = task_result[0][6]
            affaires = task_result[0][7]
            status_projet  = task_result[0][8]

            observation = task_result[0][9]
            commune = task_result[0][10]

            mois_d_execution = task_result[0][11]
            mois_d_execution = datetime.strptime(mois_d_execution, date_format)

            periode_d_execution = task_result[0][12]
            # date_bornage = datetime.strptime(date_bornage, date_format)
            dxf_path = task_result[0][13]

            if x is None:
                x=0
            if y is None: 
                y=0

            col1,col2 = st.columns(2)
            
            with col1:
                new_numero_sequentiel = st.number_input("Entrer le numéro séquentiel de la requisition: ", numero_sequentiel)
                new_n_requisition = st.text_input("Enter numero de requisition ou le titre:", n_requisition)
                new_observation = st.text_area("Observation:", observation)
                
                new_mois_d_execution = st.date_input("La date de la réalisation du projet:", mois_d_execution)
                new_periode_d_execution = st.text_input("L'identifiant du trimestre de la réalisation du projet:", periode_d_execution)
                new_x= st.number_input("Entrer la valeur de x", value= x )
                new_y= st.number_input("Entrer la valeur de y", value = y)

            with col2:
                new_commune =st.text_input("La commune concernée: ", commune)
                new_status_projet = st.selectbox("cloturer",[status_projet,"OUI","NON"], index=0)
                new_zone_projection = st.selectbox("zone de projection",[zone_projection,1,2])
                new_date_bornage = st.date_input('Date de bornage: ' )
                new_nature_de_l_affaire = st.text_input("La nature de l'affaire: ", nature_de_l_affaire)
                new_affaires = st.selectbox("L'affaire: ", [affaires, 'Livrée', 'Rejetée', 'En cours : Dessin et Cal', 'En cours : pas encore Levé', 'Non levé'])
                new_dxf_path = st.text_input("Ecrire le chemin du fichier dxf/dwg approprier", dxf_path) #type:ignore
            
            if st.button("Mise a jour"):
                edit_task_data(new_numero_sequentiel, new_n_requisition,new_date_bornage,new_zone_projection,new_x,new_y,new_nature_de_l_affaire,new_affaires,new_status_projet, new_observation, new_commune, new_mois_d_execution, new_periode_d_execution, new_dxf_path, n_requisition)
                st.success("La requisition : {} a etait modifier".format(new_n_requisition))
            
            with st.expander("Voir les données modifiées"):
                result = view_all_data()
                clean_df = pd.DataFrame(result,columns=["Numéro_Séquentiel","requisition_ou_titre","date_bornage", "zone_projection","x", "y", "nature_d_affaire" ,"affaires", "cloture", "observation", "commune", "mois_dexecution", "periode_d_execution", "dxf_path"])
                selected_df = clean_df[clean_df['requisition_ou_titre'] == new_n_requisition]
                st.dataframe(selected_df)


    elif choice == "Supprimer les requisitions":
        st.subheader("Supprimer une requisition")
        
        with st.expander("Voire les données: "):
            result = view_all_data()
            clean_df = pd.DataFrame(result,columns=["Numéro_Séquentiel","requisition_ou_titre","date_bornage", "zone_projection","x", "y", "nature_d_affaire" ,"affaires", "cloture", "observation", "commune", "mois_dexecution", "periode_d_execution", "dxf_path"])
        
        unique_list = [i[0] for i in view_all_task_names()]
        delete_by_task_name =  st.selectbox("Selectionner une requisition",unique_list)
        if st.button("Supprimer"):
            delete_data(delete_by_task_name)
            st.warning("Suppression de la requisition: '{}'".format(delete_by_task_name))
        
        with st.expander("Voir les données après la Suprresion"):
            result = view_all_data()
            clean_df = pd.DataFrame(result,columns=["Numéro_Séquentiel","requisition_ou_titre","date_bornage", "zone_projection","x", "y", "nature_d_affaire" ,"affaires", "cloture", "observation", "commune", "mois_dexecution", "periode_d_execution", "dxf_path"])
            st.dataframe(clean_df)

    elif choice == "Rédiger le pv de Récéption":

        st.subheader("Rédiger le pv de Récéption: ")
        with st.form(key='pv_form'):
            EXERCICE_BUDGETAIRE_YEAR = st.date_input("EXERCICE BUDGETAIRE de l'année:") 
            EXERCICE_BUDGETAIRE_YEAR = EXERCICE_BUDGETAIRE_YEAR.year#type:ignore

            NATURE_DU_DOSSIER = st.text_input("La nature du dossier: ", "Quatrième Trimestre "+str(EXERCICE_BUDGETAIRE_YEAR))
            NUMERO_PV = st.number_input("Le numéro du pv: ")
            NUMERO_PV = int(NUMERO_PV)

            result = view_all_data()
            df_pv = pd.DataFrame(result,columns=["Numéro_Séquentiel","requisition_ou_titre","date_bornage", "zone_projection","x", "y", "nature_d_affaire" ,"affaires", "cloture", "observation", "commune", "mois_dexecution", "periode_d_execution", "dxf_path"])
            Date_du_PV = st.date_input("Selectionner le mois du pv: ")
            Date_du_PV_month = Date_du_PV.month#type:ignore
            # df_pv.index = df_pv.index + 1
            # df_pv.reset_index(inplace=True)
            # df_pv.rename(columns={'index':'Numero_Sequentiel'}, inplace=True)

            min_index = st.slider("Le premier dossier Livré dans le mois:", 1, int(df_pv.Numéro_Séquentiel.max()), 1)
            max_index = st.slider("Le dernier dossier Livré dans le mois:", 1, int(df_pv.Numéro_Séquentiel.max()), int(df_pv.Numéro_Séquentiel.max()))

            affaires_retournee_sans_levee = len(df_pv[(df_pv["affaires"]=="Non levé") ])
            
            filtered_df = df_pv[(df_pv.Numéro_Séquentiel >= min_index) & (df_pv.Numéro_Séquentiel <= max_index) & (df_pv["affaires"]=="Livrée") ]

            affaires_livree = len(filtered_df)

            filtered_df = filtered_df[['Numéro_Séquentiel', 'requisition_ou_titre', 'observation' ]]

            dict_df = filtered_df.to_dict(orient='list')

            for i, value in enumerate(dict_df['Numéro_Séquentiel']):
                dict_df['Numéro_Séquentiel'][i] = str(value)

            for i, value in enumerate(dict_df['observation']):
                dict_df['observation'][i] = ''

            # pv_df = df_pv[df_pv["periode_d_execution"] == Date_du_PV]
            # pv_df = pv_df.reset_index()

            Retard_Livree = st.text_input("Retard par rapport à la livraison: ", "Néant")

            Retard_Rejetee = st.text_input("Retard par rapport au rejet : ", "Néant")

            nbr_affaires_non_acceptes = st.text_input("Nombre d'affaires non acceptées suite au rejet: ", "Néant")

            nbr_affaires_non_Livrees = st.text_input("Nombre d'affaires non livrées après 60 jours suite au rejet: ", "Néant")

            nbr_affaires_non_recuperees = st.text_input("Nombre d'affaires non récupérées suite au rejet après 60 jours: ", "Néant")

            nbr_affaires_retournee_sans_levee = st.number_input("Nombre d'affaires retournées sans levé pour cas de forces majeures: ", affaires_retournee_sans_levee)

            #Date_du_PV = st.date_input("La date du pv: " )

            submit_bt = st.form_submit_button(label="Télécharger le Pv")

        if submit_bt:
            generate_pv(EXERCICE_BUDGETAIRE_YEAR, NATURE_DU_DOSSIER, NUMERO_PV,Date_du_PV, Date_du_PV_month, affaires_livree, Retard_Livree, Retard_Rejetee,nbr_affaires_non_acceptes,
                        nbr_affaires_non_Livrees, nbr_affaires_non_recuperees, nbr_affaires_retournee_sans_levee, dict_df   )
   
    else:
        st.subheader("Exporter les données")
        result = view_all_data()
        clean_df = pd.DataFrame(result,columns=["Numéro_Séquentiel","requisition_ou_titre","date_bornage", "zone_projection","x", "y", "nature_d_affaire" ,"affaires", "cloture", "observation", "commune", "mois_dexecution", "periode_d_execution", "dxf_path"])
        st.dataframe(clean_df)
        
        

        
        csv = convert_df(clean_df)

        # Show a download button to download the CSV file
        if st.button("Télécharger Fichier CSV"):
            st.write("Fichier CSV  exporté.")
            st.download_button(
                label="Télécharger",
                data=csv,
                file_name='bi_ouarzazate.csv'
            )
if __name__ == '__main__':
    main()
    




