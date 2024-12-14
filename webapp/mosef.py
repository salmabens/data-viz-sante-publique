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


# Charger les données (avec mise en cache pour améliorer les performances)
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

# Định nghĩa danh sách các năm từ 2015 đến 2022
years = list(range(2015, 2023))

###############################################################################################

# Sidebar: Tạo các nút thả xuống
with st.sidebar:

    st.title("Menu de Navigation")  # Tiêu đề thanh bên

    # Tạo các expander cho điều hướng
    page = None  # Biến để lưu lựa chọn của người dùng
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
    /* Thay đổi màu nền của sidebar */
    [data-testid="stSidebar"] {
        background-color: #00008B; /* Màu xanh dương đậm */
    }

    /* Tùy chỉnh tiêu đề "Menu de Navigation" */
    [data-testid="stSidebar"] h1 {
        color: white; /* Màu chữ trắng */
        font-size: 22px; /* Kích thước chữ */
        font-weight: bold; /* Chữ in đậm */
    }

    /* Tùy chỉnh tiêu đề của các expander */
    [data-testid="stSidebar"] .stExpander > div > div:first-child {
        font-size: 16px; /* Kích thước chữ cho tiêu đề expander */
        color: white; /* Màu chữ trắng */
        font-weight: bold; /* Chữ in đậm */
    }

    /* Tùy chỉnh các nút bên trong expander */
    [data-testid="stSidebar"] .stButton button {
        color: white; /* Màu chữ của nút */
        font-weight: 300; /* Chữ mỏng */
        background-color: #1b1bf7; /* Màu nền của nút */
        border: 1px solid white; /* Viền nút màu trắng */
        border-radius: 15px; /* Bo tròn các góc của nút */
        font-size: 16px; /* Kích thước chữ nhỏ hơn */
        padding: 6px 12px; /* Giảm padding để nút gọn hơn */
    }

    /* Khi hover vào nút */
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #0059b3; /* Màu nền khi hover */
        color: #ffffff; /* Màu chữ khi hover */
    }

    /* Tùy chỉnh expander */
    [data-testid="stSidebar"] .stExpander {
        border: 0.7px solid white; /* Viền màu trắng cho expander */
        border-radius: 10px; /* Bo tròn các góc của expander */
        margin-bottom: 10px; /* Khoảng cách giữa các expander */
    }

    /* Tùy chỉnh chữ bên trong expander */
    [data-testid="stSidebar"] .stExpander div {
        color: white; /* Màu chữ trắng */
        font-size: 16px; /* Kích thước chữ nhỏ hơn */
        font-weight: 300; /* Chữ mỏng hơn cho nội dung */
    }
    </style>
