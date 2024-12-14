import os
import requests
import gc  # garbage collection
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import pandas as pd
from streamlit_folium import st_folium


# Load the data (with caching to improve performance)
@st.cache_data
def load_patients_by_region_data(year):
    file_path = f'../data/patients_by_region_pathology_{year}.csv'
    return pd.read_csv(file_path)

@st.cache_data
def load_patients_by_department_data(year):
    file_path = f'../data/patients_by_department_pathology_{year}.csv'
    return pd.read_csv(file_path)

@st.cache_data
def load_patients_by_gender_data(year):
    file_path = f'../data/patients_by_sexe_pathology_{year}.csv'
    return pd.read_csv(file_path)

@st.cache_data
def load_patients_by_age_group_data(year):
    file_path = f'../data/patients_by_age_group_pathology_{year}.csv'
    return pd.read_csv(file_path)

@st.cache_data
def load_staged_data(year):
    file_path = f'../data/staged_data_{year}.csv'
    return pd.read_csv(file_path)

@st.cache_data
def load_and_cache_data(year):
    staged_data_year = load_staged_data(year)
    staged_data_year = staged_data_year.loc[
        (staged_data_year["Department Name"] != "Hors France Métropolitaine") &
        (staged_data_year["Gender Label"] != "tous sexes") &
        (staged_data_year["Age Group Label"] != "tous âges") &
        (staged_data_year["Department"] != 999) &
        (staged_data_year["Region"] != 99)
    ].copy()
    staged_data_year["Year"] = year
    return staged_data_year

# Define the list of years from 2015 to 2022
years = list(range(2015, 2023))

###############################################################################################

# Sidebar: Create dropdown buttons
with st.sidebar:

    st.title("Menu de Navigation")  

    # Create expanders for navigation
    page = None  
    with st.expander("🏠 Accueil"):
        if st.button("Aller à Accueil", key="accueil_button"):
            st.session_state.page = "Accueil"

    with st.expander("🗺️ Analyse par région"):
        if st.button("Voir la Carte", key="region_button"):
            st.session_state.page = "Région"

    with st.expander("🗺️ Analyse par département"):
        if st.button("Voir la Carte", key="departement_button"):
            st.session_state.page = "Département"

    with st.expander("📊 Analyse par âge"):
        if st.button("Voir les diagrammes", key="age_button"):
            st.session_state.page = "Age"

    with st.expander("📊 Analyse par sexe"):
        if st.button("Voir les diagrammes", key="sexe_button"):
            st.session_state.page = "Sexe"

st.markdown("""
    <style>

    [data-testid="stSidebar"] {
        background-color: #00008B; 
    }

    
    [data-testid="stSidebar"] h1 {
        color: white; 
        font-size: 22px; 
        font-weight: bold;
    }

    [data-testid="stSidebar"] .stExpander > div > div:first-child {
        font-size: 16px; 
        color: white; 
        font-weight: bold; 
    }

    [data-testid="stSidebar"] .stButton button {
        color: white; 
        font-weight: 300; 
        background-color: #1b1bf7;
        border: 1px solid white; 
        border-radius: 15px; 
        font-size: 16px; 
        padding: 6px 12px; 
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #0059b3; 
        color: #ffffff; 
    }

    [data-testid="stSidebar"] .stExpander {
        border: 0.7px solid white; 
        border-radius: 10px; 
        margin-bottom: 10px; 
    }

    [data-testid="stSidebar"] .stExpander div {
        color: white; 
        font-size: 16px; 
        font-weight: 300; 
    }
    </style>
""", unsafe_allow_html=True)


###############################################################################################

# Main Content: Display content based on the selected page
# Check and initialize the value for st.session_state.page
if "page" not in st.session_state:
    st.session_state.page = "Accueil"  

