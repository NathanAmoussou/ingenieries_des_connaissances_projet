## Journal de mise en conformité des données (so far)

### Contrainte projet

Le projet impose d’intégrer **deux sources hétérogènes**, notamment avec **des formats différents**. Nos deux jeux de données initiaux étant tous les deux en **CSV**, nous avons décidé de conserver le dataset UN-Habitat “Open Spaces and Green Areas” tel quel (CSV/Excel exportable CSV) et de transformer le dataset “Global Air Pollution Data” (CSV) en **JSON**.

### Facelift / transformation du dataset “Global Air Pollution Data”

Nous avons développé un script `csv_to_json.py` qui :

1. **Lit le CSV** de pollution (`global_air_pollution_data.csv`).
2. **Nettoie les en-têtes** : suppression d’un caractère BOM (`utf-8-sig`) et suppression de tabulations/espaces cachés dans certains noms de colonnes (ex : `co_aqi_value` était présent sous une forme “polluée” avec tabulation).
3. **Nettoie les valeurs** : `strip()` (espaces), et conversions de types pour les mesures numériques (`to_int`) afin d’obtenir des valeurs exploitables ensuite en RDF (littéraux typés).
4. **Restructure les données** en JSON en regroupant les informations AQI dans des objets imbriqués (`aqi`, `iaqi`) inspirés d’un format JSON courant d’API AQI (plus natural pour JSON + plus facile à parcourir avec JSONPath en RML).

Structure JSON cible (extrait) :

* `measurements[*].country_name`
* `measurements[*].city_name`
* `measurements[*].aqi.value / aqi.category`
* `measurements[*].iaqi.(co|o3|no2|pm25).value / category`

### Gestion des lignes incomplètes

Pendant la conversion, certaines lignes du CSV ne contenaient pas de `country_name` (exemples : “Granville”, “Kingston Upon Hull”, etc.).
Ces lignes ont été **ignorées** (skip) car elles ne permettent pas :

* de construire des URI stables (ville/pays), et
* de réaliser une jointure fiable avec le dataset “Green Areas” (qui dépend du couple pays/ville).

Résultat conversion :

* `pollution_facelift.json` généré avec **23035** enregistrements valides,
* **428** lignes ignorées car incomplètes.

### Résultat attendu pour la suite (RML)

Nous avons maintenant deux sources hétérogènes prêtes au “data lifting” :

* **Source espaces verts** : CSV (UN-Habitat)
* **Source pollution** : JSON (facelift local)

Étape suivante : écrire deux mappings RML (CSV + JSON) avec une stratégie d’URI commune (ville/pays) afin de produire un graphe RDF intégré et interrogeable en SPARQL.
