# RML Mapping

## Step 1: Define an RDF graph example

Before mapping, we define (and validate with the professor) an example of the RDF graph we aim to build in `rdf_example_graph.tll`.

## Step 2: Define the RDF mapping

In `mapping.ttl`, we define a mapping from `clean_green.csv` and `clean_pollution.json` to a RDF graph.

## Step 3: Install RMLMapper (on Ubuntu)

Install Java 21 or higher:

```bash
sudo apt update
sudo apt install openjdk-21-jre-headless
```

To verify the installation, run: `java -version`.
Then, download the RMLMapper executable:

```bash
# Replace the URL with the latest version link if 8.1.0 is outdated
wget https://github.com/RMLio/rmlmapper-java/releases/download/v8.1.0/rmlmapper-8.1.0-r380-all.jar -O rmlmapper.jar
```

Create a command shortcut to avoid typing `java -jar ...` every time (optionnal):

```bash
mkdir -p ~/opt/rmlmapper
mv rmlmapper.jar ~/opt/rmlmapper/
```

```bash
echo "alias rmlmapper='java -jar ~/opt/rmlmapper/rmlmapper.jar'" >> ~/.bashrc
source ~/.bashrc
```

## Step 4: Map RDF graph with RMLMapper

In `rdf_mapping/`, execute:

```bash
rmlmapper -m mapping.ttl -o rdf_graph.ttl
```

It ouputs the RDF graph `rdf_graph.ttl`.
