
# Knowledge Engineering Project

1) Figure out a use case to integrate 2 independent data sources:

Select source data: CSV/JSON files (local FS or over http/Web API) or RDB

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


2) Select and understand target vocabularies:
• Schema.org, DBpedia, https://lov.linkeddata.es/dataset/lov/ …

Vocabularies used:









Interesting links:
https://ourworldindata.org/air-pollution 
