# Knowledge Engineering Project
1. Figure out a use case to integrate 2 independent data sources:
	- Select source data: CSV/JSON files (local FS or over http/Web API) or RDB

Datasets used:
- [1. Open Spaces and Green Areas (XLS)](https://data.unhabitat.org/pages/open-spaces-and-green-areas)
- [2. Global Air Pollution Data (CSV)](https://www.kaggle.com/datasets/sazidthe1/global-air-pollution-data)
- [3. Air Quality Programmatics (JSON)](https://aqicn.org/api/data)

Link: link between green areas and air quality in cities.

Use cases to integrate 2 independent data sources:
- "In what city we have pollution value X and green space value Y?"
- "Top 10 cities with highest pollution level and lowest green space value"

First we will convert the .xlsx file (1) to .csv.
And using the JSON format form (3), we will convert the .csv file (2) to .json.
This will ensure we use one CSV file and one JSON file.

After applying our Python normalization script (cleaning parentheses, accents, and slugs), we increased the number of joined cities from 365 to 435 (+19%).
The remaining discrepancies are largely due to data incompleteness (cities present in one dataset but genuinely missing from the other), rather than naming mismatches. We consider this subset of 435 common cities sufficient and high-quality for our Knowledge Graph analysis.

**----------------------------------------------------------------------------------------**

2) Select and understand target vocabularies:
• Schema.org, DBpedia, https://lov.linkeddata.es/dataset/lov/ …

Goals: select **classes** and **properties**

Main classes: **City**, and **Country**. They are common to both datasets.
Main properties: 
- **City**: `isInCountry`, `hasName`, `hasCityCode`, etc. (might change over time)
- **Country**: `hasName`, `isInRegion`, `isInSubRegion`, etc.

Concerning the data from the dataset, we could add properties such as: `aqiValue`, `coValue`, `no3Value`, etc, and `greenArea`...


Vocabularies chosen:

1) Schema.org (schema:): Backbone for Geographic Entities
We use Schema.org as the reference ontology to define the static structure of our knowledge graph. 

Main Classes: schema:City for cities, schema:Country for countries.

Regional Hierarchy: We use schema:AdministrativeArea to model UN SDG Regions and Sub-Regions (e.g., "Southern Asia").

Key Properties:

schema:name: Standard label for all entities (City, Country, Region).

schema:identifier: Stores technical codes (e.g., "AF_KABUL" or internal City Codes).

schema:containedInPlace: Defines the hierarchical relationship (e.g., City $\rightarrow$ Country $\rightarrow$ Sub-Region $\rightarrow$ Region). This enables transitive queries (e.g., finding all cities within a specific continent).

2) SOSA/SSN (Sensor, Observation, Sample, and Actuator):
We selected the W3C standard SOSA to model all dynamic data (Air Quality and Green Area statistics). Since these values are time-dependent and not static attributes of a city, we model them as Observations.
​

Class: sosa:Observation

Key properties:

sosa:hasFeatureOfInterest: Links the observation to the schema:City.

sosa:hasSimpleResult: Contains the numeric value (AQI value, Green Area percentage).

sosa:resultTime: Specifies the timestamp or year of the data.

schema:qualitativeValue: The category label (e.g., "Moderate", "Good"). Since these categories are specific to the index scale used in the source dataset (and differ from EU/US standards), we preserve them as literal strings rather than mapping them to a specific ontology class.

sosa:observedProperty: Defines what is being measured (see below).

3) Eionet Air Quality Vocabulary:
To define pollutants semantically, we reuse the official European Environment Agency (EEA) vocabulary. This provides standard URIs for chemical compounds instead of creating custom ones.
​

Usage: Used in sosa:observedProperty.

Examples: http://dd.eionet.europa.eu/vocabulary/aq/pollutant/7 (for Ozone/O3), .../8 (for NO2).

4) DBpedia & QUDT:
We use DBpedia to define concepts not present in Eionet, specifically for Green Areas and the Air Quality Index itself. QUDT is used to handle units explicitly.

Green Areas: Modeled as sosa:Observation. The sosa:observedProperty points to dbr:Urban_green_space (DBpedia resource).

