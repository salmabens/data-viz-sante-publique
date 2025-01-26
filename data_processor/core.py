import pandas as pd
import os
import gc
import datetime

# Dictionary of region codes with their names

region_names = {
    1: "Guadeloupe",
    2: "Martinique",
    3: "Guyane",
    4: "La Réunion",
    6: "Mayotte",
    11: "Île-de-France",
    24: "Centre-Val de Loire",
    27: "Bourgogne-Franche-Comté",
    28: "Normandie",
    32: "Hauts-de-France",
    44: "Grand Est",
    52: "Pays de la Loire",
    53: "Bretagne",
    75: "Nouvelle-Aquitaine",
    76: "Occitanie",
    84: "Auvergne-Rhône-Alpes",
    93: "Provence-Alpes-Côte d'Azur",
    94: "Corse"
}


# Dictionaries of latitudes and longitudes for each region of France

latitudes_region = {
    "Île-de-France": 48.8566,
    "Champagne-Ardenne": 49.0,
    "Haute-Normandie": 49.4,
    "Bretagne": 48.6,
    "Poitou-Charentes": 46.5,
    "Rhône-Alpes": 45.7,
    "Nouvelle-Aquitaine": 44.0,
    "Languedoc-Roussillon": 43.5,
    "Midi-Pyrénées": 43.5,
    "Provence-Alpes-Côte d'Azur": 43.5,
    "Alsace": 48.5,
    "Lorraine": 48.7,
    "Île-de-France (Paris)": 48.8566,
    "Haute-Normandie (again)": 49.4,
    "Provence-Alpes-Côte d'Azur (again)": 43.5,
    "Rhône-Alpes (again)": 45.7,
    "Alsace (again)": 48.5,
    "Non renseigné / Collectivités d'Outre-Mer": None  
}

longitudes_region = {
    "Île-de-France": 2.3522,
    "Champagne-Ardenne": 4.0,
    "Haute-Normandie": 1.1,
    "Bretagne": -2.0,
    "Poitou-Charentes": -0.5,
    "Rhône-Alpes": 4.9,
    "Nouvelle-Aquitaine": -0.5,
    "Languedoc-Roussillon": 3.5,
    "Midi-Pyrénées": 1.5,
    "Provence-Alpes-Côte d'Azur": 6.0,
    "Alsace": 7.5,
    "Lorraine": 6.2,
    "Île-de-France (Paris)": 2.3522,
    "Haute-Normandie (again)": 1.1,
    "Provence-Alpes-Côte d'Azur (again)": 6.0,
    "Rhône-Alpes (again)": 4.9,
    "Alsace (again)": 7.5,
    "Non renseigné / Collectivités d'Outre-Mer": None  
}

# Dictionaries of latitudes and longitudes for each department of France

