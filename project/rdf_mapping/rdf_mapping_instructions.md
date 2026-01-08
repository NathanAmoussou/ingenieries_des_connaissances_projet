# RML Mapping

## Step 1: RDF Mapping Definition

In `mapping.ttl`, we define a mapping from `clean_green.csv` and `clean_pollution.json` to a RDF graph.

## Step 2: Install RMLMapper (on Ubuntu)

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

## Step 3: Map RDF Graph with RMLMapper

In `rdf_mapping/`, execute:

```bash
rmlmapper -m mapping.ttl -o rdf_graph.ttl
```