""", unsafe_allow_html=True)


###############################################################################################

# Main Content: Hiển thị nội dung theo trang được chọn
# Kiểm tra và khởi tạo giá trị cho st.session_state.page
if "page" not in st.session_state:
    st.session_state.page = "Accueil"  # Giá trị mặc định ban đầu

# Main Content: Hiển thị nội dung theo trang được chọn
if st.session_state.page == "Accueil" or "page" not in locals():

    # Đường dẫn tới logo
    logo_path = os.path.abspath("static/logo.jpeg")

    # Tạo bố cục với st.columns để căn giữa logo
    col1, col2, col3 = st.columns([3, 3, 2])  # Tạo 3 cột với cột giữa rộng hơn

    with col2:  # Đặt logo ở cột giữa
        st.image(logo_path, use_container_width =False, width=150)

    # Tiêu đề trang
    st.markdown("""
        <h1 style="color: #00008B; text-align: center; font-size: 34px;">
            Bienvenue sur DataViz Santé Publique
        </h1>
    """, unsafe_allow_html=True)

    # Nội dung chính đơn giản hóa
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

    # Tạo footer bản quyền
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

   # Lựa chọn năm từ năm 2015 đến 2022 với giá trị mặc định là 2022
    selected_year = st.selectbox(
        "Choisir l'année:", 
        list(range(2015, 2023)), 
        index=len(range(2015, 2023)) - 1,  # Đặt mặc định là năm cuối cùng trong danh sách (năm 2022)
        key="year_select"  # Đặt một key duy nhất để tránh trùng lặp ID
    )

    # Load dữ liệu cho năm được chọn từ dictionary
    df = load_patients_by_region_data(selected_year)

    # Gộp CSS để chỉnh sửa font chữ, độ dày của các thanh chọn và nội dung bên trong selectbox
    st.markdown("""
        <style>
        /* Chỉnh font chữ và kiểu dáng cho thanh selectbox */
        div[role="combobox"] > div {
            font-size: 12px;  /* Cỡ chữ nhỏ */
            font-weight: 300;  /* Chữ mảnh */
        }
        div[role="combobox"] > div > div {
            font-size: 12px;  /* Cỡ chữ cho các tùy chọn */
        }

        /* Thay đổi chiều cao, góc bo tròn và màu nền của selectbox */
        div[data-baseweb="select"] {
            height: 35px;  /* Độ cao của thanh selectbox */
            border-radius: 5px;  /* Góc bo tròn */
            background-color: #add8e6;  /* Màu xanh dương nhạt (LightBlue) */
            color: black;  /* Màu chữ bên trong */
        }

        /* Thay đổi font chữ bên trong các lựa chọn */
        div[data-baseweb="select"] > div {
            font-size: 14px;  /* Cỡ chữ nội dung bên trong selectbox */
        }

        /* Thay đổi font chữ của nội dung thả xuống */
        div[data-baseweb="select"] .css-1nfy0zz {
            font-size: 14px;  /* Font chữ nhỏ hơn */
        }

        /* Thay đổi khoảng cách và màu nền khi hover */
        div[data-baseweb="select"] .css-1nfy0zz:hover {
            background-color: #87cefa; /* Màu xanh dương sáng hơn khi hover (SkyBlue) */
        }
        </style>
    """, unsafe_allow_html=True)

    # Tạo danh sách các giá trị unique cho Pathology Level 1
    pathology_level_1_list = df['Pathology Level 1'].unique()

    # Tạo nút chọn cho Pathology Level 1 với giá trị mặc định là "Diabète" nếu có
    default_index_level_1 = list(pathology_level_1_list).index("Cancers") if "Cancers" in pathology_level_1_list else 0
    selected_pathology_level_1 = st.selectbox(
        "Choisir la pathologie du niveau 1",
        pathology_level_1_list,
        index=default_index_level_1,
        key="pathology_level_1_select"
    )

    # Lọc dữ liệu theo Pathology Level 1
    filtered_df_level_1 = df[df['Pathology Level 1'] == selected_pathology_level_1]

    # Tạo danh sách các giá trị unique cho Pathology Level 2 từ dữ liệu đã lọc
    pathology_level_2_list = filtered_df_level_1['Pathology Level 2'].unique().tolist()

    # Tạo nút chọn cho Pathology Level 2
    selected_pathology_level_2 = st.selectbox(
        "Choisir la pathologie du niveau 2 (Sous-groupe de pathologies)",
        pathology_level_2_list,
        index=len(pathology_level_2_list) - 1,  # Đặt giá trị cuối làm giá trị mặc định
        key="pathology_level_2_select"
    )
    filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1['Pathology Level 2'] == selected_pathology_level_2]


    # Tạo danh sách các giá trị unique cho Pathology Level 3 từ dữ liệu đã lọc
    pathology_level_3_list = filtered_df_level_2['Pathology Level 3'].unique().tolist()

    # Tạo nút chọn cho Pathology Level 3
    selected_pathology_level_3 = st.selectbox(
        "Choisir la pathologie du niveau 3 (Sous-groupe détaillé de pathologies)",
        pathology_level_3_list,
        index=len(pathology_level_3_list) - 1,  # Đặt giá trị cuối làm giá trị mặc định
        key="pathology_level_3_select"
    )

    filtered_df = filtered_df_level_2.loc[
        (filtered_df_level_2['Pathology Level 3'] == selected_pathology_level_3) & 
        (filtered_df_level_2['Region'] != 99)
    ].copy()  # Tạo một bản sao rõ ràng

    # Các cột cần hiển thị và kiểm tra
    columns_to_display = ["Region Name", "Patient Count (top)"]

    if all(col in filtered_df.columns for col in columns_to_display):
        # Lọc và sắp xếp dữ liệu
        filtered_df_display = filtered_df[columns_to_display].sort_values(
            by="Patient Count (top)", ascending=True
        )

        # Tạo biểu đồ thanh ngang
        fig = px.bar(
            filtered_df_display,
            y="Region Name",  # Trục Y là tên vùng
            x="Patient Count (top)",  # Trục X là số lượng bệnh nhân
            orientation="h",  # Thanh ngang
            text="Patient Count (top)",  # Hiển thị dữ liệu trên thanh
        )

        # Làm tròn giá trị hiển thị trên thanh
        fig.update_traces(
            texttemplate="%{text:,}".replace(",", " "),  # Hiển thị dữ liệu với khoảng cách cho hàng nghìn
            textposition="outside",  # Hiển thị dữ liệu bên trong thanh
            marker_color="#1b1bf7",  # Màu xanh dương
            marker_line_width=0,  # Loại bỏ viền của thanh
            width=0.4,  # Làm mỏng các thanh biểu đồ
        )

        # Tùy chỉnh giao diện
        fig.update_layout(
            template="none",  # Loại bỏ template mặc định
            paper_bgcolor="rgba(0,0,0,0)",  # Nền toàn bộ biểu đồ trong suốt
            plot_bgcolor="rgba(0,0,0,0)",  # Nền bên trong vùng biểu đồ trong suốt
            margin=dict(t=20, l=200, r=20, b=20),  # Giảm margin bên phải để căn trái
            height=450,  # Tăng chiều cao biểu đồ
            xaxis=dict(
                title=None,  # Loại bỏ tiêu đề trục X
                showgrid=False,  # Loại bỏ lưới trên trục X
                zeroline=False,  # Loại bỏ đường zero
                showticklabels=False,  # Loại bỏ nhãn trên trục X
            ),
            yaxis=dict(
                title=None,  # Loại bỏ tiêu đề trục Y
                tickfont=dict(size=12),  # Tăng cỡ chữ để hiển thị đầy đủ tên vùng
                showline=False,  # Loại bỏ đường viền
                automargin=True,  # Tự động căn chỉnh margin để tên hiển thị rõ ràng
            ),
        )

        # Hiển thị biểu đồ trong Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Dọn dẹp dữ liệu tạm thời
        del filtered_df_display
        gc.collect()
    else:
        st.error(f"One or more columns from {columns_to_display} are missing in the filtered data.")

    # Giả sử filtered_df đã được lọc theo năm và Pathology Levels
    columns_to_display = ["Region Name", "Patient Count (top)"]
    if all(col in filtered_df.columns for col in columns_to_display):
        # Lấy dữ liệu chỉ với các cột cần thiết
        data = filtered_df[columns_to_display]

        # Kiểm tra và điền giá trị thiếu
        data["Region Name"] = data["Region Name"].fillna("Non renseigné")

        # Tính toán các chỉ số thống kê
        max_region = data.loc[data["Patient Count (top)"].idxmax()]
        min_region = data.loc[data["Patient Count (top)"].idxmin()]
        avg_patient_count = round(data["Patient Count (top)"].mean())
        median_patient_count = round(data["Patient Count (top)"].median())

        # Xử lý giá trị hiển thị với định dạng số
        max_patient_count = f"{int(max_region['Patient Count (top)']):,}".replace(",", " ")
        min_patient_count = f"{int(min_region['Patient Count (top)']):,}".replace(",", " ")
        avg_patient_count_display = f"{avg_patient_count:,}".replace(",", " ")
        median_patient_count_display = f"{median_patient_count:,}".replace(",", " ")

        # Dọn dẹp dữ liệu tạm thời
        del data
        gc.collect()

        # Hiển thị các nút với thông tin thống kê
        st.markdown(f"""
        <style>
        .stat-box {{
            display: flex;
            justify-content: space-between;
            align-items: stretch; /* Căn đều chiều cao các nút */
            margin-top: 20px;
        }}
        .stat-item {{
            text-align: center;
            background-color: #ffcc00;
            padding: 15px; /* Giảm padding để nút nhỏ gọn hơn */
            border-radius: 10px;
            flex: 1;
            margin: 0 10px;
            color: white;
            font-family: Arial, sans-serif;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column; /* Căn chỉnh theo chiều dọc */
            justify-content: center; /* Căn giữa nội dung */
            align-items: center; /* Căn giữa nội dung */
            min-height: 150px; /* Giảm chiều cao tối thiểu */
            max-height: 150px; /* Giảm chiều cao tối đa */
        }}
        .stat-item span {{
            font-size: 16px;  /* Kích thước chữ nhỏ hơn cho tên vùng */
            font-weight: 400; /* Làm chữ thanh mảnh */
        }}
        .stat-item small {{
            font-size: 12px;  /* Kích thước nhỏ hơn cho mô tả */
            font-weight: 300; /* Làm chữ mỏng hơn */
            margin-top: 8px; /* Giảm khoảng cách giữa các thành phần */
        }}
        .stat-item .number {{
            font-size: 24px; /* Kích thước chữ cho số liệu */
            font-weight: 600; /* Làm chữ đậm hơn cho số liệu */
            margin-top: 5px; /* Khoảng cách giữa tên và số liệu */
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

    # Chèn một dòng trống giữa khối thống kê và bản đồ
    st.markdown("<br>", unsafe_allow_html=True)

     # Kiểm tra nếu dữ liệu đã lọc có các cột cần thiết
    required_columns = ["Region Name", "Patient Count (top)"]

    if all(column in filtered_df.columns for column in required_columns):
        # Chuẩn bị dữ liệu
        map_data = filtered_df[["Region Name", "Patient Count (top)"]].copy()
        map_data = map_data.dropna(subset=["Patient Count (top)"])  # Loại bỏ giá trị NaN

        # Kiểm tra nếu map_data còn dữ liệu
        if map_data.empty:
            st.error("No valid data available after cleaning.")
        else:
            # Đường dẫn tới tệp GeoJSON chứa thông tin biên giới của các vùng
            geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson"

            # Tải GeoJSON
            import requests
            response = requests.get(geojson_url)
            if response.status_code != 200:
                st.error("Failed to load GeoJSON data.")
            else:
                geojson_data = response.json()

                # Thêm dữ liệu vào GeoJSON (mapping Region Name -> Patient Count)
                for feature in geojson_data["features"]:
                    region_name = feature["properties"]["nom"]  # Thuộc tính 'nom' là tên vùng
                    if region_name in map_data["Region Name"].values:
                        # Lấy giá trị duy nhất tương ứng với Region Name
                        patient_count = map_data.loc[
                            map_data["Region Name"] == region_name, "Patient Count (top)"
                        ].iloc[0]
                        feature["properties"]["Patient Count (top)"] = int(patient_count)
                    else:
                        feature["properties"]["Patient Count (top)"] = "No Data"

                # Khởi tạo bản đồ trung tâm tại Pháp
                m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

                # Ánh xạ dữ liệu vào GeoJSON
                folium.Choropleth(
                    geo_data=geojson_data,
                    name="choropleth",
                    data=map_data,
                    columns=["Region Name", "Patient Count (top)"],  # Dữ liệu ánh xạ
                    key_on="feature.properties.nom",  # Thuộc tính trong GeoJSON tương ứng với "Region Name"
                    fill_color="YlOrRd",  # Thang màu (vàng đến đỏ)
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    nan_fill_color="#e1ebf5",  # Đổi màu mặc định cho vùng không có dữ liệu thành xanh dương nhạt
                    legend_name="Patient Count (top)",
                ).add_to(m)

                # Thêm tooltip hiển thị thông tin khi trỏ chuột
                folium.GeoJson(
                    geojson_data,
                    style_function=lambda x: {
                        "fillColor": "YlOrRd",
                        "color": "black",
                        "weight": 0.2,
                        "dashArray": "5, 5",
                    },
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=["nom", "Patient Count (top)"],  # Hiển thị tên vùng và số bệnh nhân
                        aliases=["Region: ", "Patients: "],  # Nhãn hiển thị
                        style="font-size:12px;",  # Kiểu chữ
                        localize=True,
                    ),
                ).add_to(m)

                # Hiển thị bản đồ trong Streamlit
                st_folium(m, width=800, height=600)

                # Dọn dẹp dữ liệu GeoJSON
                del geojson_data, m, map_data
                gc.collect()
    else:
        st.error("Les colonnes 'Region Name' et 'Patient Count (top)' sont manquantes dans les données.")

    # Gộp dữ liệu qua các năm nhưng chỉ lọc theo Pathology Levels đã chọn
    all_years_data = []

    # Duyệt qua từng năm
    for year in years:
        # Lấy dữ liệu từng năm
        df_year = load_patients_by_region_data(year).copy()  # Gọi hàm với year làm tham số

        # Lọc theo Pathology Level 1
        filtered_df_level_1 = df_year[df_year['Pathology Level 1'] == selected_pathology_level_1]

        # Lọc theo Pathology Level 2
        filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1['Pathology Level 2'] == selected_pathology_level_2]

        filtered_df = filtered_df_level_2.loc[
            (filtered_df_level_2['Pathology Level 3'] == selected_pathology_level_3) &
            (filtered_df_level_2['Region'] != 99)
        ].copy()  # Thêm .copy() để tránh cảnh báo

        # Thêm cột năm vào DataFrame
        filtered_df["Year"] = year

        # Append dữ liệu đã lọc vào danh sách
        all_years_data.append(filtered_df)

        # Xóa dữ liệu trung gian sau khi append
        del df_year, filtered_df_level_1, filtered_df_level_2, filtered_df
        gc.collect()  # Dọn rác

    # Kết hợp tất cả dữ liệu qua các năm
    combined_data = pd.concat(all_years_data, ignore_index=True)

    # Xóa danh sách dữ liệu trung gian
    del all_years_data
    gc.collect()  # Dọn rác

    # Nhóm dữ liệu theo Region và Year để tính tổng số bệnh nhân
    region_year_data = combined_data.groupby(["Region Name", "Year"])["Patient Count (top)"].sum().reset_index()

    # Xóa dữ liệu trung gian
    del combined_data
    gc.collect()  # Dọn rác

    # Tạo biểu đồ đường để hiển thị evolution
    fig = px.line(
        region_year_data,
        x="Year",
        y="Patient Count (top)",
        color="Region Name",  # Phân biệt theo từng vùng
        labels={"Patient Count (top)": "Nombre de patients", "Year": "Année"},
        title=f"Évolution du nombre de patients pour {selected_pathology_level_1}, {selected_pathology_level_2}, {selected_pathology_level_3}"
    )

    # Tùy chỉnh giao diện biểu đồ
    fig.update_layout(
        template="simple_white",
        title_x=0.5,  # Căn giữa tiêu đề
        legend_title_text="Région",
        xaxis=dict(title="Année"),
        yaxis=dict(title="Nombre de patients"),
        margin=dict(l=50, r=50, t=50, b=50),  # Căn chỉnh margin
        height=500  # Chiều cao của biểu đồ
    )

    # Hiển thị gợi ý ngay trước biểu đồ
    st.markdown("""
    <p style="font-size: 14px; font-style: italic; color: gray;">
    Astuce : Cliquez sur les noms des régions dans la légende pour les masquer/afficher.
    </p>
    """, unsafe_allow_html=True)

    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Lấy danh sách các vùng từ dữ liệu
    regions_list = region_year_data["Region Name"].unique().tolist()

    # Sắp xếp danh sách các vùng theo thứ tự chữ cái (tùy chọn)
    regions_list.sort()

    # Dropdown để chọn vùng
    selected_region = st.selectbox(
        "Choisir une région :", 
        options=regions_list, 
        index=0
    )

    # Lọc dữ liệu theo vùng được chọn
    region_data = region_year_data[region_year_data["Region Name"] == selected_region]

    # Xóa dữ liệu trung gian sau khi lọc
    del region_year_data
    gc.collect()

    # Tạo biểu đồ với dữ liệu hiển thị cho từng năm
    fig = px.line(
        region_data,
        x="Year",
        y="Patient Count (top)",
        labels={"Patient Count (top)": "Nombre de patients", "Year": "Année"},
        title=f"Évolution du nombre de patients pour la région {selected_region}"
    )

    # Thêm các điểm dữ liệu (markers) và hiển thị giá trị
    fig.update_traces(
        mode="lines+markers+text",  # Hiển thị đường, điểm và nhãn
        text=region_data["Patient Count (top)"],  # Nhãn giá trị tương ứng với từng năm
        textposition="top center",  # Vị trí của nhãn
        line_color="#1b1bf7"  # Màu đường là xanh dương đậm
    )

    # Cập nhật giao diện biểu đồ
    fig.update_layout(
        template="none",  # Xóa template mặc định
        height=500,  # Chiều cao của biểu đồ
        title={
            "text": f"Évolution du nombre de patients pour la région {selected_region}",
            "x": 0.5,  # Căn giữa tiêu đề
            "xanchor": "center"
        },
        xaxis=dict(
            title="Année",  # Tiêu đề trục X
            showgrid=False  # Loại bỏ lưới
        ),
        yaxis=dict(
            title="Nombre de patients",  # Tiêu đề trục Y
            showgrid=True  # Hiển thị lưới để dễ nhìn hơn
        )
    )

    # Hiển thị gợi ý ngay trước biểu đồ
    st.markdown("""
    <p style="font-size: 14px; font-style: italic; color: gray;">
    Astuce : Si vous souhaitez zoomer sur l'évolution d'une seule région, veuillez sélectionner la région dans la liste déroulante ci-dessous.
    </p>
    """, unsafe_allow_html=True)

    # Hiển thị biểu đồ
    st.plotly_chart(fig, use_container_width=True)

    # Xóa dữ liệu sau khi hiển thị
    del region_data
    gc.collect()