latitudes_dept = {
    "Ain": 46.0333,
    "Aisne": 49.5667,
    "Allier": 46.5667,
    "Alpes-de-Haute-Provence": 44.0,
    "Hautes-Alpes": 44.6667,
    "Alpes-Maritimes": 43.7,
    "Ardèche": 44.75,
    "Ardennes": 49.75,
    "Ariège": 43.0,
    "Aube": 48.3,
    "Aude": 43.1,
    "Aveyron": 44.35,
    "Bouches-du-Rhône": 43.4,
    "Calvados": 49.1833,
    "Cantal": 45.0333,
    "Charente": 45.65,
    "Charente-Maritime": 45.75,
    "Cher": 47.0833,
    "Corrèze": 45.25,
    "Corse-du-Sud": 41.85,
    "Haute-Corse": 42.45,
    "Côte-d'Or": 47.3167,
    "Côtes-d'Armor": 48.5167,
    "Creuse": 46.1667,
    "Dordogne": 45.1833,
    "Doubs": 47.25,
    "Drôme": 44.6667,
    "Eure": 49.0667,
    "Eure-et-Loir": 48.4667,
    "Finistère": 48.3833,
    "Gard": 44.1333,
    "Haute-Garonne": 43.6,
    "Gers": 43.65,
    "Gironde": 44.85,
    "Hérault": 43.5,
    "Ille-et-Vilaine": 48.1167,
    "Indre": 46.9333,
    "Indre-et-Loire": 47.3833,
    "Isère": 45.3333,
    "Jura": 46.6667,
    "Landes": 43.9,
    "Loir-et-Cher": 47.5833,
    "Loire": 45.5833,
    "Haute-Loire": 45.05,
    "Loire-Atlantique": 47.3,
    "Loiret": 47.9167,
    "Lot": 44.6667,
    "Lot-et-Garonne": 44.4167,
    "Lozère": 44.5167,
    "Maine-et-Loire": 47.4667,
    "Manche": 49.05,
    "Marne": 49.0833,
    "Haute-Marne": 48.15,
    "Mayenne": 48.3,
    "Meurthe-et-Moselle": 48.7,
    "Meuse": 49.0,
    "Morbihan": 47.75,
    "Moselle": 49.1,
    "Nièvre": 47.0,
    "Nord": 50.6333,
    "Oise": 49.4333,
    "Orne": 48.6,
    "Pas-de-Calais": 50.4667,
    "Puy-de-Dôme": 45.7667,
    "Pyrénées-Atlantiques": 43.3333,
    "Hautes-Pyrénées": 43.0833,
    "Pyrénées-Orientales": 42.7,
    "Bas-Rhin": 48.5833,
    "Haut-Rhin": 47.75,
    "Rhône": 45.75,
    "Haute-Saône": 47.6667,
    "Saône-et-Loire": 46.6667,
    "Sarthe": 48.0,
    "Savoie": 45.5,
    "Haute-Savoie": 46.0833,
    "Paris": 48.8566,
    "Seine-Maritime": 49.4667,
    "Seine-et-Marne": 48.5333,
    "Yvelines": 48.8,
    "Deux-Sèvres": 46.35,
    "Somme": 49.9167,
    "Tarn": 43.9,
    "Tarn-et-Garonne": 44.0667,
    "Var": 43.5,
    "Vaucluse": 44.0,
    "Vendée": 46.75,
    "Vienne": 46.5833,
    "Haute-Vienne": 45.8333,
    "Vosges": 48.2,
    "Yonne": 47.8333,
    "Territoire de Belfort": 47.65,
    "Essonne": 48.6333,
    "Hauts-de-Seine": 48.8833,
    "Seine-Saint-Denis": 48.9333,
    "Val-de-Marne": 48.7833,
    "Val-d'Oise": 49.05,
    "Non renseigné / Collectivités d'Outre-Mer": None  
}

