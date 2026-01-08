# SPARQL Querying

## Step 1: Define SPARQL queries

Based on the generated RDF graph structure (in `rdf_mapping/rdf_graph`), we define three SPARQL queries.

Query 1:

> Which cities should be prioritized because they combine high PM2.5 AQI (`100`) and low green area per capita (`10.0`) (2020)?

```sparql
PREFIX schema: <http://schema.org/>
PREFIX sosa:   <http://www.w3.org/ns/sosa/>

SELECT ?countryName ?cityName ?pm25 ?pm25Cat ?greenM2
WHERE {
  VALUES (?pm25Th ?greenTh) { (100 10.0) }   # <-- à ajuster après test

  ?city a schema:City ;
        schema:name ?cityName ;
        schema:containedInPlace ?country .
  ?country a schema:Country ;
           schema:name ?countryName .

  ?pmObs a sosa:Observation ;
         sosa:hasFeatureOfInterest ?city ;
         sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001> ;
         sosa:hasSimpleResult ?pm25 ;
         schema:qualitativeValue ?pm25Cat .

  ?greenObs a sosa:Observation ;
            sosa:hasFeatureOfInterest ?city ;
            schema:name "Green Area Per Capita" ;
            sosa:hasSimpleResult ?greenM2 .

  FILTER(?pm25 > ?pm25Th && ?greenM2 < ?greenTh)
}
ORDER BY DESC(?pm25) ASC(?greenM2)
LIMIT 50
```

Query 2:

> Which countries have the highest average PM2.5 AQI across matched cities, and what is their average green area per capita (2020)?

```sparql
PREFIX schema: <http://schema.org/>
PREFIX sosa:   <http://www.w3.org/ns/sosa/>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>

SELECT ?countryName ?nCities ?avgPm25 ?avgGreenM2
WHERE {
  {
    SELECT ?countryName
           (COUNT(DISTINCT ?city) AS ?nCities)
           (AVG(?pm25d) AS ?avgPm25)
           (AVG(?greenD) AS ?avgGreenM2)
    WHERE {
      ?city schema:containedInPlace ?country .
      ?country schema:name ?countryName .

      ?pmObs a sosa:Observation ;
             sosa:hasFeatureOfInterest ?city ;
             sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001> ;
             sosa:hasSimpleResult ?pm25 .

      ?greenObs a sosa:Observation ;
                sosa:hasFeatureOfInterest ?city ;
                schema:name "Green Area Per Capita" ;
                sosa:hasSimpleResult ?greenM2 .

      BIND(xsd:decimal(?pm25)    AS ?pm25d)
      BIND(xsd:decimal(?greenM2) AS ?greenD)
    }
    GROUP BY ?countryName
    HAVING (COUNT(DISTINCT ?city) >= 3)
  }
}
ORDER BY DESC(?avgPm25)
LIMIT 15
```

> Within each country, which cities are above the national average for PM2.5 AQI while being below the national average for green area per capita (2020)?

```sparql
PREFIX schema: <http://schema.org/>
PREFIX sosa:   <http://www.w3.org/ns/sosa/>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>

SELECT ?countryName ?cityName ?pm25 ?greenM2 ?avgPm25 ?avgGreenM2
WHERE {
  # (1) National averages per country (computed on matched cities only)
  {
    SELECT ?country ?countryName
           (AVG(?pm25d_in) AS ?avgPm25)
           (AVG(?greenD_in) AS ?avgGreenM2)
    WHERE {
      ?city_in schema:containedInPlace ?country .
      ?country schema:name ?countryName .

      ?pmObs_in a sosa:Observation ;
                sosa:hasFeatureOfInterest ?city_in ;
                sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001> ;
                sosa:hasSimpleResult ?pm25_in .

      ?greenObs_in a sosa:Observation ;
                   sosa:hasFeatureOfInterest ?city_in ;
                   schema:name "Green Area Per Capita" ;
                   sosa:hasSimpleResult ?green_in .

      BIND(xsd:decimal(?pm25_in)  AS ?pm25d_in)
      BIND(xsd:decimal(?green_in) AS ?greenD_in)
    }
    GROUP BY ?country ?countryName
    HAVING (COUNT(DISTINCT ?city_in) >= 2)
  }

  # (2) Cities compared to their national averages
  ?city schema:containedInPlace ?country ;
        schema:name ?cityName .

  ?pmObs a sosa:Observation ;
         sosa:hasFeatureOfInterest ?city ;
         sosa:observedProperty <http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001> ;
         sosa:hasSimpleResult ?pm25 .

  ?greenObs a sosa:Observation ;
            sosa:hasFeatureOfInterest ?city ;
            schema:name "Green Area Per Capita" ;
            sosa:hasSimpleResult ?greenM2 .

  BIND(xsd:decimal(?pm25)    AS ?pm25d)
  BIND(xsd:decimal(?greenM2) AS ?greenD)

  FILTER(?pm25d > ?avgPm25 && ?greenD < ?avgGreenM2)
}
ORDER BY DESC(?pm25d)
LIMIT 200
```

## Step 2: Test these queries against our graph

We use the tool Corese. We load the RDF graph and each of these queries.

Results for query 1:

```csv
1	India	Moradabad	500	Hazardous	"4.01"^^xsd:double
2	India	Delhi	446	Hazardous	"3.68"^^xsd:double
3	Pakistan	Faisalabad	301	Hazardous	"2.65"^^xsd:double
4	Pakistan	Hāfizābād	248	Very Unhealthy	"1.07"^^xsd:double
5	Pakistan	Jhang	208	Very Unhealthy	"7.77"^^xsd:double
...
```

Results for query 2:

```csv
1	Pakistan	16	185,563	7,58500
2	India	26	175,385	7,94423
3	China	10	166,200	50,5860
4	South Africa	4	140,250	20,0875
5	Tajikistan	3	111,667	26,2400
...
```

Results for query 3:

```csv
1	India	Moradabad	500	"4.01"^^xsd:double	175,385	7,94423
2	India	Delhi	446	"3.68"^^xsd:double	175,385	7,94423
3	Pakistan	Faisalabad	301	"2.65"^^xsd:double	185,563	7,58500
4	Pakistan	Hāfizābād	248	"1.07"^^xsd:double	185,563	7,58500
5	China	Qingdao	232	"38.63"^^xsd:double	166,200	50,5860
...
```
