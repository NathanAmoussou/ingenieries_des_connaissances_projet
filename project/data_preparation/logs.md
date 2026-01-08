## Journal de mise en conformité des données (so far)

### Contrainte projet

Le projet impose d’intégrer **deux sources hétérogènes**, notamment avec **des formats différents**. Nos deux jeux de données initiaux étant tous les deux en **CSV**, nous avons décidé de conserver le dataset UN-Habitat “Open Spaces and Green Areas” tel quel (CSV/Excel exportable CSV) et de transformer le dataset “Global Air Pollution Data” (CSV) en **JSON**.

### Facelift / transformation du dataset “Global Air Pollution Data”

Nous avons développé un script `csv_to_json.py` qui :

1. **Lit le CSV** de pollution (`pollution.csv`).
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

* `pollution.json` généré avec **23035** enregistrements valides,
* **428** lignes ignorées car incomplètes.

### Résultat attendu pour la suite (RML)

Nous avons maintenant deux sources hétérogènes prêtes au “data lifting” :

* **Source espaces verts** : CSV (UN-Habitat)
* **Source pollution** : JSON (facelift local)

Étape suivante : écrire deux mappings RML (CSV + JSON) avec une stratégie d’URI commune (ville/pays) afin de produire un graphe RDF intégré et interrogeable en SPARQL.

### Contrôle qualité & facelift des données “Green Areas”

Après génération du JSON pollution, nous avons effectué un contrôle qualité minimal sur les deux sources afin de fiabiliser la jointure ville/pays :

**Résultats audit (avant facelift green)**

* *Green areas* : 667 lignes

  * Doublons `City Name` (tous pays confondus) : 14 lignes, expliqués principalement par des **noms de villes ambiguës entre pays** et des valeurs manquantes.
  * Doublons `(pays, ville)` : 0 (absence de “vrais doublons” intra-pays)
  * Doublons `City Code` : uniquement dus aux valeurs manquantes ; vérification “hors NA” = 0 doublon réel
  * Valeurs manquantes : `City Name` = 8, `City Code` = 8
* *Pollution* : 23035 lignes, pas de valeurs manquantes sur `country_name`, `city_name`, `aqi.value`, `pm25.value`.

**Intersection (jointure possible) – avant facelift green**

* Paires (pays, ville) green : 667
* Paires (pays, ville) pollution : 23035
* Paires communes : 365

**Facelift appliqué au dataset green**
Pour augmenter l’intersection et éviter des jointures incorrectes, nous avons créé `green_facelift.csv` en :

1. supprimant les lignes incomplètes (City Name/Code manquants) → 667 → **659** lignes,
2. ajoutant des colonnes techniques de jointure `country_join` et `city_join`,
3. normalisant les chaînes (trim, minuscules, suppression NBSP, suppression accents, espaces multiples),
4. harmonisant certains noms de pays (ex. noms “ONU” → forme plus courte) via une table de correspondance minimale,
5. générant plusieurs variantes de noms de ville (ex. suppression des parenthèses, extraction d’alias entre parenthèses, gestion des virgules/tirets) et en sélectionnant automatiquement la variante qui matche le mieux la pollution dans le même pays.

**Intersection (jointure possible) – après facelift green**

* Paires green (après suppression des manquants) : **659**
* Paires communes : **450** (gain de +85 matches, ~68% des villes green matchées)
* Des règles supplémentaires d’harmonisation (pays/villes) ont été testées ensuite mais **sans gain** : nous avons donc arrêté le pré-traitement à ce niveau pour rester dans une approche simple et contrôlée.