longitudes_dept = {
    "Ain": 5.35,
    "Aisne": 3.6167,
    "Allier": 3.3333,
    "Alpes-de-Haute-Provence": 6.2333,
    "Hautes-Alpes": 6.3333,
    "Alpes-Maritimes": 7.25,
    "Ardèche": 4.4167,
    "Ardennes": 4.75,
    "Ariège": 1.6167,
    "Aube": 4.05,
    "Aude": 2.35,
    "Aveyron": 2.5667,
    "Bouches-du-Rhône": 5.35,
    "Calvados": -0.3667,
    "Cantal": 2.55,
    "Charente": 0.1667,
    "Charente-Maritime": -1.0333,
    "Cher": 2.4,
    "Corrèze": 1.7667,
    "Corse-du-Sud": 8.75,
    "Haute-Corse": 9.1667,
    "Côte-d'Or": 4.8667,
    "Côtes-d'Armor": -2.85,
    "Creuse": 1.95,
    "Dordogne": 0.7167,
    "Doubs": 6.3333,
    "Drôme": 5.05,
    "Eure": 1.15,
    "Eure-et-Loir": 1.35,
    "Finistère": -4.1167,
    "Gard": 4.1333,
    "Haute-Garonne": 1.45,
    "Gers": 0.6,
    "Gironde": -0.5667,
    "Hérault": 3.8333,
    "Ille-et-Vilaine": -1.6833,
    "Indre": 1.55,
    "Indre-et-Loire": 0.6833,
    "Isère": 5.5667,
    "Jura": 5.75,
    "Landes": -0.7667,
    "Loir-et-Cher": 1.3333,
    "Loire": 4.3167,
    "Haute-Loire": 3.5667,
    "Loire-Atlantique": -1.5667,
    "Loiret": 2.2,
    "Lot": 1.4333,
    "Lot-et-Garonne": 0.6167,
    "Lozère": 3.5,
    "Maine-et-Loire": -0.55,
    "Manche": -1.3833,
    "Marne": 4.2333,
    "Haute-Marne": 5.3333,
    "Mayenne": -0.6167,
    "Meurthe-et-Moselle": 6.1667,
    "Meuse": 5.3667,
    "Morbihan": -2.8333,
    "Moselle": 6.3333,
    "Nièvre": 3.5,
    "Nord": 3.0667,
    "Oise": 2.7,
    "Orne": 0.0167,
    "Pas-de-Calais": 2.5,
    "Puy-de-Dôme": 3.0833,
    "Pyrénées-Atlantiques": -0.6833,
    "Hautes-Pyrénées": 0.1333,
    "Pyrénées-Orientales": 2.8667,
    "Bas-Rhin": 7.75,
    "Haut-Rhin": 7.3333,
    "Rhône": 4.8333,
    "Haute-Saône": 6.05,
    "Saône-et-Loire": 4.3833,
    "Sarthe": 0.2,
    "Savoie": 6.3333,
    "Haute-Savoie": 6.4,
    "Paris": 2.3522,
    "Seine-Maritime": 0.9667,
    "Seine-et-Marne": 2.9167,
    "Yvelines": 1.8167,
    "Deux-Sèvres": -0.2333,
    "Somme": 2.3,
    "Tarn": 2.15,
    "Tarn-et-Garonne": 1.3667,
    "Var": 6.2167,
    "Vaucluse": 5.1667,
    "Vendée": -1.4167,
    "Vienne": 0.3333,
    "Haute-Vienne": 1.3333,
    "Vosges": 6.3333,
    "Yonne": 3.5667,
    "Territoire de Belfort": 6.8667,
    "Essonne": 2.25,
    "Hauts-de-Seine": 2.2333,
    "Seine-Saint-Denis": 2.45,
    "Val-de-Marne": 2.4667,
    "Val-d'Oise": 2.2167,
    "Non renseigné / Collectivités d'Outre-Mer": None  
}


# Creation of a dictionary for French departments
department_names = {
    "01": "Ain",
    "02": "Aisne",
    "03": "Allier",
    "04": "Alpes-de-Haute-Provence",
    "05": "Hautes-Alpes",
    "06": "Alpes-Maritimes",
    "07": "Ardèche",
    "08": "Ardennes",
    "09": "Ariège",
    "10": "Aube",
    "11": "Aude",
    "12": "Aveyron",
    "13": "Bouches-du-Rhône",
    "14": "Calvados",
    "15": "Cantal",
    "16": "Charente",
    "17": "Charente-Maritime",
    "18": "Cher",
    "19": "Corrèze",
    "2A": "Corse-du-Sud",
    "2B": "Haute-Corse",
    "21": "Côte-d'Or",
    "22": "Côtes-d'Armor",
    "23": "Creuse",
    "24": "Dordogne",
    "25": "Doubs",
    "26": "Drôme",
    "27": "Eure",
    "28": "Eure-et-Loir",
    "29": "Finistère",
    "30": "Gard",
    "31": "Haute-Garonne",
    "32": "Gers",
    "33": "Gironde",
    "34": "Hérault",
    "35": "Ille-et-Vilaine",
    "36": "Indre",
    "37": "Indre-et-Loire",
    "38": "Isère",
    "39": "Jura",
    "40": "Landes",
    "41": "Loir-et-Cher",
    "42": "Loire",
    "43": "Haute-Loire",
    "44": "Loire-Atlantique",
    "45": "Loiret",
    "46": "Lot",
    "47": "Lot-et-Garonne",
    "48": "Lozère",
    "49": "Maine-et-Loire",
    "50": "Manche",
    "51": "Marne",
    "52": "Haute-Marne",
    "53": "Mayenne",
    "54": "Meurthe-et-Moselle",
    "55": "Meuse",
    "56": "Morbihan",
    "57": "Moselle",
    "58": "Nièvre",
    "59": "Nord",
    "60": "Oise",
    "61": "Orne",
    "62": "Pas-de-Calais",
    "63": "Puy-de-Dôme",
    "64": "Pyrénées-Atlantiques",
    "65": "Hautes-Pyrénées",
    "66": "Pyrénées-Orientales",
    "67": "Bas-Rhin",
    "68": "Haut-Rhin",
    "69": "Rhône",
    "70": "Haute-Saône",
    "71": "Saône-et-Loire",
    "72": "Sarthe",
    "73": "Savoie",
    "74": "Haute-Savoie",
    "75": "Paris",
    "76": "Seine-Maritime",
    "77": "Seine-et-Marne",
    "78": "Yvelines",
    "79": "Deux-Sèvres",
    "80": "Somme",
    "81": "Tarn",
    "82": "Tarn-et-Garonne",
    "83": "Var",
    "84": "Vaucluse",
    "85": "Vendée",
    "86": "Vienne",
    "87": "Haute-Vienne",
    "88": "Vosges",
    "89": "Yonne",
    "90": "Territoire de Belfort",
    "91": "Essonne",
    "92": "Hauts-de-Seine",
    "93": "Seine-Saint-Denis",
    "94": "Val-de-Marne",
    "95": "Val-d'Oise",
    "971": "Guadeloupe",
    "972": "Martinique",
    "973": "Guyane",
    "974": "La Réunion",
    "976": "Mayotte",
    "999": "Hors France Métropolitaine"
}

