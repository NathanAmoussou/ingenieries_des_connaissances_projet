# Knowledge Engineering Project - SPARQL Side
## Roadmap
- [ ] Data preparation
	- [x] Find two heterogeneous data sources
		- [Open Spaces and Green Areas](https://data.unhabitat.org/pages/open-spaces-and-green-areas) (XLS)
		- [Global Air Pollution Data](https://www.kaggle.com/datasets/sazidthe1/global-air-pollution-data) (CSV)
	- [x] Clean and prepare the sources
		- Done in `projet/data/cleaning.ipynb`
	- [ ] Write the report part
- [ ] RDF graph generation using RML
- [ ] SPARQL queries preparation to query the graph
	- [x] Define competency questions that require both sources
	- [ ] When available, adapt Fuseki and Corese
	- [ ] Write the report part
- [ ] Explore an LLM-based approach to query the graph
- [ ] Write report
## Competency questions
Which cities should be prioritized for intervention because they combine high PM2.5 AQI and low green area per capita (2020)?
```
PREFIX ex: <http://example.org/>

SELECT ?country ?city ?pm25 ?greenM2
WHERE {
  ?v ex:country ?country ;
     ex:city ?city ;
     ex:pm25_aqi_value ?pm25 ;
     ex:green_area_per_capita_2020 ?greenM2 .
  FILTER(?pm25 > X && ?greenM2 < Y)
}
ORDER BY DESC(?pm25) ASC(?greenM2)
LIMIT 50
```
Which countries have the highest average PM2.5 AQI across matched cities, and what is their average green area per capita (2020)?
```
PREFIX ex: <http://example.org/>

SELECT ?country
       (COUNT(?v) AS ?nCities)
       (AVG(?pm25) AS ?avgPm25)
       (AVG(?greenM2) AS ?avgGreenM2)
WHERE {
  ?v ex:country ?country ;
     ex:pm25_aqi_value ?pm25 ;
     ex:green_area_per_capita_2020 ?greenM2 .
}
GROUP BY ?country
HAVING (COUNT(?v) >= N)
ORDER BY DESC(?avgPm25)
LIMIT 15
```
Within each country, which cities are worse than their national average for PM2.5 AQI while also being below the national average for green area per capita (2020)?
```
PREFIX ex: <http://example.org/>

SELECT ?country ?city ?pm25 ?greenM2 ?avgPm25 ?avgGreenM2
WHERE {
  # (1) calcul des moyennes nationales
  {
    SELECT ?country
           (AVG(?pm25) AS ?avgPm25)
           (AVG(?greenM2) AS ?avgGreenM2)
    WHERE {
      ?v ex:country ?country ;
         ex:pm25_aqi_value ?pm25 ;
         ex:green_area_per_capita_2020 ?greenM2 .
    }
    GROUP BY ?country
  }

  # (2) villes à comparer à leur moyenne nationale
  ?v2 ex:country ?country ;
      ex:city ?city ;
      ex:pm25_aqi_value ?pm25 ;
      ex:green_area_per_capita_2020 ?greenM2 .

  FILTER(?pm25 > ?avgPm25 && ?greenM2 < ?avgGreenM2)
}
ORDER BY DESC(?pm25)
LIMIT 200
```