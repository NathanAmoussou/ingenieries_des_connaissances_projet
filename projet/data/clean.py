import pandas as pd
import json
import re
import unidecode  # Pense à faire: pip install unidecode

# --- FONCTIONS DE NETTOYAGE ---

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # 1. Mettre en minuscule
    text = text.lower()
    # 2. Supprimer tout ce qui est entre parenthèses (ex: "Mumbai (Bombay)" -> "Mumbai")
    text = re.sub(r'\s*\(.*?\)', '', text)
    # 3. Supprimer ce qui suit une virgule (ex: "Yulin, Guangxi" -> "Yulin")
    text = text.split(',')[0]
    # 4. Enlever les accents (ex: "København" -> "kobenhavn", "Hérault" -> "herault")
    text = unidecode.unidecode(text)
    # 5. Remplacer les espaces et tirets par underscore
    text = re.sub(r'[\s\-]+', '_', text)
    # 6. Supprimer les caractères spéciaux restants (garder a-z, 0-9, _)
    text = re.sub(r'[^a-z0-9_]', '', text)
    return text.strip('_')

# Dictionnaire de correction manuelle pour les pays (à compléter si besoin)
COUNTRY_MAPPING = {
    "turkiye": "turkey",
    "iran_islamic_republic_of": "iran",
    "united_states_of_america": "usa",
    "united_states": "usa",
    "korea_republic_of": "south_korea",
    "viet_nam": "vietnam",
    "russia": "russian_federation" # Vérifie lequel est dans le JSON !
}

def get_join_key(country, city):
    # Nettoyer d'abord
    c_clean = clean_text(country)
    cit_clean = clean_text(city)
    
    # Appliquer le mapping pays si nécessaire
    if c_clean in COUNTRY_MAPPING:
        c_clean = COUNTRY_MAPPING[c_clean]
        
    return c_clean, cit_clean

# --- 1. TRAITEMENT DU CSV (Green Data) ---
print("Traitement du CSV...")
df = pd.read_csv('green_areas_cleaned.csv') # Remplace par ton vrai nom de fichier

# Créer les colonnes de jointure propres
df['country_join'] = df.apply(lambda row: get_join_key(row['Country or Territory Name'], row['City Name'])[0], axis=1)
df['city_join']    = df.apply(lambda row: get_join_key(row['Country or Territory Name'], row['City Name'])[1], axis=1)

df.to_csv('clean_green.csv', index=False)
print("-> clean_green.csv généré !")

# --- 2. TRAITEMENT DU JSON (Pollution Data) ---
print("Traitement du JSON...")
with open('pollution.json', 'r', encoding='utf-8') as f: # Remplace par ton vrai nom
    data = json.load(f)

measurements = data.get('measurements', [])

for m in measurements:
    raw_country = m.get('country_name', '')
    raw_city = m.get('city_name', '')
    
    c_join, cit_join = get_join_key(raw_country, raw_city)
    
    # On ajoute ces clés directement dans l'objet JSON pour RML
    m['country_join'] = c_join
    m['city_join'] = cit_join

with open('clean_pollution.json', 'w', encoding='utf-8') as f:
    json.dump({"measurements": measurements}, f, indent=2)

print("-> clean_pollution.json généré !")
print("Terminé. Utilisez 'country_join' et 'city_join' dans votre RML.")

# --- 3. ANALYSE DES CORRESPONDANCES (A ajouter à la fin) ---

# Récupérer l'ensemble des clés (Pays, Ville) du CSV nettoyé
# (df est déjà chargé plus haut)
keys_csv = set(zip(df['country_join'], df['city_join']))

# Récupérer l'ensemble des clés du JSON nettoyé
# (measurements est déjà chargé plus haut)
keys_json = set()
for m in measurements:
    keys_json.add( (m['country_join'], m['city_join']) )

# Calcul de l'intersection (Les villes communes)
common_cities = keys_csv.intersection(keys_json)
missing_in_json = keys_csv - keys_json # Villes vertes qu'on ne trouve pas dans la pollution

print("\n--- RÉSULTATS DU MATCHING ---")
print(f"Nombre de villes dans le CSV (Green) : {len(keys_csv)}")
print(f"Nombre de villes dans le JSON (Pollution) : {len(keys_json)}")
print(f"-> NOMBRE DE VILLES COMMUNES : {len(common_cities)}")

# Afficher quelques exemples de succès pour te rassurer
print("\nExemples de matchs réussis :")
print(list(common_cities)[:10])

# Afficher les ratés pour voir s'il faut encore améliorer le dictionnaire
print("\nExemples de matchs ratés (Dans CSV mais pas JSON) :")
print(list(missing_in_json)[:10])