genders = {
    1 : "Homme",
    2 : "Femme",
    9 : "Tous sexes" 
}

pathologies_level1_short_names = {
    "Maladies cardioneurovasculaires": "Cardio-neurovasc.",
    "Cancers": "Cancers",
    "Maladies inflammatoires ou rares ou infection VIH": "Inflamm./rares/VIH",
    "Maladies neurologiques": "Neurologiques",
    "Maladies psychiatriques": "Psychiatriques",
    "Traitements psychotropes (hors pathologies)": "Psychotropes",
    "Insuffisance rénale chronique terminale": "Insuff. rénale",
    "Traitements du risque vasculaire (hors pathologies)": "Risque vasculaire",
    "Affections de longue durée (dont 31 et 32) pour d'autres causes": "ALD autres causes",
    "Diabète": "Diabète",
    "Hospitalisation pour Covid-19": "Covid-19",
    "Hospitalisations hors pathologies repérées (avec ou sans pathologies, traitements ou maternité)": "Hospit. hors pathologies",
    "Maladies du foie ou du pancréas (hors mucoviscidose)": "Foie/pancréas",
    "Maladies respiratoires chroniques (hors mucoviscidose)": "Respiratoires chroniques",
    "Pas de pathologie repérée, traitement, maternité, hospitalisation ou traitement antalgique ou anti-inflammatoire": "Aucune pathologie",
    "Total consommants tous régimes": "Total consommateurs",
    "Traitement antalgique ou anti-inflammatoire (hors pathologies, traitements, maternité ou hospitalisations)": "Antalgiques/anti-inflam.",
    "Maternité (avec ou sans pathologies)": "Maternité"
}

