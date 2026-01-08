# SPARQL Querying

## Step 1: Define SPARQL queries

Based on the generated RDF graph structure (in `rdf_mapping/rdf_graph`), we define three SPARQL queries.

Query 1 (in `sparql_query_1.rq`):

> Which cities should be prioritized because they combine high PM2.5 AQI (`100`) and low green area per capita (`10.0`) (2020)?

Query 2 (in `sparql_query_2.rq`):

> Which countries have the highest average PM2.5 AQI across matched cities, and what is their average green area per capita (2020)?

Query 3 (in `sparql_query_3.rq`):

> Within each country, which cities are above the national average for PM2.5 AQI while being below the national average for green area per capita (2020)?

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
