# Plan de Projet : Intégration de Données Hétérogènes (RML & SPARQL)

Ce document détaille les étapes de réalisation du projet d'ingénierie des connaissances, visant à intégrer des données sur les espaces verts urbains et la pollution de l'air dans un graphe de connaissances unifié.

## Phase 1 : Modélisation des Données

Cette phase conceptuelle est critique pour assurer l'interopérabilité des deux sources de données.

1.  **Définition de la stratégie de nommage (URIs)**
    * Utiliser le nom de la ville comme clé de jointure entre les deux sources.
    * **Format cible des URIs** : `http://example.org/city/{Nom_De_La_Ville_Normalisé}`.
    * *Note :* S'assurer que les espaces et caractères spéciaux sont traités de manière identique dans les deux mappings (encodage URL ou remplacement par des underscores).

2.  **Sélection des vocabulaires et ontologies**
    * Identifier les classes et propriétés standards à réutiliser (ex: `schema:City`, `dbo:City`).
    * Définir les prédicats pour les mesures spécifiques si aucun standard n'existe (ex: `ex:greenAreaPercentage`, `ex:aqiValue`, `ex:pm25Concentration`).

3.  **Conception du graphe cible**
    * Modéliser la structure RDF attendue : un nœud central "Ville" auquel sont rattachés les indicateurs provenant des deux fichiers sources.

## Phase 2 : Implémentation des Mappings RML

Création des fichiers de mapping `.ttl` pour transformer les sources CSV en RDF.

1.  **Mapping de la Source 1 (Espaces Verts)**
    * Fichier : `green_mapping.ttl`.
    * Source : `Share_of_green_areas...Data.csv`.
    * **Objectif** : Mapper le nom de la ville (Sujet) et les pourcentages d'espaces verts (Objets).

2.  **Mapping de la Source 2 (Pollution)**
    * Fichier : `pollution_mapping.ttl`.
    * Source : `global_air_pollution_data.csv`.
    * **Objectif** : Mapper le nom de la ville (Sujet) et les indices de pollution (AQI, CO, Ozone, etc.).

3.  **Tests unitaires**
    * Exécuter le RMLMapper sur un échantillon réduit de données pour valider la syntaxe RDF et la structure des URIs générées.

## Phase 3 : Génération et Vérification du Graphe

Production des données RDF finales et validation de l'intégration.

1.  **Exécution complète**
    * Lancer le RMLMapper sur les fichiers complets pour générer `green_output.ttl` et `pollution_output.ttl`.

2.  **Vérification de la jointure**
    * Inspecter les fichiers de sortie pour confirmer que les URIs des villes communes sont strictement identiques dans les deux graphes.
    * *Critère de succès :* Les informations de pollution et d'espaces verts doivent pouvoir être rattachées au même sujet RDF.

## Phase 4 : Exploitation et Expérimentation

Validation de l'utilité du graphe via des requêtes et des outils d'IA.

1.  **Requête SPARQL d'intégration**
    * Rédiger et exécuter une requête SPARQL impliquant les propriétés des deux sources simultanément.
    * *Exemple :* Sélectionner les villes ayant un fort taux d'espaces verts et un faible indice de pollution.
    * Capturer le résultat de l'exécution (preuve de fonctionnement).

2.  **Prototypage LLM (Text-to-SPARQL)**
    * Fournir le schéma de données (modèle de la Phase 1) à un LLM.
    * Tester la traduction de questions en langage naturel vers SPARQL (ex: "Quelles sont les villes les plus polluées ?").
    * Définir 3 "Questions de Compétence" pour évaluer les capacités du système.
    * Analyser les succès et les échecs de l'approche.

## Phase 5 : Livrables et Rapport

Finalisation du rendu du projet.

1.  **Constitution du dossier technique**
    * Regrouper les mappings RML, les fichiers RDF générés et les scripts de pré-traitement éventuels.

2.  **Rédaction du rapport**
    * Décrire le scénario d'intégration.
    * Justifier les choix de modélisation (URIs, vocabulaires).
    * Documenter la méthodologie et les difficultés rencontrées.
    * Présenter l'analyse critique de l'expérimentation avec le LLM.