pathologies_level2_short_names = {
    "Maladies inflammatoires chroniques": "Inflamm. chroniques",
    "Maladies rares": "Rares",
    "Accident vasculaire cérébral": "AVC",
    "Autres cancers": "Autres cancers",
    "Cancer bronchopulmonaire": "Cancer pulmonaire",
    "Cancer colorectal": "Cancer colorectal",
    "Insuffisance cardiaque": "Insuff. cardiaque",
    "Maladie coronaire": "Coronaires",
    "Cancer de la prostate": "Cancer prostate",
    "Cancer du sein de la femme": "Cancer sein (F)",
    "Affections de longue durée (dont 31 et 32) pour d'autres causes": "ALD autres causes",
    "Artériopathie périphérique": "Artériopathie",
    "Autres affections cardiovasculaires": "Autres cardio.",
    "Autres affections neurologiques": "Autres neuro.",
    "Autres troubles psychiatriques": "Autres psychiat.",
    "Diabète": "Diabète",
    "Dialyse chronique": "Dialyse",
    "Déficience mentale": "Déficience mentale",
    "Démences (dont maladie d'Alzheimer)": "Démences/Alzheimer",
    "Embolie pulmonaire": "Embolie pulmonaire",
    "Hospitalisation pour Covid-19": "Covid-19",
    "Hospitalisations hors pathologies repérées (avec ou sans pathologies, traitements ou maternité)": "Hospit. hors pathologies",
    "Infection par le VIH": "VIH",
    "Lésion médullaire": "Lésion médullaire",
    "Maladie de Parkinson": "Parkinson",
    "Maladie valvulaire": "Valvulopathies",
    "Maladies du foie ou du pancréas (hors mucoviscidose)": "Foie/pancréas",
    "Maladies respiratoires chroniques (hors mucoviscidose)": "Respir. chroniques",
    "Myopathie ou myasthénie": "Myopathies",
    "Pas de pathologie repérée, traitement, maternité, hospitalisation ou traitement antalgique ou anti-inflammatoire": "Aucune pathologie",
    "Sclérose en plaques": "Sclérose en plaques",
    "Suivi de transplantation rénale": "Suivi transpl. rénale",
    "Total consommants tous régimes": "Total consommateurs",
    "Traitement antalgique ou anti-inflammatoire (hors pathologies, traitements, maternité ou hospitalisations)": "Antalgiques/anti-inflam.",
    "Traitements antidépresseurs ou régulateurs de l'humeur (hors pathologies)": "Antidépresseurs",
    "Traitements antihypertenseurs (hors pathologies)": "Antihypertenseurs",
    "Traitements anxiolytiques (hors pathologies)": "Anxiolytiques",
    "Traitements hypnotiques (hors pathologies)": "Hypnotiques",
    "Traitements hypolipémiants (hors pathologies)": "Hypolipémiants",
    "Traitements neuroleptiques (hors pathologies)": "Neuroleptiques",
    "Transplantation rénale": "Transpl. rénale",
    "Troubles addictifs": "Addictions",
    "Troubles du rythme ou de la conduction cardiaque": "Rythme/conduction card.",
    "Troubles névrotiques et de l'humeur": "Névroses/humeur",
    "Troubles psychiatriques débutant dans l'enfance": "Psychiatrie enfant",
    "Troubles psychotiques": "Psychotiques",
    "Épilepsie": "Épilepsie",
    "Maternité (avec ou sans pathologies)": "Maternité"
}


pathologies_level3_short_names = {
    "Accident vasculaire cérébral aigu": "AVC aigu",
    "Affections de longue durée (dont 31 et 32) pour d'autres causes": "ALD autres causes",
    "Artériopathie périphérique": "Artériopathie",
    "Autres affections cardiovasculaires": "Autres cardio.",
    "Autres affections neurologiques": "Autres neuro.",
    "Autres cancers actifs": "Cancers actifs (autres)",
    "Autres cancers sous surveillance": "Cancers sous surv. (autres)",
    "Autres maladies inflammatoires chroniques": "Inflamm. chroniques (autres)",
    "Autres troubles psychiatriques": "Psychiatrie (autres)",
    "Cancer bronchopulmonaire actif": "Cancer pulmonaire actif",
    "Cancer bronchopulmonaire sous surveillance": "Cancer pulm. sous surv.",
    "Cancer colorectal actif": "Cancer colorectal actif",
    "Cancer colorectal sous surveillance": "Cancer colorectal sous surv.",
    "Diabète": "Diabète",
    "Dialyse chronique": "Dialyse",
    "Déficience mentale": "Déficience mentale",
    "Démences (dont maladie d'Alzheimer)": "Démences/Alzheimer",
    "Embolie pulmonaire": "Embolie pulmonaire",
    "Hospitalisation pour Covid-19": "Covid-19",
    "Hospitalisations hors pathologies repérées (avec ou sans pathologies, traitements ou maternité)": "Hospit. hors pathologies",
    "Hémophilie ou troubles de l'hémostase graves": "Hémophilie",
    "Infection par le VIH": "VIH",
    "Insuffisance cardiaque aiguë": "Insuff. cardiaque aiguë",
    "Insuffisance cardiaque chronique": "Insuff. cardiaque chronique",
    "Lésion médullaire": "Lésion médullaire",
    "Maladie coronaire chronique": "Coronaires chroniques",
    "Maladie de Parkinson": "Parkinson",
    "Maladie valvulaire": "Valvulopathies",
    "Maladies du foie ou du pancréas (hors mucoviscidose)": "Foie/pancréas",
    "Maladies inflammatoires chroniques intestinales": "Inflamm. chroniques intest.",
    "Maladies métaboliques héréditaires ou amylose": "Métabolique/amylose",
    "Maladies respiratoires chroniques (hors mucoviscidose)": "Respir. chroniques",
    "Mucoviscidose": "Mucoviscidose",
    "Myopathie ou myasthénie": "Myopathies",
    "Pas de pathologie repérée, traitement, maternité, hospitalisation ou traitement antalgique ou anti-inflammatoire": "Aucune pathologie",
    "Polyarthrite rhumatoïde ou maladies apparentées": "Polyarthrite",
    "Sclérose en plaques": "Sclérose en plaques",
    "Spondylarthrite ankylosante ou maladies apparentées": "Spondylarthrite",
    "Suivi de transplantation rénale": "Suivi transpl. rénale",
    "Syndrome coronaire aigu": "Syndrome coron. aigu",
    "Séquelle d'accident vasculaire cérébral": "Séquelle AVC",
    "Total consommants tous régimes": "Total consommateurs",
    "Traitement antalgique ou anti-inflammatoire (hors pathologies, traitements, maternité ou hospitalisations)": "Antalgiques/anti-inflam.",
    "Traitements antidépresseurs ou régulateurs de l'humeur (hors pathologies)": "Antidépresseurs",
    "Traitements antihypertenseurs (hors pathologies)": "Antihypertenseurs",
    "Traitements anxiolytiques (hors pathologies)": "Anxiolytiques",
    "Traitements hypnotiques (hors pathologies)": "Hypnotiques",
    "Traitements hypolipémiants (hors pathologies)": "Hypolipémiants",
    "Traitements neuroleptiques (hors pathologies)": "Neuroleptiques",
    "Transplantation rénale": "Transpl. rénale",
    "Troubles addictifs": "Addictions",
    "Troubles du rythme ou de la conduction cardiaque": "Rythme/conduction card.",
    "Troubles névrotiques et de l'humeur": "Névroses/humeur",
    "Troubles psychiatriques débutant dans l'enfance": "Psychiatrie enfant",
    "Troubles psychotiques": "Psychotiques",
    "Épilepsie": "Épilepsie",
    "Cancer de la prostate actif": "Cancer prostate actif",
    "Cancer de la prostate sous surveillance": "Cancer prostate sous surv.",
    "Cancer du sein de la femme actif": "Cancer sein (F) actif",
    "Cancer du sein de la femme sous surveillance": "Cancer sein (F) sous surv.",
    "Maternité (avec ou sans pathologies)": "Maternité"
}