# Main Content: Display content based on the selected page
if st.session_state.page == "Accueil" or "page" not in locals():

    logo_path = os.path.abspath("static/logo.jpeg")

    col1, col2, col3 = st.columns([3, 3, 2])  

    with col2:  
        st.image(logo_path, use_container_width =False, width=150)

    # Page title
    st.markdown("""
        <h1 style="color: #00008B; text-align: center; font-size: 34px;">
            Bienvenue sur DataViz Santé Publique
        </h1>
    """, unsafe_allow_html=True)

    # Simplified main content
    st.markdown("""
        <style>
            .highlight {
                color: #1b1bf7; 
                font-weight: bold;
            }
            .section-title {
                color: #007bff; 
                font-size: 20px; 
                font-weight: bold; 
                margin-top: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        ### Votre outil d'analyse et de visualisation des données de santé publique.
        Notre plateforme offre une exploration détaillée des 
        <span class="highlight">données actualisées de 2015 à 2022</span>, fournies par l’Assurance Maladie, couvrant un large éventail de pathologies, 
        traitements chroniques et épisodes de soins. Conçue pour répondre aux besoins des 
        <span class="highlight">mutuelles, professionnels de santé</span> et acteurs engagés dans la gestion des soins et dépenses de santé, 
        elle vous aide à prendre des décisions éclairées.
    """, unsafe_allow_html=True)

    st.markdown("""
        ### Pourquoi choisir notre plateforme ?
        - Analyse par **pathologie, traitement chronique** ou **épisode de soins**, déclinée par sexe, classe d’âge, région et département.
        - Suivi des **prévalences (%)** et des **dépenses remboursées** pour une meilleure compréhension des dynamiques de santé.
        - Comparaisons temporelles (**2015-2022**) pour identifier les tendances clés par région ou département.
    """)

    st.markdown("""
        ### Applications concrètes pour les acteurs de la santé :
        - **Pour les mutuelles :** Ajustez vos offres en fonction des pathologies et besoins locaux.
        - **Pour les professionnels de santé :** Identifiez les besoins prioritaires pour planifier les soins et répartir les ressources.
        - **Pour les décideurs publics :** Suivez l’évolution des dépenses et pathologies émergentes pour adapter les politiques publiques.
    """)

    st.markdown("""
        ### Caractéristiques de la population analysée :
        Les données couvrent **68,7 millions de bénéficiaires** de l’assurance maladie obligatoire en 2022, incluant :
        - Les individus ayant bénéficié d’au moins une prestation remboursée (médecine, pharmacie, biologie, etc.).
        - Ceux ayant été hospitalisés dans un établissement public ou privé.
        
        **Note :** Par respect pour le secret statistique, aucune donnée n’est communiquée lorsque le nombre de patients pris en charge est inférieur à 11. 
        Ces cas sont indiqués comme **« Non significatif »**.
    """)

    st.markdown("""
        ### Explorez dès maintenant !
        **DataViz Santé Publique**, c’est une vision claire pour une meilleure santé. Utilisez nos outils interactifs pour analyser les dynamiques de santé à travers la France. 🌍
    """, unsafe_allow_html=True)

    # Create a copyright footer
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: #333;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            font-family: Arial, sans-serif;
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        }
        </style>
        <div class="footer">
            © 2024 DataViz Santé Publique. Tous droits réservés. | 
            <a href="https://www.example.com" style="text-decoration: none; color: #007bff;">Politique de confidentialité</a> | 
            <a href="https://www.example.com" style="text-decoration: none; color: #007bff;">Conditions d'utilisation</a>
        </div>
    """, unsafe_allow_html=True)


###############################################################################################

elif st.session_state.page == "Région":
    st.markdown("""
        <h1 style="color: #00008B; text-align: center; font-size: 30px;">
            Analyse des pathologies par région
        </h1>
    """, unsafe_allow_html=True)

   # Select a year from 2015 to 2022 with the default value set to 2022
    selected_year = st.selectbox(
        "Choisir l'année:", 
        list(range(2015, 2023)), 
        index=len(range(2015, 2023)) - 1,  # Set the default to the last year in the list (2022)
        key="year_select"  
    )

    df = load_patients_by_region_data(selected_year)

    # Combine CSS to adjust the font style, thickness of the selection bars, and the content inside the select box.
    st.markdown("""
        <style>
    
        div[role="combobox"] > div {
            font-size: 12px;  
            font-weight: 300;  
        }
        div[role="combobox"] > div > div {
            font-size: 12px;  
        }

        
        div[data-baseweb="select"] {
            height: 35px;  
            border-radius: 5px;  
            background-color: #add8e6;  
            color: black;  
        }

        
        div[data-baseweb="select"] > div {
            font-size: 14px;  
        }

        
        div[data-baseweb="select"] .css-1nfy0zz {
            font-size: 14px;  
        }

        
        div[data-baseweb="select"] .css-1nfy0zz:hover {
            background-color: #87cefa; 
        }
        </style>
    """, unsafe_allow_html=True)

    pathology_level_1_list = df['Pathology Level 1'].unique()

    # Create a selection button for Pathology Level 1 with the default value set to "Diabetes" if available
    default_index_level_1 = list(pathology_level_1_list).index("Cancers") if "Cancers" in pathology_level_1_list else 0
    selected_pathology_level_1 = st.selectbox(
        "Choisir la pathologie du niveau 1",
        pathology_level_1_list,
        index=default_index_level_1,
        key="pathology_level_1_select"
    )

    filtered_df_level_1 = df[df['Pathology Level 1'] == selected_pathology_level_1]

    pathology_level_2_list = filtered_df_level_1['Pathology Level 2'].unique().tolist()

    selected_pathology_level_2 = st.selectbox(
        "Choisir la pathologie du niveau 2 (Sous-groupe de pathologies)",
        pathology_level_2_list,
        index=len(pathology_level_2_list) - 1,  
        key="pathology_level_2_select"
    )
    filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1['Pathology Level 2'] == selected_pathology_level_2]


    pathology_level_3_list = filtered_df_level_2['Pathology Level 3'].unique().tolist()

    selected_pathology_level_3 = st.selectbox(
        "Choisir la pathologie du niveau 3 (Sous-groupe détaillé de pathologies)",
        pathology_level_3_list,
        index=len(pathology_level_3_list) - 1,  
        key="pathology_level_3_select"
    )

    filtered_df = filtered_df_level_2.loc[
        (filtered_df_level_2['Pathology Level 3'] == selected_pathology_level_3) & 
        (filtered_df_level_2['Region'] != 99)
    ].copy()  

    # The columns to display and verify
    columns_to_display = ["Region Name", "Patient Count (top)"]

    if all(col in filtered_df.columns for col in columns_to_display):
        filtered_df_display = filtered_df[columns_to_display].sort_values(
            by="Patient Count (top)", ascending=True
        )

        # Create a horizontal bar chart
        fig = px.bar(
            filtered_df_display,
            y="Region Name",  
            x="Patient Count (top)",  
            orientation="h",  
            text="Patient Count (top)",  
        )

        fig.update_traces(
            texttemplate="%{text:,}".replace(",", " "),  
            textposition="outside",  
            marker_color="#1b1bf7",  
            marker_line_width=0,  
            width=0.4,  
        )


        fig.update_layout(
            template="none",  
            paper_bgcolor="rgba(0,0,0,0)",  
            plot_bgcolor="rgba(0,0,0,0)",  
            margin=dict(t=20, l=200, r=20, b=20),  
            height=450,  
            xaxis=dict(
                title=None,  
                showgrid=False,  
                zeroline=False,  
                showticklabels=False,  
            ),
            yaxis=dict(
                title=None,  
                tickfont=dict(size=12),  
                showline=False,  
                automargin=True,  
            ),
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Clean up temporary data
        del filtered_df_display
        gc.collect()
    else:
        st.error(f"One or more columns from {columns_to_display} are missing in the filtered data.")

    columns_to_display = ["Region Name", "Patient Count (top)"]
    if all(col in filtered_df.columns for col in columns_to_display):

        data = filtered_df[columns_to_display]


        data["Region Name"] = data["Region Name"].fillna("Non renseigné")


        max_region = data.loc[data["Patient Count (top)"].idxmax()]
        min_region = data.loc[data["Patient Count (top)"].idxmin()]
        avg_patient_count = round(data["Patient Count (top)"].mean())
        median_patient_count = round(data["Patient Count (top)"].median())


        max_patient_count = f"{int(max_region['Patient Count (top)']):,}".replace(",", " ")
        min_patient_count = f"{int(min_region['Patient Count (top)']):,}".replace(",", " ")
        avg_patient_count_display = f"{avg_patient_count:,}".replace(",", " ")
        median_patient_count_display = f"{median_patient_count:,}".replace(",", " ")


        del data
        gc.collect()

        # Display buttons with statistical information
        st.markdown(f"""
        <style>
        .stat-box {{
            display: flex;
            justify-content: space-between;
            align-items: stretch; 
            margin-top: 20px;
        }}
        .stat-item {{
            text-align: center;
            background-color: #ffcc00;
            padding: 15px; 
            border-radius: 10px;
            flex: 1;
            margin: 0 10px;
            color: white;
            font-family: Arial, sans-serif;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            min-height: 150px; 
            max-height: 150px; 
        }}
        .stat-item span {{
            font-size: 16px;  
            font-weight: 400; 
        }}
        .stat-item small {{
            font-size: 12px;  
            font-weight: 300; 
            margin-top: 8px; 
        }}
        .stat-item .number {{
            font-size: 24px; 
            font-weight: 600; 
            margin-top: 5px; 
        }}
        .red {{background-color: #ff5733;}}
        .green {{background-color: #28a745;}}
        .blue {{background-color: #007bff;}}
        .orange {{background-color: #ffcc00;}}
        </style>
        <div class="stat-box">
            <div class="stat-item red">
                <span>{max_region['Region Name']}</span>
                <span class="number">{max_patient_count}</span>
                <small>Région avec le plus de patients</small>
            </div>
            <div class="stat-item green">
                <span>{min_region['Region Name']}</span>
                <span class="number">{min_patient_count}</span>
                <small>Région avec le moins de patients</small>
            </div>
            <div class="stat-item blue">
                <span class="number">{avg_patient_count_display}</span>
                <small>Moyenne des patients par région</small>
            </div>
            <div class="stat-item orange">
                <span class="number">{median_patient_count_display}</span>
                <small>Médiane des patients par région</small>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Insert a blank line between the statistics block and the map
    st.markdown("<br>", unsafe_allow_html=True)

    # Check if the filtered data contains the necessary columns
    required_columns = ["Region Name", "Patient Count (top)"]

    if all(column in filtered_df.columns for column in required_columns):

        map_data = filtered_df[["Region Name", "Patient Count (top)"]].copy()
        map_data = map_data.dropna(subset=["Patient Count (top)"])  

        if map_data.empty:
            st.error("No valid data available after cleaning.")
        else:
            # The path to the GeoJSON file containing the border information of the regions
            geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson"

            import requests
            response = requests.get(geojson_url)
            if response.status_code != 200:
                st.error("Failed to load GeoJSON data.")
            else:
                geojson_data = response.json()

                # Add data to GeoJSON (mapping Region Name -> Patient Count)
                for feature in geojson_data["features"]:
                    region_name = feature["properties"]["nom"]  
                    if region_name in map_data["Region Name"].values:
                        # Get the unique values corresponding to Region Name
                        patient_count = map_data.loc[
                            map_data["Region Name"] == region_name, "Patient Count (top)"
                        ].iloc[0]
                        feature["properties"]["Patient Count (top)"] = int(patient_count)
                    else:
                        feature["properties"]["Patient Count (top)"] = "No Data"

                # Initialize the map centered on France
                m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

                # Map the data into the GeoJSON
                folium.Choropleth(
                    geo_data=geojson_data,
                    name="choropleth",
                    data=map_data,
                    columns=["Region Name", "Patient Count (top)"],  
                    key_on="feature.properties.nom",  
                    fill_color="YlOrRd",  
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    nan_fill_color="#e1ebf5",  
                    legend_name="Patient Count (top)",
                ).add_to(m)

                # Add a tooltip to display information when hovering over the map
                folium.GeoJson(
                    geojson_data,
                    style_function=lambda x: {
                        "fillColor": "YlOrRd",
                        "color": "black",
                        "weight": 0.2,
                        "dashArray": "5, 5",
                    },
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=["nom", "Patient Count (top)"],  
                        aliases=["Region: ", "Patients: "],  
                        style="font-size:12px;",  
                        localize=True,
                    ),
                ).add_to(m)


                st_folium(m, width=800, height=600)


                del geojson_data, m, map_data
                gc.collect()
    else:
        st.error("Les colonnes 'Region Name' et 'Patient Count (top)' sont manquantes dans les données.")

    # Combine the data across years but filter only by the selected Pathology Levels
    all_years_data = []

    # Iterate through each year
    for year in years:
    
        df_year = load_patients_by_region_data(year).copy()  


        filtered_df_level_1 = df_year[df_year['Pathology Level 1'] == selected_pathology_level_1]

    
        filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1['Pathology Level 2'] == selected_pathology_level_2]

        filtered_df = filtered_df_level_2.loc[
            (filtered_df_level_2['Pathology Level 3'] == selected_pathology_level_3) &
            (filtered_df_level_2['Region'] != 99)
        ].copy()  

        
        filtered_df["Year"] = year

        
        all_years_data.append(filtered_df)


        del df_year, filtered_df_level_1, filtered_df_level_2, filtered_df
        gc.collect() 

    # Combine all the data across the years
    combined_data = pd.concat(all_years_data, ignore_index=True)

    # Delete the intermediate data list
    del all_years_data
    gc.collect()  


    region_year_data = combined_data.groupby(["Region Name", "Year"])["Patient Count (top)"].sum().reset_index()


    del combined_data
    gc.collect()  


    fig = px.line(
        region_year_data,
        x="Year",
        y="Patient Count (top)",
        color="Region Name",  
        labels={"Patient Count (top)": "Nombre de patients", "Year": "Année"},
        title=f"Évolution du nombre de patients pour {selected_pathology_level_1}, {selected_pathology_level_2}, {selected_pathology_level_3}"
    )


    fig.update_layout(
        template="simple_white",
        title_x=0.5,  
        legend_title_text="Région",
        xaxis=dict(title="Année"),
        yaxis=dict(title="Nombre de patients"),
        margin=dict(l=50, r=50, t=50, b=50),  
        height=500  
    )

    # Display the suggestion right before the chart
    st.markdown("""
    <p style="font-size: 14px; font-style: italic; color: gray;">
    Astuce : Cliquez sur les noms des régions dans la légende pour les masquer/afficher.
    </p>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig, use_container_width=True)


    regions_list = region_year_data["Region Name"].unique().tolist()

   
    regions_list.sort()

    # Dropdown to select a region
    selected_region = st.selectbox(
        "Choisir une région :", 
        options=regions_list, 
        index=0
    )

    region_data = region_year_data[region_year_data["Region Name"] == selected_region]

    # Delete intermediate data after filtering
    del region_year_data
    gc.collect()

    # Create a chart with data displayed for each year
    fig = px.line(
        region_data,
        x="Year",
        y="Patient Count (top)",
        labels={"Patient Count (top)": "Nombre de patients", "Year": "Année"},
        title=f"Évolution du nombre de patients pour la région {selected_region}"
    )


    fig.update_traces(
        mode="lines+markers+text",  
        text=region_data["Patient Count (top)"],  
        textposition="top center",  
        line_color="#1b1bf7"  
    )


    fig.update_layout(
        template="none",  
        height=500,  
        title={
            "text": f"Évolution du nombre de patients pour la région {selected_region}",
            "x": 0.5,  
            "xanchor": "center"
        },
        xaxis=dict(
            title="Année",  
            showgrid=False  
        ),
        yaxis=dict(
            title="Nombre de patients",  
            showgrid=True  
        )
    )


    st.markdown("""
    <p style="font-size: 14px; font-style: italic; color: gray;">
    Astuce : Si vous souhaitez zoomer sur l'évolution d'une seule région, veuillez sélectionner la région dans la liste déroulante ci-dessous.
    </p>
    """, unsafe_allow_html=True)


    st.plotly_chart(fig, use_container_width=True)


    del region_data
    gc.collect()


###############################################################################################

# Main Content: Display content based on the selected page
if st.session_state.page == "Département":
    st.markdown("""
        <h1 style="color: #00008B; text-align: center; font-size: 30px;">
            Analyse des données par département !
        </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
        <p style="text-align: center; font-style: italic; font-weight: 300; font-size: 16px;">
            Utilisez les options ci-dessous pour analyser les données.
        </p>
    """, unsafe_allow_html=True)


    selected_year = st.selectbox(
        "Choisir l'année:", 
        list(range(2015, 2023)), 
        index=len(range(2015, 2023)) - 1,  
        key="year_select_departement"  
    )


    df = load_patients_by_department_data(selected_year)

    df = df[df["Department Name"] != "Hors France Métropolitaine"].copy()


    pathology_level_1_list = df['Pathology Level 1'].unique()


    default_index_level_1 = list(pathology_level_1_list).index("Cancers") if "Cancers" in pathology_level_1_list else 0
    selected_pathology_level_1 = st.selectbox(
        "Choisir la pathologie du niveau 1",
        pathology_level_1_list,
        index=default_index_level_1,
        key="pathology_level_1_select_departement"
    )

    filtered_df_level_1 = df[df['Pathology Level 1'] == selected_pathology_level_1]


    pathology_level_2_list = filtered_df_level_1['Pathology Level 2'].unique().tolist()


    selected_pathology_level_2 = st.selectbox(
        "Choisir la pathologie du niveau 2 (Sous-groupe de pathologies)",
        pathology_level_2_list,
        index=len(pathology_level_2_list) - 1,  
        key="pathology_level_2_select_departement"
    )
    filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1['Pathology Level 2'] == selected_pathology_level_2]


    pathology_level_3_list = filtered_df_level_2['Pathology Level 3'].unique().tolist()


    selected_pathology_level_3 = st.selectbox(
        "Choisir la pathologie du niveau 3 (Sous-groupe détaillé de pathologies)",
        pathology_level_3_list,
        index=len(pathology_level_3_list) - 1,  
        key="pathology_level_3_select_departement"
    )

    filtered_df = filtered_df_level_2.loc[
        (filtered_df_level_2['Pathology Level 3'] == selected_pathology_level_3) & 
        (filtered_df_level_2['Department'] != 99)
    ].copy()  
    

    staged_data_year = load_staged_data(selected_year)

    filtered_staged_data = staged_data_year.loc[
        (staged_data_year['Year'] == selected_year) &
        (staged_data_year['Pathology Level 1'] == selected_pathology_level_1) &
        (staged_data_year['Pathology Level 2'] == selected_pathology_level_2) &
        (staged_data_year['Pathology Level 3'] == selected_pathology_level_3) &
        (staged_data_year["Gender Label"] != "tous sexes") &
        (staged_data_year["Age Group Label"] != "tous âges") &
        (staged_data_year["Department"] != 999) &
        (staged_data_year["Region"] != 99)
    ].copy()

 
    columns_to_display = ["Department Name", "Age Group Label", "Patient Count (top)", "Total Population", "Prevalence"]

    if all(col in filtered_staged_data.columns for col in columns_to_display):
 
        filtered_df_display = (
            filtered_staged_data.loc[
                (filtered_staged_data["Department Name"] != "Hors France Métropolitaine") &  
                (filtered_staged_data["Patient Count (top)"].notna())  
            ][columns_to_display]
            .drop_duplicates()  
            .sort_values(by=["Department Name", "Patient Count (top)"], ascending=[True, False])  
        )


        st.dataframe(filtered_df_display, use_container_width=True)

  
        del filtered_df_display 
        gc.collect()
    else:
        st.error(f"One or more columns from {columns_to_display} are missing in the filtered data.")


    columns_to_display = ["Department Name", "Patient Count (top)"]
    if all(col in filtered_df.columns for col in columns_to_display):

        data = filtered_df[columns_to_display]


        data.loc[:, "Department Name"] = data["Department Name"].fillna("Non renseigné")


        max_department = data.loc[data["Patient Count (top)"].idxmax()]
        min_department = data.loc[data["Patient Count (top)"].idxmin()]
        avg_patient_count = round(data["Patient Count (top)"].mean())
        median_patient_count = round(data["Patient Count (top)"].median())


        max_patient_count = f"{int(max_department['Patient Count (top)']):,}".replace(",", " ")
        min_patient_count = f"{int(min_department['Patient Count (top)']):,}".replace(",", " ")
        avg_patient_count_display = f"{avg_patient_count:,}".replace(",", " ")
        median_patient_count_display = f"{median_patient_count:,}".replace(",", " ")

        
        st.markdown(f"""
            <style>
            .stat-box {{
                display: flex;
                justify-content: space-between;
                align-items: stretch; 
                margin-top: 20px;
            }}
            .stat-item {{
                text-align: center;
                background-color: #ffcc00;
                padding: 15px; 
                border-radius: 10px;
                flex: 1;
                margin: 0 10px;
                color: white;
                font-family: Arial, sans-serif;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column; 
                justify-content: center; 
                align-items: center; 
                min-height: 150px; 
                max-height: 150px; 
            }}
            .stat-item span {{
                font-size: 16px;  
                font-weight: bold; 
            }}
            .stat-item small {{
                font-size: 12px;  
                font-weight: 300; 
                margin-top: 10px;
            }}
            .stat-item .number {{
                font-size: 24px; 
                font-weight: 600; 
                margin-top: 5px; 
            }}
            .red {{background-color: #ff5733;}}
            .green {{background-color: #28a745;}}
            .blue {{background-color: #007bff;}}
            .orange {{background-color: #ffcc00;}}
            </style>
            <div class="stat-box">
                <div class="stat-item red">
                    <span>{max_department['Department Name']}</span>
                    <span>{max_patient_count}</span>
                    <small>Département avec le plus de patients</small>
                </div>
                <div class="stat-item green">
                    <span>{min_department['Department Name']}</span>
                    <span>{min_patient_count}</span>
                    <small>Département avec le moins de patients</small>
                </div>
                <div class="stat-item blue">
                    <span>{avg_patient_count_display}</span>
                    <small>Moyenne des patients par département</small>
                </div>
                <div class="stat-item orange">
                    <span>{median_patient_count_display}</span>
                    <small>Médiane des patients par département</small>
                </div>
            </div>
        """, unsafe_allow_html=True)

        
        del data
        gc.collect()
    else:
        st.error(f"One or more columns from {columns_to_display} are missing in the filtered data.")
    
  
    st.markdown("<br>", unsafe_allow_html=True)

 
    if all(column in filtered_df.columns for column in columns_to_display):

        map_data = filtered_df[["Department Name", "Patient Count (top)"]].copy()
        map_data = map_data.dropna(subset=["Patient Count (top)"])  

        if map_data.empty:
            st.error("No valid data available after cleaning.")
        else:
            # The path to the GeoJSON file containing the border information of the regions
            geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"

        
            import requests
            response = requests.get(geojson_url)
            if response.status_code != 200:
                st.error("Failed to load GeoJSON data.")
            else:
                geojson_data = response.json()

               
                for feature in geojson_data["features"]:
                    department_name = feature["properties"]["nom"]  
                    if department_name in map_data["Department Name"].values:
                   
                        patient_count = map_data.loc[
                            map_data["Department Name"] == department_name, "Patient Count (top)"
                        ].iloc[0]
                        feature["properties"]["Patient Count (top)"] = int(patient_count)
                    else:
                        feature["properties"]["Patient Count (top)"] = None

            
                min_value = map_data["Patient Count (top)"].min()
                max_value = map_data["Patient Count (top)"].max()

      
                m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

   
                folium.Choropleth(
                    geo_data=geojson_data,
                    name="choropleth",
                    data=map_data,
                    columns=["Department Name", "Patient Count (top)"],  
                    key_on="feature.properties.nom",  
                    fill_color="YlOrRd",  
                    fill_opacity=0.7,
                    line_opacity=0,
                    nan_fill_color="#e1ebf5",  
                    legend_name="Patient Count (top)",
                    threshold_scale=[
                        min_value,
                        min_value + (max_value - min_value) * 0.25,
                        min_value + (max_value - min_value) * 0.5,
                        min_value + (max_value - min_value) * 0.75,
                        max_value,
                    ],
                ).add_to(m)

         
                folium.GeoJson(
                    geojson_data,
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=["nom", "Patient Count (top)"],  
                        aliases=["Department: ", "Patients: "], 
                        style="font-size:12px;", 
                        localize=True,
                    ),
                    
                ).add_to(m)

            
                st_folium(m, width=800, height=600)

          
                del geojson_data, m, map_data
                gc.collect()

    else:
        st.error("Les colonnes 'Department Name' et 'Patient Count (top)' sont manquantes dans les données.")


    all_years_data = []


    for year in years:

        df_year = load_patients_by_department_data(year).copy()  

     
        df_year = df_year[df_year["Department Name"] != "Hors France Métropolitaine"]


        filtered_df_level_1 = df_year[df_year['Pathology Level 1'] == selected_pathology_level_1]


        filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1['Pathology Level 2'] == selected_pathology_level_2]

     
        filtered_df = filtered_df_level_2.loc[
            (filtered_df_level_2['Pathology Level 3'] == selected_pathology_level_3) &
            (filtered_df_level_2['Department'] != 999)
        ].copy()

   
        filtered_df["Year"] = year

   
        all_years_data.append(filtered_df)

   
        del df_year, filtered_df_level_1, filtered_df_level_2, filtered_df
        gc.collect()

   
    combined_data = pd.concat(all_years_data, ignore_index=True)

  
    department_year_data = combined_data.groupby(["Department Name", "Year"])["Patient Count (top)"].sum().reset_index()

 
    del all_years_data, combined_data
    gc.collect()


    departments_list = department_year_data["Department Name"].unique().tolist()
    departments_list.sort()  
    selected_department = st.selectbox(
        "Choisir un département :", 
        options=departments_list, 
        index=0
    )

   
    department_data = department_year_data[department_year_data["Department Name"] == selected_department]

  
    fig = px.line(
        department_data,
        x="Year",
        y="Patient Count (top)",
        labels={"Patient Count (top)": "Nombre de patients", "Year": "Année"},
        title=f"Évolution du nombre de patients pour le département {selected_department}"
    )

  
    fig.update_traces(
        mode="lines+markers+text",  
        text=department_data["Patient Count (top)"],  
        textposition="top center",  
        line_color="#1b1bf7"  
    )


    fig.update_layout(
        template="none",  
        height=500,  
        title={
            "text": f"Évolution du nombre de patients pour le département {selected_department}",
            "x": 0.5,  
            "xanchor": "center"
        },
        xaxis=dict(
            title="Année",  
            showgrid=False  
        ),
        yaxis=dict(
            title="Nombre de patients",  
            showgrid=True  
        )
    )


    st.markdown("""
    <p style="font-size: 14px; font-style: italic; color: gray;">
    Astuce : Si vous souhaitez zoomer sur l'évolution d'un seul département, veuillez sélectionner le département dans la liste déroulante ci-dessus.
    </p>
    """, unsafe_allow_html=True)


    st.plotly_chart(fig, use_container_width=True)


    del department_year_data, department_data
    gc.collect()


    columns_to_display = ["Department Name", "Age Group Label", "Patient Count (top)"]

    if all(col in filtered_staged_data.columns for col in columns_to_display):
    
        filtered_df_display = (
            filtered_staged_data.loc[
                (filtered_staged_data["Department Name"] != "Hors France Métropolitaine") &  
                (filtered_staged_data["Patient Count (top)"].notna())  
            ][columns_to_display]
            .drop_duplicates()  
            .sort_values(by=["Department Name", "Patient Count (top)"], ascending=[True, False]) 
        )

      
        filtered_age_data = filtered_df_display.loc[
            filtered_df_display["Age Group Label"] != "tous âges"
        ].copy()

    
        filtered_age_data_department = filtered_age_data.loc[
            filtered_age_data["Department Name"] == selected_department
        ]

     
        age_class_distribution = (
            filtered_age_data_department.groupby("Age Group Label")["Patient Count (top)"]
            .sum()
            .reset_index()
        )

     
        if not age_class_distribution.empty:
           
            total_patients = age_class_distribution["Patient Count (top)"].sum()

        
            age_class_distribution["Percentage"] = (
                age_class_distribution["Patient Count (top)"] / total_patients * 100
            )

  
            filtered_age_class_distribution = age_class_distribution[
                age_class_distribution["Percentage"] >= 0.1
            ]

        
            if not filtered_age_class_distribution.empty:
                fig_pie = px.pie(
                    filtered_age_class_distribution,
                    names="Age Group Label", 
                    values="Patient Count (top)",  
                    title=f"<b>Répartition des classes d'âge pour la pathologie sélectionnée </b>",
                    hole=0.4,  
                )

                fig_pie.update_traces(
                    textinfo="percent",  
                    hoverinfo="label+percent+value",  
                    textfont_size=14,  
                )

           
                fig_pie.update_layout(
                    title=dict(
                        text=f"<b>Répartition des classes d'âge pour la pathologie sélectionnée </b>",
                        x=0.1, 
                        font=dict(size=18),  
                    ),
                    showlegend=True,  
                    legend=dict(
                        title="Classe d'âge",  
                        orientation="v",  
                        x=1.05,  
                        y=0.5,  
                        font=dict(size=12), 
                    ),
                    margin=dict(t=70, l=50, r=120, b=50),  
                    height=500, 
                    width=750,  
                )

             
                st.markdown("""
                <p style="font-size: 14px; font-style: italic; color: gray; text-align: center;">
                Astuce : Survolez les parties du graphique pour voir plus de détails interactifs.
                </p>
                """, unsafe_allow_html=True)

             
                st.plotly_chart(fig_pie, use_container_width=False)  

            else:
                st.error("Aucune classe d'âge avec un pourcentage supérieur ou égal à 0.1% n'a été trouvée.")

        else:
            st.error("Les colonnes nécessaires pour générer le graphique ne sont pas disponibles.")

       
        del filtered_df_display, filtered_staged_data, filtered_age_data_department
        gc.collect()
    else:
        st.error(f"One or more columns from {columns_to_display} are missing in the filtered data.")


###############################################################################################

elif st.session_state.page == "Age":
    st.markdown("""
        <h1 style="color: #00008B; text-align: center; font-size: 30px;">
            Analyse des pathologies par âge
        </h1>
    """, unsafe_allow_html=True)

    combined_data = pd.concat(
        [load_and_cache_data(year) for year in range(2015, 2023)], ignore_index=True
    )

   
    if combined_data not in st.session_state:
        st.session_state.combined_data = combined_data  

  
    age_groups = (
        combined_data["Age Group Label"]
        .drop_duplicates()  
        .sort_values()  
        .tolist()  
    )

   
    selected_age_group = st.selectbox(
        "Choisir un groupe d'âge pour analyser:", 
        options=age_groups, 
        index=0  
    )

  
    filtered_combined_data = combined_data.loc[
        combined_data["Age Group Label"] == selected_age_group
    ].copy()

   
    del combined_data
    gc.collect()

  
    pathology_level_1_list = (
        filtered_combined_data["Pathology Level 1"]
        .drop_duplicates()  
        .sort_values()  
        .reset_index(drop=True) 
    )

 
    if not pathology_level_1_list.empty:
        st.markdown("### Liste des pathologies (Niveau 1)")
      
        st.table(pathology_level_1_list.to_frame(name="Pathology Level 1"))
    else:
        st.warning("Aucune pathologie disponible pour le groupe d'âge sélectionné.")

   
    pathology_level_1_list = filtered_combined_data["Pathology Level 1"].drop_duplicates().sort_values().tolist()

  
    selected_pathology_level_1 = st.selectbox(
        "Choisir la pathologie du niveau 1",
        pathology_level_1_list,
        index=0,  
        key="pathology_level_1_select_age"
    )


    filtered_df_level_1 = filtered_combined_data[filtered_combined_data["Pathology Level 1"] == selected_pathology_level_1]

 
    pathology_level_2_list = (
        filtered_df_level_1["Pathology Level 2"]
        .dropna()  
        .loc[lambda x: x != "nan"]  
        .drop_duplicates()  
        .sort_values()  
        .tolist() 
    )

   
    selected_pathology_level_2 = st.selectbox(
        "Choisir la pathologie du niveau 2 (Sous-groupe de pathologies)",
        pathology_level_2_list,
        index=len(pathology_level_2_list) - 1,  
        key="pathology_level_2_select_departement"
    )

  
    filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1["Pathology Level 2"] == selected_pathology_level_2]

   
    pathology_level_3_list = (
        filtered_df_level_2["Pathology Level 3"]
        .dropna() 
        .loc[lambda x: x != "nan"]  
        .drop_duplicates()  
        .sort_values() 
        .tolist()  
    )

   
    selected_pathology_level_3 = st.selectbox(
        "Choisir la pathologie du niveau 3 (Sous-groupe détaillé de pathologies)",
        pathology_level_3_list,
        index=len(pathology_level_3_list) - 1,  
        key="pathology_level_3_select_departement"
    )

   
    filtered_data = filtered_df_level_2.loc[
        (filtered_df_level_2["Pathology Level 3"] == selected_pathology_level_3) &
        (filtered_df_level_2["Age Group Label"] == selected_age_group)
    ].copy()

    del filtered_df_level_1, filtered_df_level_2
    gc.collect()

  
    filtered_data_non_null = filtered_data[filtered_data["Patient Count (top)"].notnull()]
   
    filtered_data_non_null = filtered_data_non_null.sort_values(by="Patient Count (top)", ascending=False)

   
    grouped_data = (
        filtered_data_non_null.groupby(["Department Name", "Gender Label"])["Patient Count (top)"]
        .sum()
        .reset_index()
    )
    
    del filtered_data_non_null
    gc.collect()


   
    total_patients_national = grouped_data["Patient Count (top)"].sum()

  
    national_gender_distribution = (
        grouped_data.groupby("Gender Label")["Patient Count (top)"]
        .sum()
        .reset_index()
    )

   
    national_gender_distribution["% Gender"] = (
        national_gender_distribution["Patient Count (top)"] / total_patients_national * 100
    )

  
    fig_pie = px.pie(
        national_gender_distribution,
        names="Gender Label",  
        values="Patient Count (top)",  
        hole=0.4,  
    )

    
    fig_pie.update_traces(
        textinfo="percent+label",  
        hoverinfo="label+percent+value",  
    )
    fig_pie.update_layout(
        legend=dict(
            title="Genre",  
            orientation="v",  
            x=1.05,  
            y=0.5,  
            font=dict(size=12),  
        ),
        margin=dict(t=70, l=50, r=150, b=50), 
        height=400, 
        width=600,  
    )

  
    st.plotly_chart(fig_pie, use_container_width=False)

    del national_gender_distribution
    gc.collect()

  
    if not grouped_data.empty:
      
        st.dataframe(
            grouped_data, 
            use_container_width=True
        )
    else:
      
        st.warning("Aucune donnée patient n'existe pour le groupe d'âge et la pathologie sélectionnés.")

 
    map_data = grouped_data[["Department Name", "Patient Count (top)"]].copy()
    map_data = map_data.dropna(subset=["Patient Count (top)"])  

 
    if map_data.empty:
        st.error("No valid data available after cleaning.")
    else:
       
        geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"

    
        import requests
        response = requests.get(geojson_url)
        if response.status_code != 200:
            st.error("Failed to load GeoJSON data.")
        else:
            geojson_data = response.json()

          
            for feature in geojson_data["features"]:
                department_name = feature["properties"]["nom"]  
                if department_name in map_data["Department Name"].values:
                   
                    patient_count = map_data.loc[
                        map_data["Department Name"] == department_name, "Patient Count (top)"
                    ].iloc[0]
                    feature["properties"]["Patient Count (top)"] = int(patient_count)
                else:
                    feature["properties"]["Patient Count (top)"] = None

         
            min_value = map_data["Patient Count (top)"].min()
            max_value = map_data["Patient Count (top)"].max()

          
            m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

         
            folium.Choropleth(
                geo_data=geojson_data,
                name="choropleth",
                data=map_data,
                columns=["Department Name", "Patient Count (top)"],  
                key_on="feature.properties.nom", 
                fill_color="YlOrRd", 
                fill_opacity=0.7,
                line_opacity=0,
                nan_fill_color="#e1ebf5",  
                legend_name="Patient Count (top)",
                threshold_scale=[
                    min_value,
                    min_value + (max_value - min_value) * 0.25,
                    min_value + (max_value - min_value) * 0.5,
                    min_value + (max_value - min_value) * 0.75,
                    max_value,
                ],
            ).add_to(m)

           
            folium.GeoJson(
                geojson_data,
                tooltip=folium.features.GeoJsonTooltip(
                    fields=["nom", "Patient Count (top)"],  
                    aliases=["Department: ", "Patients: "],  
                    style="font-size:12px;", 
                    localize=True,
                ),
                
            ).add_to(m)

           
            st_folium(m, width=800, height=600)

         
            del geojson_data, m, map_data
            gc.collect()


###############################################################################################

elif st.session_state.page == "Sexe":
    st.markdown("""
        <h1 style="color: #00008B; text-align: center; font-size: 30px;">
            Analyse des pathologies par sexe
        </h1>
    """, unsafe_allow_html=True)

   
    combined_data = pd.concat(
        [load_and_cache_data(year) for year in range(2015, 2023)], ignore_index=True
    )

   
    if combined_data not in st.session_state:
        st.session_state.combined_data = combined_data  


   
    sex_groups = (
        combined_data["Gender Label"]
        .drop_duplicates()  
        .sort_values()  
        .tolist()  
    )

   
    selected_sex_group = st.selectbox(
        "Choisir un sexe pour analyser:", 
        options=sex_groups, 
        index=0  
    )

    
    filtered_combined_data = combined_data.loc[
        combined_data["Gender Label"] == selected_sex_group
    ].copy()

   
    del st.session_state.combined_data, combined_data
    gc.collect()

   
    pathology_level_1_list = (
        filtered_combined_data["Pathology Level 1"]
        .drop_duplicates()  
        .sort_values() 
        .reset_index(drop=True)  
    )

   
    if not pathology_level_1_list.empty:
        st.markdown("### Liste des pathologies (Niveau 1)")
       
        st.table(pathology_level_1_list.to_frame(name="Pathology Level 1"))
    else:
        st.warning("Aucune pathologie disponible pour le groupe d'âge sélectionné.")

   
    pathology_level_1_list = filtered_combined_data["Pathology Level 1"].drop_duplicates().sort_values().tolist()

  
    selected_pathology_level_1 = st.selectbox(
        "Choisir la pathologie du niveau 1",
        pathology_level_1_list,
        index=0,  
        key="pathology_level_1_select_age"
    )

    
    filtered_df_level_1 = filtered_combined_data[filtered_combined_data["Pathology Level 1"] == selected_pathology_level_1]

    
    pathology_level_2_list = (
        filtered_df_level_1["Pathology Level 2"]
        .dropna()  
        .loc[lambda x: x != "nan"]  
        .drop_duplicates()  
        .sort_values()  
        .tolist()  
    )

   
    selected_pathology_level_2 = st.selectbox(
        "Choisir la pathologie du niveau 2 (Sous-groupe de pathologies)",
        pathology_level_2_list,
        index=len(pathology_level_2_list) - 1, 
        key="pathology_level_2_select_departement"
    )

    
    filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1["Pathology Level 2"] == selected_pathology_level_2]

   
    pathology_level_3_list = (
        filtered_df_level_2["Pathology Level 3"]
        .dropna()  
        .loc[lambda x: x != "nan"]  
        .drop_duplicates()  
        .sort_values()  
        .tolist()  
    )

   
    selected_pathology_level_3 = st.selectbox(
        "Choisir la pathologie du niveau 3 (Sous-groupe détaillé de pathologies)",
        pathology_level_3_list,
        index=len(pathology_level_3_list) - 1,  
        key="pathology_level_3_select_departement"
    )

  
    filtered_data = filtered_df_level_2.loc[
        (filtered_df_level_2["Pathology Level 3"] == selected_pathology_level_3) &
        (filtered_df_level_2["Gender Label"] == selected_sex_group)
    ].copy()

    del filtered_df_level_1, filtered_df_level_2
    gc.collect()

  
    filtered_data_non_null = filtered_data[filtered_data["Patient Count (top)"].notnull()]
   
    filtered_data_non_null = filtered_data_non_null.sort_values(by="Patient Count (top)", ascending=False)

   
    grouped_data = (
        filtered_data_non_null.groupby(["Department Name", "Age Group Label"])["Patient Count (top)"]
        .sum()
        .reset_index()
    )
    
    del filtered_data_non_null
    gc.collect()

  
    total_patients_national = grouped_data["Patient Count (top)"].sum()

  
    national_sex_distribution = (
        grouped_data.groupby("Age Group Label")["Patient Count (top)"]
        .sum()
        .reset_index()
    )

  
    national_sex_distribution["% Age"] = (
        national_sex_distribution["Patient Count (top)"] / total_patients_national * 100
    )

   
    fig_pie = px.pie(
        national_sex_distribution,
        names="Age Group Label",  
        values="Patient Count (top)",  
        hole=0.4,  
    )

    
    fig_pie.update_traces(
        textinfo="percent",  
        hoverinfo="label+percent+value",  
    )
    fig_pie.update_layout(
        legend=dict(
            title="Age",  
            orientation="v",  
            x=1.05,  
            y=0.5,  
            font=dict(size=12),  
        ),
        margin=dict(t=70, l=50, r=150, b=50),  
        height=400,  
        width=600, 
    )

   
    st.plotly_chart(fig_pie, use_container_width=False)

    del national_sex_distribution
    gc.collect()

   
    if not grouped_data.empty:
       
        st.dataframe(
            grouped_data,
            use_container_width=True
        )
    else:
        
        st.warning("Aucune donnée patient n'existe pour le groupe d'âge et la pathologie sélectionnés.")

    map_data = grouped_data[["Department Name", "Patient Count (top)"]].copy()
    map_data = map_data.dropna(subset=["Patient Count (top)"])  

  
    if map_data.empty:
        st.error("No valid data available after cleaning.")
    else:
        
        geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"

      
        import requests
        response = requests.get(geojson_url)
        if response.status_code != 200:
            st.error("Failed to load GeoJSON data.")
        else:
            geojson_data = response.json()

           
            for feature in geojson_data["features"]:
                department_name = feature["properties"]["nom"]  
                if department_name in map_data["Department Name"].values:
                  
                    patient_count = map_data.loc[
                        map_data["Department Name"] == department_name, "Patient Count (top)"
                    ].iloc[0]
                    feature["properties"]["Patient Count (top)"] = int(patient_count)
                else:
                    feature["properties"]["Patient Count (top)"] = None

          
            min_value = map_data["Patient Count (top)"].min()
            max_value = map_data["Patient Count (top)"].max()

           
            m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

        
            folium.Choropleth(
                geo_data=geojson_data,
                name="choropleth",
                data=map_data,
                columns=["Department Name", "Patient Count (top)"], 
                key_on="feature.properties.nom",  
                fill_color="YlOrRd",  
                fill_opacity=0.7,
                line_opacity=0,
                nan_fill_color="#e1ebf5",  
                legend_name="Patient Count (top)",
                threshold_scale=[
                    min_value,
                    min_value + (max_value - min_value) * 0.25,
                    min_value + (max_value - min_value) * 0.5,
                    min_value + (max_value - min_value) * 0.75,
                    max_value,
                ],
            ).add_to(m)

          
            folium.GeoJson(
                geojson_data,
                tooltip=folium.features.GeoJsonTooltip(
                    fields=["nom", "Patient Count (top)"],  
                    aliases=["Department: ", "Patients: "],  
                    style="font-size:12px;", 
                    localize=True,
                ),
                
            ).add_to(m)

           
            st_folium(m, width=800, height=600)

         
            del geojson_data, m, map_data
            gc.collect()