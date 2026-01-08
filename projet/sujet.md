1. Figure out a use case to integrate 2 independent data sources:

Select source data: CSV/JSON/XML files (local FS or over http, Web API) or RDB
Select and understand target vocabularies.
E.g. Schema.org, DBpedia, https://lov.linkeddata.es/dataset/lov/ …
Reuse existing vocabularies, do not create your own unless discussed and agreed with the teacher.
2. Translate both sources into RDF using RML

Define a resource naming strategy: how to construct the resource URIs
Write an example of the RDF you would like to generate
Define how to join the 2 sources: name? identifier? etc.
Pre-process the files if needed (e.g. in python) or use RML functions: remove outliers, fix syntax variations, etc.
Write and execute the RML mappings
3. Write a SPARQL query that involves the triples generated from both data sources
 
4. Start prototyping an LLM-based approach to query the graph
Goal: translate a natural language question into an equivalent SPARQL query
Use an LLM of your choice. The important is the method, not the fact that the result will be the right one => using a small or large model will not change the grade.
Propose 3 competency questions that query different aspects of the graph.
Discuss the results: What works? What does not work? What could help improve?
5. Upload the result of your work as a Zip file containing

Files you produced: mappings + CSV/JSON/RDB + RDF result
Snapshot of SPARQL queries execution
Report:
No ChatGPT fluff!
Useful information only:
succinct description of your use case
resource naming strategy: how to construct the resource URIs
modelling choices,
how the 2 sources:  are joined: name? identifier?
methodology adopted for the text-to-SPARQL translation
difficulties