# Create the 'data' folder at the beginning of the script
print("Create the folder 'Data'...")
os.makedirs("../data", exist_ok=True)

current_year = 2024
staged_file_path = f"../archived/staged/staged_data_{current_year}.csv"

# Load the data from the staged_data.csv file
print("Loading staged data...")
staged_data = pd.read_csv(staged_file_path, sep=",", header=0, skipinitialspace=True)
staged_data = staged_data.drop_duplicates()
# staged_data = staged_data[staged_data["Region"] != 99]
staged_data = staged_data.loc[
    (staged_data["Gender Label"] != "tous sexes") &
    (staged_data["Age Group Label"] != "tous âges") &
    (staged_data["Department"] != 999) &
    (staged_data["Region"] != 99)
]

# Get the unique years in staged_data
unique_years = staged_data['Year'].unique()

# Create a loop to process each year
for year in unique_years:
    # Filter data by year
    staged_data_year = staged_data[staged_data['Year'] == year]
    staged_data_year["Region Name"] = staged_data_year["Region"].map(region_names)
    staged_data_year['Department Name'] = staged_data_year['Department'].map(department_names)
    # Save staged_data for the specific year
    staged_data_year.to_csv(f"../data/staged_data_{year}.csv", index=False, encoding="utf-8")
        
    # Calculate indicators and specific distributions for each year
    # Patients by region and Pathology Level 1 - Pathology Level 2 - Pathology Level 3
    patients_by_region_pathology = staged_data_year.groupby(["Region", "Pathology Level 1", "Pathology Level 2", "Pathology Level 3"])["Patient Count (top)"].sum().reset_index()
    # Add region columns
    patients_by_region_pathology["Region Name"] = patients_by_region_pathology["Region"].map(region_names)
    patients_by_region_pathology["Latitude Région"] = patients_by_region_pathology["Region Name"].map(latitudes_region)
    patients_by_region_pathology["Longitude Région"] = patients_by_region_pathology["Region Name"].map(longitudes_region)
    patients_by_region_pathology['Pathology Level 1 Name'] = patients_by_region_pathology['Pathology Level 1'].map(pathologies_level1_short_names)
    patients_by_region_pathology['Pathology Level 2 Name'] = patients_by_region_pathology['Pathology Level 2'].map(pathologies_level2_short_names)
    patients_by_region_pathology['Pathology Level 3 Name'] = patients_by_region_pathology['Pathology Level 3'].map(pathologies_level3_short_names)
    # Export to a CSV file
    patients_by_region_pathology.to_csv(f"../data/patients_by_region_pathology_{year}.csv", index=False, encoding="utf-8")

    del patients_by_region_pathology
    gc.collect()

    # Patients by department and Pathology Level 1 - Pathology Level 2 - Pathology Level 3
    patients_by_department_pathology = staged_data_year.groupby(["Department", "Pathology Level 1", "Pathology Level 2", "Pathology Level 3"])["Patient Count (top)"].sum().reset_index()
    # Add department columns
    patients_by_department_pathology['Department Name'] = patients_by_department_pathology['Department'].map(department_names)
    patients_by_department_pathology["Latitude Department"] = patients_by_department_pathology["Department Name"].map(latitudes_dept)
    patients_by_department_pathology["Longitude Department"] = patients_by_department_pathology["Department Name"].map(longitudes_dept)
    patients_by_department_pathology['Pathology Level 1 Name'] = patients_by_department_pathology['Pathology Level 1'].map(pathologies_level1_short_names)
    patients_by_department_pathology['Pathology Level 2 Name'] = patients_by_department_pathology['Pathology Level 2'].map(pathologies_level2_short_names)
    patients_by_department_pathology['Pathology Level 3 Name'] = patients_by_department_pathology['Pathology Level 3'].map(pathologies_level3_short_names)
    # Export to a CSV file
    patients_by_department_pathology.to_csv(f"../data/patients_by_department_pathology_{year}.csv", index=False, encoding="utf-8")

    del patients_by_department_pathology
    gc.collect()

    # Patients by gender and Pathology Level 1 - Pathology Level 2 - Pathology Level 3
    patients_by_sexe_pathology = staged_data_year.groupby(["Gender", "Gender Label", "Pathology Level 1", "Pathology Level 2", "Pathology Level 3"])["Patient Count (top)"].sum().reset_index()
    patients_by_sexe_pathology['Pathology Level 1 Name'] = patients_by_sexe_pathology['Pathology Level 1'].map(pathologies_level1_short_names)
    patients_by_sexe_pathology['Pathology Level 2 Name'] = patients_by_sexe_pathology['Pathology Level 2'].map(pathologies_level2_short_names)
    patients_by_sexe_pathology['Pathology Level 3 Name'] = patients_by_sexe_pathology['Pathology Level 3'].map(pathologies_level3_short_names)
    patients_by_sexe_pathology.to_csv(f"../data/patients_by_sexe_pathology_{year}.csv", index=False, encoding="utf-8")

    del patients_by_sexe_pathology
    gc.collect()

    # Patients by age group and Pathology Level 1 - Pathology Level 2 - Pathology Level 
    patients_by_age_group_pathology = staged_data_year.groupby(["Age Group (5 years)", "Age Group Label", "Pathology Level 1", "Pathology Level 2", "Pathology Level 3"])["Patient Count (top)"].sum().reset_index()
    # Mapping age group and pathology levels with their names
    patients_by_age_group_pathology['Pathology Level 1 Name'] = patients_by_age_group_pathology['Pathology Level 1'].map(pathologies_level1_short_names)
    patients_by_age_group_pathology['Pathology Level 2 Name'] = patients_by_age_group_pathology['Pathology Level 2'].map(pathologies_level2_short_names)
    patients_by_age_group_pathology['Pathology Level 3 Name'] = patients_by_age_group_pathology['Pathology Level 3'].map(pathologies_level3_short_names)
    # Exporting the result to a CSV file
    patients_by_age_group_pathology.to_csv(f"../data/patients_by_age_group_pathology_{year}.csv", index=False, encoding="utf-8")

    del patients_by_age_group_pathology, staged_data_year
    gc.collect()

print("All data processed and saved in the folder 'data'.")
