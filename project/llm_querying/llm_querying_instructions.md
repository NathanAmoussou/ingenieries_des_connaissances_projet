# LLM Querying

## Step 1: Define the LLM querying pipeline

Defined in `llm_to_sparql.ipynb`.

## Step 2: Prompting the LLM to translate queries

Query 1:

> Which are the 50 cities with the highest PM2.5 AQI and their green area per capita?

LLM output:

```sparql
PREFIX schema: <http://schema.org/>
PREFIX sosa:   <http://www.w3.org/ns/sosa/>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?cityName ?pm25Cat ?greenM2
WHERE {
  ?city a schema:City ;
        schema:name ?cityName .
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?city ;
       schema:name "Air Quality Index" ;
       sosa:hasSimpleResult ?aqi .
  ?pm25Obs a sosa:Observation ;
         sosa:hasFeatureOfInterest ?city ;
         sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001> ;
         schema:qualitativeValue ?pm25Cat ;
         sosa:hasSimpleResult ?pm25 .
  ?gObs a sosa:Observation ;
        sosa:hasFeatureOfInterest ?city ;
        schema:name "Green Area Per Capita" ;
        sosa:hasSimpleResult ?greenM2 .
  FILTER(?aqi = 50 && ?pm25Cat = "High")
}
ORDER BY DESC(?greenM2)
```

Query 2:

> Which cities have Green Area Share below 5% and what is their PM2.5 category?

LLM output:

```sparql
PREFIX schema: <http://schema.org/>
PREFIX sosa:   <http://www.w3.org/ns/sosa/>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?cityName (CASE ?pm25Cat WHEN "Good" THEN "Good" ELSE ?pm25Cat END) AS ?pm25Cat
WHERE {
  ?city a schema:City ;
        schema:name ?cityName .
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?city ;
       schema:name "Green Area Share" ;
       sosa:hasSimpleResult ?share ;
       sosa:hasSimpleResult ?pm25 .
  FILTER(?share < 5)
  BIND(sosa:label(?pm25) AS ?pm25Cat)
}
```

Query 3:

> Is there a relationship between PM2.5 and Green Area Per Capita? Return city, pm25, greenM2.

LLM output:

```sparql
PREFIX schema: <http://schema.org/>
PREFIX sosa:   <http://www.w3.org/ns/sosa/>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?city ?pm25 ?greenM2
WHERE {
  ?obs a sosa:Observation ;
       sosa:hasFeatureOfInterest ?city ;
       schema:name "Green Area Per Capita" ;
       sosa:hasSimpleResult ?greenM2 .
  OPTIONAL { ?obs sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001> ;
         sosa:hasSimpleResult ?pm25 } .
}
```

## Step 3: Testing the output

Result for query 1 (empty):

```csv

```

Result for query 2 (Corese error):

```text
fr.inria.corese.core.sparql.exceptions.QuerySyntaxException: fr.inria.corese.core.sparql.triple.javacc1.JavaccParseException: Incorrect Variable: CASE Line: 6
```

Result for query 3:

```csv
1	<http://example.org/city/afghanistan/herat>		"1.75"^^xsd:double
2	<http://example.org/city/afghanistan/kabul>		"1.71"^^xsd:double
3	<http://example.org/city/afghanistan/kandahar>		"1.66"^^xsd:double
4	<http://example.org/city/afghanistan/mazar_e_sharif>		"1.45"^^xsd:double
5	<http://example.org/city/algeria/annaba>		"17.73"^^xsd:double
6	<http://example.org/city/algeria/batna>		"2.42"^^xsd:double
7	<http://example.org/city/algeria/blida>		"13.53"^^xsd:double
8	<http://example.org/city/algeria/chlef>		"6.46"^^xsd:double
9	<http://example.org/city/algeria/qacentina>		"5.18"^^xsd:double
10	<http://example.org/city/algeria/tiaret>		"0.17"^^xsd:double
...
```