For "Share of green area", we add sosa:hasResultUnit pointing to unit:PERCENT (from QUDT).

For "Green area per capita", the unit is documented as m²/person.

Air Quality Index (AQI): The sosa:observedProperty points to dbr:Air_quality_index.

**----------------------------------------------------------------------------------------**

3) Translate both sources into RDF using RML

For the resource URIs we use the strategies:

1) Administrative entities:

Regions: http://example.org/region/{Region_Name}

Countries: http://example.org/country/{Country_Name}

Cities: http://example.org/city/{Country_Name}/{City_Name}


2) Observations:

http://example.org/obs/{Measure_Type}/{Country_Name}/{City_Name}


@prefix schema: <http://schema.org/> .
@prefix sosa:   <http://www.w3.org/ns/sosa/> .
@prefix ex:     <http://example.org/> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix qudt:   <http://qudt.org/vocab/unit/> .



ex:region/Asia a schema:AdministrativeArea ;
    schema:name "Asia" ;
    schema:description "SDG Region" .

ex:region/Southern_Asia a schema:AdministrativeArea ;
    schema:name "Southern Asia" ;
    schema:description "SDG Sub-Region" ;
    schema:containedInPlace ex:region/Asia .

ex:country/Afghanistan a schema:Country ;
    schema:name "Afghanistan" ;
    schema:containedInPlace ex:region/Southern_Asia .

ex:city/Afghanistan/Kabul a schema:City ;
    schema:name "Kabul" ;
    schema:identifier "AF_KABUL" ;
    schema:containedInPlace ex:country/Afghanistan .



# Green Areas
ex:obs/GreenShare/Afghanistan/Kabul a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:city/Afghanistan/Kabul ;
    sosa:resultTime "2020"^^xsd:gYear ;
    sosa:observedProperty <http://dbpedia.org/resource/Urban_green_space> ;
    schema:name "Green Area Share" ;
    sosa:hasSimpleResult "3.51"^^xsd:double ;
    sosa:hasResultUnit qudt:PERCENT .

ex:obs/GreenCapita/Afghanistan/Kabul a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:city/Afghanistan/Kabul ;
    sosa:resultTime "2020"^^xsd:gYear ;
    sosa:observedProperty <http://dbpedia.org/resource/Urban_green_space> ;
    schema:name "Green Area Per Capita" ;
    sosa:hasSimpleResult "1.71"^^xsd:double ;
    rdfs:comment "Unit: square meters per person" .


# Global AQI
ex:obs/AQI/Afghanistan/Kabul a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:city/Afghanistan/Kabul ;
    sosa:observedProperty <http://dbpedia.org/resource/Air_quality_index> ;
    sosa:hasSimpleResult "64"^^xsd:integer ;
    schema:qualitativeValue "Moderate" .

# O3
ex:obs/O3/Afghanistan/Kabul a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:city/Afghanistan/Kabul ;
    sosa:resultTime "2025"^^xsd:gYear ; 
    sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/7> ;
    sosa:hasSimpleResult "41"^^xsd:integer ;
    schema:qualitativeValue "Good" .

# NO2
ex:obs/NO2/Afghanistan/Kabul a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:city/Afghanistan/Kabul ;
    sosa:resultTime "2025"^^xsd:gYear ;
    sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/8> ;
    sosa:hasSimpleResult "0"^^xsd:integer ;
    schema:qualitativeValue "Good" .

# CO
ex:obs/CO/Afghanistan/Kabul a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:city/Afghanistan/Kabul ;
    sosa:resultTime "2025"^^xsd:gYear ;
    sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/10> ;
    sosa:hasSimpleResult "0"^^xsd:integer ;
    schema:qualitativeValue "Good" .

# PM2.5
ex:obs/PM25/Afghanistan/Kabul a sosa:Observation ;
    sosa:hasFeatureOfInterest ex:city/Afghanistan/Kabul ;
    sosa:resultTime "2025"^^xsd:gYear ;
    sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001> ;
    sosa:hasSimpleResult "64"^^xsd:integer ;
    schema:qualitativeValue "Moderate" .




Interesting links:
https://ourworldindata.org/air-pollution 