###############################################################################################

# Main Content: Hiển thị nội dung theo trang được chọn
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

    # Lựa chọn năm từ năm 2015 đến 2022 với giá trị mặc định là 2022
    selected_year = st.selectbox(
        "Choisir l'année:", 
        list(range(2015, 2023)), 
        index=len(range(2015, 2023)) - 1,  # Đặt mặc định là năm cuối cùng trong danh sách (năm 2022)
        key="year_select_departement"  # Đặt một key duy nhất để tránh trùng lặp ID
    )

    # Load dữ liệu cho năm được chọn từ dictionary
    df = load_patients_by_department_data(selected_year)
    # Lọc bỏ dòng có giá trị "Hors France Métropolitaine" trong cột "Department Name"
    df = df[df["Department Name"] != "Hors France Métropolitaine"].copy()

    # Tạo danh sách các giá trị unique cho Pathology Level 1
    pathology_level_1_list = df['Pathology Level 1'].unique()

    # Tạo nút chọn cho Pathology Level 1 với giá trị mặc định là "Diabète" nếu có
    default_index_level_1 = list(pathology_level_1_list).index("Cancers") if "Cancers" in pathology_level_1_list else 0
    selected_pathology_level_1 = st.selectbox(
        "Choisir la pathologie du niveau 1",
        pathology_level_1_list,
        index=default_index_level_1,
        key="pathology_level_1_select_departement"
    )

    # Lọc dữ liệu theo Pathology Level 1
    filtered_df_level_1 = df[df['Pathology Level 1'] == selected_pathology_level_1]

    # Tạo danh sách các giá trị unique cho Pathology Level 2 từ dữ liệu đã lọc
    pathology_level_2_list = filtered_df_level_1['Pathology Level 2'].unique().tolist()

    # Tạo nút chọn cho Pathology Level 2
    selected_pathology_level_2 = st.selectbox(
        "Choisir la pathologie du niveau 2 (Sous-groupe de pathologies)",
        pathology_level_2_list,
        index=len(pathology_level_2_list) - 1,  # Đặt giá trị cuối làm giá trị mặc định
        key="pathology_level_2_select_departement"
    )
    filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1['Pathology Level 2'] == selected_pathology_level_2]

    # Tạo danh sách các giá trị unique cho Pathology Level 3 từ dữ liệu đã lọc
    pathology_level_3_list = filtered_df_level_2['Pathology Level 3'].unique().tolist()

    # Tạo nút chọn cho Pathology Level 3
    selected_pathology_level_3 = st.selectbox(
        "Choisir la pathologie du niveau 3 (Sous-groupe détaillé de pathologies)",
        pathology_level_3_list,
        index=len(pathology_level_3_list) - 1,  # Đặt giá trị cuối làm giá trị mặc định
        key="pathology_level_3_select_departement"
    )

    filtered_df = filtered_df_level_2.loc[
        (filtered_df_level_2['Pathology Level 3'] == selected_pathology_level_3) & 
        (filtered_df_level_2['Department'] != 99)
    ].copy()  # Tạo một bản sao rõ ràng
    

    # Tải dữ liệu staged_data_year cho năm được chọn
    staged_data_year = load_staged_data(selected_year)

    # Lọc dữ liệu từ bảng staged_data_year theo các giá trị đã chọn
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

    # Các cột cần hiển thị và kiểm tra
    columns_to_display = ["Department Name", "Age Group Label", "Patient Count (top)", "Total Population", "Prevalence"]

    if all(col in filtered_staged_data.columns for col in columns_to_display):
        # Lọc, loại bỏ các hàng có "Department Name" là "Hors France Métropolitaine" hoặc "Patient Count (top)" rỗng
        filtered_df_display = (
            filtered_staged_data.loc[
                (filtered_staged_data["Department Name"] != "Hors France Métropolitaine") &  # Loại bỏ dòng không mong muốn
                (filtered_staged_data["Patient Count (top)"].notna())  # Loại bỏ dòng có giá trị rỗng
            ][columns_to_display]
            .drop_duplicates()  # Loại bỏ các dòng trùng lặp
            .sort_values(by=["Department Name", "Patient Count (top)"], ascending=[True, False])  # Sắp xếp theo tên vùng và giá trị bệnh nhân
        )

        # Hiển thị bảng dữ liệu trong Streamlit
        st.dataframe(filtered_df_display, use_container_width=True)

        # Dọn dẹp dữ liệu tạm thời
        del filtered_df_display #, filtered_staged_data
        gc.collect()
    else:
        st.error(f"One or more columns from {columns_to_display} are missing in the filtered data.")

    # Giả sử filtered_df đã được lọc theo năm và Pathology Levels
    columns_to_display = ["Department Name", "Patient Count (top)"]
    if all(col in filtered_df.columns for col in columns_to_display):
        # Lấy dữ liệu chỉ với các cột cần thiết
        data = filtered_df[columns_to_display]

        # Kiểm tra và điền giá trị thiếu
        data.loc[:, "Department Name"] = data["Department Name"].fillna("Non renseigné")

        # Tính toán các chỉ số thống kê
        max_department = data.loc[data["Patient Count (top)"].idxmax()]
        min_department = data.loc[data["Patient Count (top)"].idxmin()]
        avg_patient_count = round(data["Patient Count (top)"].mean())
        median_patient_count = round(data["Patient Count (top)"].median())

        # Xử lý giá trị hiển thị với định dạng số
        max_patient_count = f"{int(max_department['Patient Count (top)']):,}".replace(",", " ")
        min_patient_count = f"{int(min_department['Patient Count (top)']):,}".replace(",", " ")
        avg_patient_count_display = f"{avg_patient_count:,}".replace(",", " ")
        median_patient_count_display = f"{median_patient_count:,}".replace(",", " ")

        # Hiển thị các nút với thông tin thống kê
        st.markdown(f"""
            <style>
            .stat-box {{
                display: flex;
                justify-content: space-between;
                align-items: stretch; /* Căn đều chiều cao các nút */
                margin-top: 20px;
            }}
            .stat-item {{
                text-align: center;
                background-color: #ffcc00;
                padding: 15px; /* Giảm padding để nút nhỏ gọn hơn */
                border-radius: 10px;
                flex: 1;
                margin: 0 10px;
                color: white;
                font-family: Arial, sans-serif;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column; /* Căn chỉnh theo chiều dọc */
                justify-content: center; /* Căn giữa nội dung */
                align-items: center; /* Căn giữa nội dung */
                min-height: 150px; /* Giảm chiều cao tối thiểu */
                max-height: 150px; /* Giảm chiều cao tối đa */
            }}
            .stat-item span {{
                font-size: 16px;  /* Cỡ chữ cho số giống region */
                font-weight: bold; /* Chữ đậm giống region */
            }}
            .stat-item small {{
                font-size: 12px;  /* Cỡ chữ mô tả giống region */
                font-weight: 300; /* Chữ mỏng giống region */
                margin-top: 10px;
            }}
            .stat-item .number {{
                font-size: 24px; /* Kích thước chữ cho số liệu */
                font-weight: 600; /* Làm chữ đậm hơn cho số liệu */
                margin-top: 5px; /* Khoảng cách giữa tên và số liệu */
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

        # Dọn dẹp dữ liệu tạm thời
        del data
        gc.collect()
    else:
        st.error(f"One or more columns from {columns_to_display} are missing in the filtered data.")
    
    # Chèn một dòng trống giữa khối thống kê và bản đồ
    st.markdown("<br>", unsafe_allow_html=True)

    # Phần bản đồ
    if all(column in filtered_df.columns for column in columns_to_display):
        # Chuẩn bị dữ liệu
        map_data = filtered_df[["Department Name", "Patient Count (top)"]].copy()
        map_data = map_data.dropna(subset=["Patient Count (top)"])  # Loại bỏ giá trị NaN

         # Kiểm tra nếu map_data còn dữ liệu
        if map_data.empty:
            st.error("No valid data available after cleaning.")
        else:
            # Đường dẫn tới tệp GeoJSON chứa thông tin biên giới của các vùng
            geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"

            # Tải GeoJSON
            import requests
            response = requests.get(geojson_url)
            if response.status_code != 200:
                st.error("Failed to load GeoJSON data.")
            else:
                geojson_data = response.json()

                # Thêm dữ liệu vào GeoJSON (mapping Department Name -> Patient Count)
                for feature in geojson_data["features"]:
                    department_name = feature["properties"]["nom"]  # Thuộc tính 'nom' là tên vùng
                    if department_name in map_data["Department Name"].values:
                        # Lấy giá trị duy nhất tương ứng với Department Name
                        patient_count = map_data.loc[
                            map_data["Department Name"] == department_name, "Patient Count (top)"
                        ].iloc[0]
                        feature["properties"]["Patient Count (top)"] = int(patient_count)
                    else:
                        feature["properties"]["Patient Count (top)"] = None

                # Tìm giá trị min và max
                min_value = map_data["Patient Count (top)"].min()
                max_value = map_data["Patient Count (top)"].max()

                # Khởi tạo bản đồ trung tâm tại Pháp
                m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

                # Ánh xạ dữ liệu vào GeoJSON
                folium.Choropleth(
                    geo_data=geojson_data,
                    name="choropleth",
                    data=map_data,
                    columns=["Department Name", "Patient Count (top)"],  # Dữ liệu ánh xạ
                    key_on="feature.properties.nom",  # Thuộc tính trong GeoJSON tương ứng với "Department Name"
                    fill_color="YlOrRd",  # Thang màu (vàng đến đỏ)
                    fill_opacity=0.7,
                    line_opacity=0,
                    nan_fill_color="#e1ebf5",  # Đổi màu mặc định cho vùng không có dữ liệu thành xanh dương nhạt
                    legend_name="Patient Count (top)",
                    threshold_scale=[
                        min_value,
                        min_value + (max_value - min_value) * 0.25,
                        min_value + (max_value - min_value) * 0.5,
                        min_value + (max_value - min_value) * 0.75,
                        max_value,
                    ],
                ).add_to(m)

                # Thêm tooltip hiển thị thông tin khi trỏ chuột
                folium.GeoJson(
                    geojson_data,
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=["nom", "Patient Count (top)"],  # Hiển thị tên vùng và số bệnh nhân
                        aliases=["Department: ", "Patients: "],  # Nhãn hiển thị
                        style="font-size:12px;",  # Kiểu chữ
                        localize=True,
                    ),
                    
                ).add_to(m)

                # Hiển thị bản đồ trong Streamlit
                st_folium(m, width=800, height=600)

                # Dọn dẹp dữ liệu GeoJSON
                del geojson_data, m, map_data
                gc.collect()

    else:
        st.error("Les colonnes 'Department Name' et 'Patient Count (top)' sont manquantes dans les données.")

    # Gộp dữ liệu qua các năm nhưng chỉ lọc theo Pathology Levels đã chọn
    all_years_data = []

    # Duyệt qua từng năm
    for year in years:
        # Lấy dữ liệu từng năm
        df_year = load_patients_by_department_data(year).copy()  # Gọi hàm với year làm tham số

        # Loại bỏ giá trị "Hors France Métropolitaine"
        df_year = df_year[df_year["Department Name"] != "Hors France Métropolitaine"]

        # Lọc theo Pathology Level 1
        filtered_df_level_1 = df_year[df_year['Pathology Level 1'] == selected_pathology_level_1]

        # Lọc theo Pathology Level 2
        filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1['Pathology Level 2'] == selected_pathology_level_2]

        # Lọc theo Pathology Level 3
        filtered_df = filtered_df_level_2.loc[
            (filtered_df_level_2['Pathology Level 3'] == selected_pathology_level_3) &
            (filtered_df_level_2['Department'] != 999)
        ].copy()

        # Thêm cột năm vào DataFrame
        filtered_df["Year"] = year

        # Append dữ liệu đã lọc vào danh sách
        all_years_data.append(filtered_df)

        # Dọn dẹp dữ liệu tạm thời
        del df_year, filtered_df_level_1, filtered_df_level_2, filtered_df
        gc.collect()

    # Kết hợp tất cả dữ liệu qua các năm (thực hiện ngoài vòng lặp)
    combined_data = pd.concat(all_years_data, ignore_index=True)

    # Nhóm dữ liệu theo Department và Year để tính tổng số bệnh nhân
    department_year_data = combined_data.groupby(["Department Name", "Year"])["Patient Count (top)"].sum().reset_index()

    # Xóa dữ liệu trung gian
    del all_years_data, combined_data
    gc.collect()

    # Dropdown để chọn département
    departments_list = department_year_data["Department Name"].unique().tolist()
    departments_list.sort()  # Sắp xếp tên département theo thứ tự chữ cái
    selected_department = st.selectbox(
        "Choisir un département :", 
        options=departments_list, 
        index=0
    )

    # Lọc dữ liệu theo département được chọn
    department_data = department_year_data[department_year_data["Department Name"] == selected_department]

    # Tạo biểu đồ với dữ liệu hiển thị cho từng năm
    fig = px.line(
        department_data,
        x="Year",
        y="Patient Count (top)",
        labels={"Patient Count (top)": "Nombre de patients", "Year": "Année"},
        title=f"Évolution du nombre de patients pour le département {selected_department}"
    )

    # Thêm các điểm dữ liệu (markers) và hiển thị giá trị
    fig.update_traces(
        mode="lines+markers+text",  # Hiển thị đường, điểm và nhãn
        text=department_data["Patient Count (top)"],  # Nhãn giá trị tương ứng với từng năm
        textposition="top center",  # Vị trí của nhãn
        line_color="#1b1bf7"  # Màu đường là xanh dương đậm
    )

    # Cập nhật giao diện biểu đồ
    fig.update_layout(
        template="none",  # Xóa template mặc định
        height=500,  # Chiều cao của biểu đồ
        title={
            "text": f"Évolution du nombre de patients pour le département {selected_department}",
            "x": 0.5,  # Căn giữa tiêu đề
            "xanchor": "center"
        },
        xaxis=dict(
            title="Année",  # Tiêu đề trục X
            showgrid=False  # Loại bỏ lưới
        ),
        yaxis=dict(
            title="Nombre de patients",  # Tiêu đề trục Y
            showgrid=True  # Hiển thị lưới để dễ nhìn hơn
        )
    )

    # Hiển thị gợi ý ngay trước biểu đồ
    st.markdown("""
    <p style="font-size: 14px; font-style: italic; color: gray;">
    Astuce : Si vous souhaitez zoomer sur l'évolution d'un seul département, veuillez sélectionner le département dans la liste déroulante ci-dessus.
    </p>
    """, unsafe_allow_html=True)

    # Hiển thị biểu đồ
    st.plotly_chart(fig, use_container_width=True)

    # Dọn dẹp dữ liệu sau khi hiển thị
    del department_year_data, department_data
    gc.collect()

    # Các cột cần hiển thị và kiểm tra
    columns_to_display = ["Department Name", "Age Group Label", "Patient Count (top)"]

    if all(col in filtered_staged_data.columns for col in columns_to_display):
        # Lọc, loại bỏ các hàng có "Department Name" là "Hors France Métropolitaine" hoặc "Patient Count (top)" rỗng
        filtered_df_display = (
            filtered_staged_data.loc[
                (filtered_staged_data["Department Name"] != "Hors France Métropolitaine") &  # Loại bỏ dòng không mong muốn
                (filtered_staged_data["Patient Count (top)"].notna())  # Loại bỏ dòng có giá trị rỗng
            ][columns_to_display]
            .drop_duplicates()  # Loại bỏ các dòng trùng lặp
            .sort_values(by=["Department Name", "Patient Count (top)"], ascending=[True, False])  # Sắp xếp theo tên vùng và giá trị bệnh nhân
        )

        # Lọc bỏ các hàng có "Age Group Label" là "tous âges" và tạo bản sao
        filtered_age_data = filtered_df_display.loc[
            filtered_df_display["Age Group Label"] != "tous âges"
        ].copy()

        # Lọc dữ liệu theo Department được chọn
        filtered_age_data_department = filtered_age_data.loc[
            filtered_age_data["Department Name"] == selected_department
        ]

        # Tạo bảng tổng hợp số lượng bệnh nhân theo `Age Group Label`
        age_class_distribution = (
            filtered_age_data_department.groupby("Age Group Label")["Patient Count (top)"]
            .sum()
            .reset_index()
        )

        # Kiểm tra nếu bảng tổng hợp không rỗng
        if not age_class_distribution.empty:
            # Tính tổng số bệnh nhân để tính phần trăm
            total_patients = age_class_distribution["Patient Count (top)"].sum()

            # Thêm cột phần trăm
            age_class_distribution["Percentage"] = (
                age_class_distribution["Patient Count (top)"] / total_patients * 100
            )

            # Lọc bỏ các nhóm tuổi chiếm dưới 0.1%
            filtered_age_class_distribution = age_class_distribution[
                age_class_distribution["Percentage"] >= 0.1
            ]

            # Tạo biểu đồ hình tròn nếu dữ liệu còn lại không rỗng
            if not filtered_age_class_distribution.empty:
                fig_pie = px.pie(
                    filtered_age_class_distribution,
                    names="Age Group Label",  # Cột chứa tên phân lớp tuổi
                    values="Patient Count (top)",  # Cột chứa giá trị số lượng bệnh nhân
                    title=f"<b>Répartition des classes d'âge pour la pathologie sélectionnée </b>",
                    hole=0.4,  # Biểu đồ donut (lỗ giữa)
                )

                # Tùy chỉnh giao diện biểu đồ
                fig_pie.update_traces(
                    textinfo="percent",  # Chỉ hiển thị phần trăm
                    hoverinfo="label+percent+value",  # Hiển thị thông tin khi hover
                    textfont_size=14,  # Tăng kích thước font chữ
                )

                # Tùy chỉnh layout
                fig_pie.update_layout(
                    title=dict(
                        text=f"<b>Répartition des classes d'âge pour la pathologie sélectionnée </b>",
                        x=0.1,  # Căn lề trái tiêu đề
                        font=dict(size=18),  # Tăng kích thước tiêu đề
                    ),
                    showlegend=True,  # Hiển thị legend (chú giải)
                    legend=dict(
                        title="Classe d'âge",  # Tiêu đề của legend
                        orientation="v",  # Đặt legend theo chiều dọc
                        x=1.05,  # Đặt legend sang bên phải
                        y=0.5,  # Căn giữa legend theo chiều dọc
                        font=dict(size=12),  # Tăng kích thước chữ của legend
                    ),
                    margin=dict(t=70, l=50, r=120, b=50),  # Điều chỉnh lề để có chỗ cho legend
                    height=500,  # Tăng chiều cao biểu đồ
                    width=750,  # Tăng chiều rộng biểu đồ để có đủ không gian cho legend
                )

                # Hiển thị gợi ý trước biểu đồ
                st.markdown("""
                <p style="font-size: 14px; font-style: italic; color: gray; text-align: center;">
                Astuce : Survolez les parties du graphique pour voir plus de détails interactifs.
                </p>
                """, unsafe_allow_html=True)

                # Hiển thị biểu đồ trong Streamlit
                st.plotly_chart(fig_pie, use_container_width=False)  # Không tự động chỉnh kích thước theo container

            else:
                st.error("Aucune classe d'âge avec un pourcentage supérieur ou égal à 0.1% n'a été trouvée.")

        else:
            st.error("Les colonnes nécessaires pour générer le graphique ne sont pas disponibles.")

        # Dọn dẹp dữ liệu tạm thời
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

    # Tải và cache dữ liệu
    combined_data = pd.concat(
        [load_and_cache_data(year) for year in range(2015, 2023)], ignore_index=True
    )

    # Tạo session_state
    if combined_data not in st.session_state:
        st.session_state.combined_data = combined_data  # Tạo DataFrame

    # Tạo danh sách các giá trị unique cho "Age Group Label"
    age_groups = (
        combined_data["Age Group Label"]
        .drop_duplicates()  # Loại bỏ các giá trị trùng lặp
        .sort_values()  # Sắp xếp theo thứ tự tăng dần
        .tolist()  # Chuyển sang danh sách
    )

    # Tạo nút chọn cho nhóm tuổi
    selected_age_group = st.selectbox(
        "Choisir un groupe d'âge pour analyser:", 
        options=age_groups, 
        index=0  # Đặt mặc định là giá trị đầu tiên
    )

    # Lọc dữ liệu trong combined_data dựa trên nhóm tuổi được chọn
    filtered_combined_data = combined_data.loc[
        combined_data["Age Group Label"] == selected_age_group
    ].copy()

    # Dọn dẹp danh sách dữ liệu tạm thời
    del combined_data
    gc.collect()

   # Lấy danh sách duy nhất các tên Pathology Level 1 từ dữ liệu đã lọc
    pathology_level_1_list = (
        filtered_combined_data["Pathology Level 1"]
        .drop_duplicates()  # Loại bỏ các giá trị trùng lặp
        .sort_values()  # Sắp xếp theo thứ tự tăng dần
        .reset_index(drop=True)  # Reset chỉ số để hiển thị đẹp hơn
    )

    # Kiểm tra nếu danh sách không rỗng
    if not pathology_level_1_list.empty:
        st.markdown("### Liste des pathologies (Niveau 1)")
        # Hiển thị danh sách dưới dạng bảng
        st.table(pathology_level_1_list.to_frame(name="Pathology Level 1"))
    else:
        st.warning("Aucune pathologie disponible pour le groupe d'âge sélectionné.")

    # Tạo danh sách các giá trị unique cho Pathology Level 1
    pathology_level_1_list = filtered_combined_data["Pathology Level 1"].drop_duplicates().sort_values().tolist()

    # Tạo nút chọn cho Pathology Level 1 với giá trị mặc định là giá trị đầu tiên trong danh sách
    selected_pathology_level_1 = st.selectbox(
        "Choisir la pathologie du niveau 1",
        pathology_level_1_list,
        index=0,  # Đặt mặc định là giá trị đầu tiên
        key="pathology_level_1_select_age"
    )

    # Lọc dữ liệu theo Pathology Level 1
    filtered_df_level_1 = filtered_combined_data[filtered_combined_data["Pathology Level 1"] == selected_pathology_level_1]

    # Tạo danh sách các giá trị unique cho Pathology Level 2, loại bỏ 'nan'
    pathology_level_2_list = (
        filtered_df_level_1["Pathology Level 2"]
        .dropna()  # Loại bỏ các giá trị NaN thật
        .loc[lambda x: x != "nan"]  # Loại bỏ các giá trị chuỗi 'nan'
        .drop_duplicates()  # Loại bỏ các giá trị trùng lặp
        .sort_values()  # Sắp xếp danh sách theo thứ tự tăng dần
        .tolist()  # Chuyển đổi thành danh sách
    )

    # Tạo nút chọn cho Pathology Level 2
    selected_pathology_level_2 = st.selectbox(
        "Choisir la pathologie du niveau 2 (Sous-groupe de pathologies)",
        pathology_level_2_list,
        index=len(pathology_level_2_list) - 1,  # Đặt giá trị cuối làm giá trị mặc định
        key="pathology_level_2_select_departement"
    )

    # Lọc dữ liệu theo Pathology Level 2
    filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1["Pathology Level 2"] == selected_pathology_level_2]

    # Loại bỏ cả NaN và 'nan' khỏi danh sách
    pathology_level_3_list = (
        filtered_df_level_2["Pathology Level 3"]
        .dropna()  # Loại bỏ các giá trị NaN thật
        .loc[lambda x: x != "nan"]  # Loại bỏ các giá trị chuỗi 'nan'
        .drop_duplicates()  # Loại bỏ các giá trị trùng lặp
        .sort_values()  # Sắp xếp danh sách theo thứ tự tăng dần
        .tolist()  # Chuyển đổi thành danh sách
    )

    # Tạo nút chọn cho Pathology Level 3
    selected_pathology_level_3 = st.selectbox(
        "Choisir la pathologie du niveau 3 (Sous-groupe détaillé de pathologies)",
        pathology_level_3_list,
        index=len(pathology_level_3_list) - 1,  # Đặt giá trị cuối làm giá trị mặc định
        key="pathology_level_3_select_departement"
    )

    # Lọc dữ liệu theo Pathology Level 3 và nhóm tuổi
    filtered_data = filtered_df_level_2.loc[
        (filtered_df_level_2["Pathology Level 3"] == selected_pathology_level_3) &
        (filtered_df_level_2["Age Group Label"] == selected_age_group)
    ].copy()

    del filtered_df_level_1, filtered_df_level_2
    gc.collect()

    # Lọc dữ liệu chỉ giữ lại những dòng mà "Patient Count (top)" không phải null
    filtered_data_non_null = filtered_data[filtered_data["Patient Count (top)"].notnull()]
    # Sắp xếp dữ liệu theo cột "Patient Count (top)" giảm dần
    filtered_data_non_null = filtered_data_non_null.sort_values(by="Patient Count (top)", ascending=False)

    # Group by "Department Name" và "Gender Label", tính tổng "Patient Count (top)"
    grouped_data = (
        filtered_data_non_null.groupby(["Department Name", "Gender Label"])["Patient Count (top)"]
        .sum()
        .reset_index()
    )
    
    del filtered_data_non_null
    gc.collect()

    # # Kiểm tra nếu dữ liệu đã lọc có tồn tại dòng nào
    # if not grouped_data.empty:
    #     # Hiển thị bảng dữ liệu đã lọc
    #     st.dataframe(
    #         grouped_data,
    #         use_container_width=True
    #     )
    # else:
    #     # Hiển thị thông báo nếu không có dữ liệu hợp lệ
    #     st.warning("Aucune donnée patient n'existe pour le groupe d'âge et la pathologie sélectionnés.")

    # # Hiển thị bảng tỷ lệ phần trăm
    # st.markdown("### Pourcentage des genres (National)")

    # Tính tổng số bệnh nhân trên cả nước
    total_patients_national = grouped_data["Patient Count (top)"].sum()

    # Tính tổng số bệnh nhân theo giới tính trên cả nước
    national_gender_distribution = (
        grouped_data.groupby("Gender Label")["Patient Count (top)"]
        .sum()
        .reset_index()
    )

    # Thêm cột tỷ lệ phần trăm
    national_gender_distribution["% Gender"] = (
        national_gender_distribution["Patient Count (top)"] / total_patients_national * 100
    )

    # Vẽ biểu đồ tròn
    fig_pie = px.pie(
        national_gender_distribution,
        names="Gender Label",  # Cột chứa tên giới tính
        values="Patient Count (top)",  # Giá trị là số bệnh nhân
        hole=0.4,  # Biểu đồ donut (có lỗ ở giữa)
    )

    # Tùy chỉnh giao diện biểu đồ
    fig_pie.update_traces(
        textinfo="percent+label",  # Hiển thị nhãn và phần trăm
        hoverinfo="label+percent+value",  # Hiển thị thông tin khi hover
    )
    fig_pie.update_layout(
        legend=dict(
            title="Genre",  # Tiêu đề của legend
            orientation="v",  # Đặt legend theo chiều dọc
            x=1.05,  # Đặt legend sang bên phải
            y=0.5,  # Căn giữa legend theo chiều dọc
            font=dict(size=12),  # Tăng kích thước chữ của legend
        ),
        margin=dict(t=70, l=50, r=150, b=50),  # Điều chỉnh lề
        height=400,  # Chiều cao biểu đồ
        width=600,  # Chiều rộng biểu đồ
    )

    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig_pie, use_container_width=False)

    del national_gender_distribution
    gc.collect()

    # Kiểm tra nếu dữ liệu đã lọc có tồn tại dòng nào
    if not grouped_data.empty:
        # Hiển thị bảng dữ liệu đã lọc
        st.dataframe(
            grouped_data, #[["Department Name", "Age Group Label","Gender Label", "Patient Count (top)"]],
            use_container_width=True
        )
    else:
        # Hiển thị thông báo nếu không có dữ liệu hợp lệ
        st.warning("Aucune donnée patient n'existe pour le groupe d'âge et la pathologie sélectionnés.")

    # Phần bản đồ
    map_data = grouped_data[["Department Name", "Patient Count (top)"]].copy()
    map_data = map_data.dropna(subset=["Patient Count (top)"])  # Loại bỏ giá trị NaN

    # Kiểm tra nếu map_data còn dữ liệu
    if map_data.empty:
        st.error("No valid data available after cleaning.")
    else:
        # Đường dẫn tới tệp GeoJSON chứa thông tin biên giới của các vùng
        geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"

        # Tải GeoJSON
        import requests
        response = requests.get(geojson_url)
        if response.status_code != 200:
            st.error("Failed to load GeoJSON data.")
        else:
            geojson_data = response.json()

            # Thêm dữ liệu vào GeoJSON (mapping Department Name -> Patient Count)
            for feature in geojson_data["features"]:
                department_name = feature["properties"]["nom"]  # Thuộc tính 'nom' là tên vùng
                if department_name in map_data["Department Name"].values:
                    # Lấy giá trị duy nhất tương ứng với Department Name
                    patient_count = map_data.loc[
                        map_data["Department Name"] == department_name, "Patient Count (top)"
                    ].iloc[0]
                    feature["properties"]["Patient Count (top)"] = int(patient_count)
                else:
                    feature["properties"]["Patient Count (top)"] = None

            # Tìm giá trị min và max
            min_value = map_data["Patient Count (top)"].min()
            max_value = map_data["Patient Count (top)"].max()

            # Khởi tạo bản đồ trung tâm tại Pháp
            m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

            # Ánh xạ dữ liệu vào GeoJSON
            folium.Choropleth(
                geo_data=geojson_data,
                name="choropleth",
                data=map_data,
                columns=["Department Name", "Patient Count (top)"],  # Dữ liệu ánh xạ
                key_on="feature.properties.nom",  # Thuộc tính trong GeoJSON tương ứng với "Department Name"
                fill_color="YlOrRd",  # Thang màu (vàng đến đỏ)
                fill_opacity=0.7,
                line_opacity=0,
                nan_fill_color="#e1ebf5",  # Đổi màu mặc định cho vùng không có dữ liệu thành xanh dương nhạt
                legend_name="Patient Count (top)",
                threshold_scale=[
                    min_value,
                    min_value + (max_value - min_value) * 0.25,
                    min_value + (max_value - min_value) * 0.5,
                    min_value + (max_value - min_value) * 0.75,
                    max_value,
                ],
            ).add_to(m)

            # Thêm tooltip hiển thị thông tin khi trỏ chuột
            folium.GeoJson(
                geojson_data,
                tooltip=folium.features.GeoJsonTooltip(
                    fields=["nom", "Patient Count (top)"],  # Hiển thị tên vùng và số bệnh nhân
                    aliases=["Department: ", "Patients: "],  # Nhãn hiển thị
                    style="font-size:12px;",  # Kiểu chữ
                    localize=True,
                ),
                
            ).add_to(m)

            # Hiển thị bản đồ trong Streamlit
            st_folium(m, width=800, height=600)

            # Dọn dẹp dữ liệu GeoJSON
            del geojson_data, m, map_data
            gc.collect()


###############################################################################################

elif st.session_state.page == "Sexe":
    st.markdown("""
        <h1 style="color: #00008B; text-align: center; font-size: 30px;">
            Analyse des pathologies par sexe
        </h1>
    """, unsafe_allow_html=True)

    # Tải và cache dữ liệu
    combined_data = pd.concat(
        [load_and_cache_data(year) for year in range(2015, 2023)], ignore_index=True
    )

    # Tạo session_state
    if combined_data not in st.session_state:
        st.session_state.combined_data = combined_data  # Tạo DataFrame


    # Tạo danh sách các giá trị unique
    sex_groups = (
        combined_data["Gender Label"]
        .drop_duplicates()  # Loại bỏ các giá trị trùng lặp
        .sort_values()  # Sắp xếp theo thứ tự tăng dần
        .tolist()  # Chuyển sang danh sách
    )

    # Tạo nút chọn 
    selected_sex_group = st.selectbox(
        "Choisir un sexe pour analyser:", 
        options=sex_groups, 
        index=0  # Đặt mặc định là giá trị đầu tiên
    )

    # Lọc dữ liệu trong combined_data dựa trên nhóm tuổi được chọn
    filtered_combined_data = combined_data.loc[
        combined_data["Gender Label"] == selected_sex_group
    ].copy()

    # Dọn dẹp danh sách dữ liệu tạm thời
    del st.session_state.combined_data, combined_data
    gc.collect()

    # Lấy danh sách duy nhất các tên Pathology Level 1 từ dữ liệu đã lọc
    pathology_level_1_list = (
        filtered_combined_data["Pathology Level 1"]
        .drop_duplicates()  # Loại bỏ các giá trị trùng lặp
        .sort_values()  # Sắp xếp theo thứ tự tăng dần
        .reset_index(drop=True)  # Reset chỉ số để hiển thị đẹp hơn
    )

    # Kiểm tra nếu danh sách không rỗng
    if not pathology_level_1_list.empty:
        st.markdown("### Liste des pathologies (Niveau 1)")
        # Hiển thị danh sách dưới dạng bảng
        st.table(pathology_level_1_list.to_frame(name="Pathology Level 1"))
    else:
        st.warning("Aucune pathologie disponible pour le groupe d'âge sélectionné.")

    # Tạo danh sách các giá trị unique cho Pathology Level 1
    pathology_level_1_list = filtered_combined_data["Pathology Level 1"].drop_duplicates().sort_values().tolist()

    # Tạo nút chọn cho Pathology Level 1 với giá trị mặc định là giá trị đầu tiên trong danh sách
    selected_pathology_level_1 = st.selectbox(
        "Choisir la pathologie du niveau 1",
        pathology_level_1_list,
        index=0,  # Đặt mặc định là giá trị đầu tiên
        key="pathology_level_1_select_age"
    )

    # Lọc dữ liệu theo Pathology Level 1
    filtered_df_level_1 = filtered_combined_data[filtered_combined_data["Pathology Level 1"] == selected_pathology_level_1]

    # Tạo danh sách các giá trị unique cho Pathology Level 2, loại bỏ 'nan'
    pathology_level_2_list = (
        filtered_df_level_1["Pathology Level 2"]
        .dropna()  # Loại bỏ các giá trị NaN thật
        .loc[lambda x: x != "nan"]  # Loại bỏ các giá trị chuỗi 'nan'
        .drop_duplicates()  # Loại bỏ các giá trị trùng lặp
        .sort_values()  # Sắp xếp danh sách theo thứ tự tăng dần
        .tolist()  # Chuyển đổi thành danh sách
    )

    # Tạo nút chọn cho Pathology Level 2
    selected_pathology_level_2 = st.selectbox(
        "Choisir la pathologie du niveau 2 (Sous-groupe de pathologies)",
        pathology_level_2_list,
        index=len(pathology_level_2_list) - 1,  # Đặt giá trị cuối làm giá trị mặc định
        key="pathology_level_2_select_departement"
    )

    # Lọc dữ liệu theo Pathology Level 2
    filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1["Pathology Level 2"] == selected_pathology_level_2]

    # Loại bỏ cả NaN và 'nan' khỏi danh sách
    pathology_level_3_list = (
        filtered_df_level_2["Pathology Level 3"]
        .dropna()  # Loại bỏ các giá trị NaN thật
        .loc[lambda x: x != "nan"]  # Loại bỏ các giá trị chuỗi 'nan'
        .drop_duplicates()  # Loại bỏ các giá trị trùng lặp
        .sort_values()  # Sắp xếp danh sách theo thứ tự tăng dần
        .tolist()  # Chuyển đổi thành danh sách
    )

    # Tạo nút chọn cho Pathology Level 3
    selected_pathology_level_3 = st.selectbox(
        "Choisir la pathologie du niveau 3 (Sous-groupe détaillé de pathologies)",
        pathology_level_3_list,
        index=len(pathology_level_3_list) - 1,  # Đặt giá trị cuối làm giá trị mặc định
        key="pathology_level_3_select_departement"
    )

    # Lọc dữ liệu theo Pathology Level 3 và nhóm tuổi
    filtered_data = filtered_df_level_2.loc[
        (filtered_df_level_2["Pathology Level 3"] == selected_pathology_level_3) &
        (filtered_df_level_2["Gender Label"] == selected_sex_group)
    ].copy()

    del filtered_df_level_1, filtered_df_level_2
    gc.collect()

    # Lọc dữ liệu chỉ giữ lại những dòng mà "Patient Count (top)" không phải null
    filtered_data_non_null = filtered_data[filtered_data["Patient Count (top)"].notnull()]
    # Sắp xếp dữ liệu theo cột "Patient Count (top)" giảm dần
    filtered_data_non_null = filtered_data_non_null.sort_values(by="Patient Count (top)", ascending=False)

    # Group by "Department Name" và "Age Group Label", tính tổng "Patient Count (top)"
    grouped_data = (
        filtered_data_non_null.groupby(["Department Name", "Age Group Label"])["Patient Count (top)"]
        .sum()
        .reset_index()
    )
    
    del filtered_data_non_null
    gc.collect()

    # Tính tổng số bệnh nhân trên cả nước
    total_patients_national = grouped_data["Patient Count (top)"].sum()

    # Tính tổng số bệnh nhân theo giới tính trên cả nước
    national_sex_distribution = (
        grouped_data.groupby("Age Group Label")["Patient Count (top)"]
        .sum()
        .reset_index()
    )

    # Thêm cột tỷ lệ phần trăm
    national_sex_distribution["% Age"] = (
        national_sex_distribution["Patient Count (top)"] / total_patients_national * 100
    )

    # # Tạo một cột mới để phân loại các nhóm tuổi
    # national_sex_distribution['Age Group Category'] = national_sex_distribution['% Age'].apply(
    #     lambda x: 'Others' if float(x.split('%')[0]) < 7 else x
    # )
    # def categorize_age_group(x):
    #     try:
    #         # Try converting to float first
    #         return 'Others' if float(x) < 7 else x
    #     except ValueError:
    #         # If conversion fails (likely a string), try splitting
    #         try:
    #             return 'Others' if float(x.split('%')[0]) < 7 else x
    #         except:
    #             # Handle unexpected values (optional)
    #             return 'Invalid'

    # national_sex_distribution['Age Group Category'] = national_sex_distribution['% Age'].apply(categorize_age_group)

    # Vẽ biểu đồ tròn
    fig_pie = px.pie(
        national_sex_distribution,
        names="Age Group Label",  # Cột chứa tên giới tính
        values="Patient Count (top)",  # Giá trị là số bệnh nhân
        hole=0.4,  # Biểu đồ donut (có lỗ ở giữa)
    )

    # Tùy chỉnh giao diện biểu đồ
    fig_pie.update_traces(
        textinfo="percent",  # Hiển thị nhãn và phần trăm
        hoverinfo="label+percent+value",  # Hiển thị thông tin khi hover
    )
    fig_pie.update_layout(
        legend=dict(
            title="Age",  # Tiêu đề của legend
            orientation="v",  # Đặt legend theo chiều dọc
            x=1.05,  # Đặt legend sang bên phải
            y=0.5,  # Căn giữa legend theo chiều dọc
            font=dict(size=12),  # Tăng kích thước chữ của legend
        ),
        margin=dict(t=70, l=50, r=150, b=50),  # Điều chỉnh lề
        height=400,  # Chiều cao biểu đồ
        width=600,  # Chiều rộng biểu đồ
    )

    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig_pie, use_container_width=False)

    del national_sex_distribution
    gc.collect()

    # Kiểm tra nếu dữ liệu đã lọc có tồn tại dòng nào
    if not grouped_data.empty:
        # Hiển thị bảng dữ liệu đã lọc
        st.dataframe(
            grouped_data,
            use_container_width=True
        )
    else:
        # Hiển thị thông báo nếu không có dữ liệu hợp lệ
        st.warning("Aucune donnée patient n'existe pour le groupe d'âge et la pathologie sélectionnés.")

    # Phần bản đồ
    map_data = grouped_data[["Department Name", "Patient Count (top)"]].copy()
    map_data = map_data.dropna(subset=["Patient Count (top)"])  # Loại bỏ giá trị NaN

    # Kiểm tra nếu map_data còn dữ liệu
    if map_data.empty:
        st.error("No valid data available after cleaning.")
    else:
        # Đường dẫn tới tệp GeoJSON chứa thông tin biên giới của các vùng
        geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"

        # Tải GeoJSON
        import requests
        response = requests.get(geojson_url)
        if response.status_code != 200:
            st.error("Failed to load GeoJSON data.")
        else:
            geojson_data = response.json()

            # Thêm dữ liệu vào GeoJSON (mapping Department Name -> Patient Count)
            for feature in geojson_data["features"]:
                department_name = feature["properties"]["nom"]  # Thuộc tính 'nom' là tên vùng
                if department_name in map_data["Department Name"].values:
                    # Lấy giá trị duy nhất tương ứng với Department Name
                    patient_count = map_data.loc[
                        map_data["Department Name"] == department_name, "Patient Count (top)"
                    ].iloc[0]
                    feature["properties"]["Patient Count (top)"] = int(patient_count)
                else:
                    feature["properties"]["Patient Count (top)"] = None

            # Tìm giá trị min và max
            min_value = map_data["Patient Count (top)"].min()
            max_value = map_data["Patient Count (top)"].max()

            # Khởi tạo bản đồ trung tâm tại Pháp
            m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

            # Ánh xạ dữ liệu vào GeoJSON
            folium.Choropleth(
                geo_data=geojson_data,
                name="choropleth",
                data=map_data,
                columns=["Department Name", "Patient Count (top)"],  # Dữ liệu ánh xạ
                key_on="feature.properties.nom",  # Thuộc tính trong GeoJSON tương ứng với "Department Name"
                fill_color="YlOrRd",  # Thang màu (vàng đến đỏ)
                fill_opacity=0.7,
                line_opacity=0,
                nan_fill_color="#e1ebf5",  # Đổi màu mặc định cho vùng không có dữ liệu thành xanh dương nhạt
                legend_name="Patient Count (top)",
                threshold_scale=[
                    min_value,
                    min_value + (max_value - min_value) * 0.25,
                    min_value + (max_value - min_value) * 0.5,
                    min_value + (max_value - min_value) * 0.75,
                    max_value,
                ],
            ).add_to(m)

            # Thêm tooltip hiển thị thông tin khi trỏ chuột
            folium.GeoJson(
                geojson_data,
                tooltip=folium.features.GeoJsonTooltip(
                    fields=["nom", "Patient Count (top)"],  # Hiển thị tên vùng và số bệnh nhân
                    aliases=["Department: ", "Patients: "],  # Nhãn hiển thị
                    style="font-size:12px;",  # Kiểu chữ
                    localize=True,
                ),
                
            ).add_to(m)

            # Hiển thị bản đồ trong Streamlit
            st_folium(m, width=800, height=600)

            # Dọn dẹp dữ liệu GeoJSON
            del geojson_data, m, map_data
            gc.collect()

