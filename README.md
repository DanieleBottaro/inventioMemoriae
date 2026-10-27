# inventioMemoriae
## Mapping the construction of Memory: A Linked Open Data approach to Nicola Pisano’s Arca di San Domenico

*InventioMemoriae* aims to model and represent in Linked Open Data (LOD) format the iconography chosen by the Dominicans to decorate the panels of the sarcophagus of the *Arca di San Domenico* by Nicola Pisano in Bologna, as a visual consecration and monumental objectification of a process of "memory construction".
The project bridges the gap between hagiographic textual narratives and sculptural visual representations by employing a Semantic Web architecture. It extracts entities from critical TEI-XML encoded texts and a supplementary JSON dataset, structuring them into a Linked Open Data knowledge graph .

```text
├── html_files/
│   ├── Index_src.html                 # Jinja2 source template for the project documentation
│   ├── inMe_stylised_xml.html         # Human-readable reading view of the TEI-XML sources
│   └── zoom-page.html                 # Interactive pan/zoom and fullscreen viewport for SVGs
├── images/
│   ├── conceptual_model.svg           # Graffoo-based diagram of the conceptual ontology model
│   ├── inme_rdf-viewer.svg            # Node-link graph visualization of the RDF dataset
│   └── theoretical_model.svg          # Visual diagram of the theoretical domain model
├── python_script/
│   ├── apply_owl_rules.py             # Applies OWL axioms defined in Protégé to the base graph
│   ├── jinja_template.py              # Populates Index_src.html with categorized entities
│   ├── json_xml_to_rdf.py             # Extracts XML/JSON data and serializes the base RDF graph
│   └── xml-html_transformation.py     # Applies XSLT to convert TEI-XML into HTML
├── rdf_dataset/
│   ├── inme_graph.ttl                 # Base RDF graph extracted from TEI and JSON
│   ├── inme_inferred_graph.ttl        # Enriched graph with materialized inferences from Protégé
|   └── owl_rules.ttl                  # Custom OWL rules to apply to the base RDF graph for inferences
├── style/
│   ├── doc_style.css                  # Custom styling for index.html and zoom view
│   └── xsl_style.css                  # Stylesheet for the XSLT-generated reading view
├── xml_json_files/
│   ├── inMe_extra_entities.json       # Supplementary JSON dataset with ad-hoc entities/relations
│   └── inMe_TEI.xml                   # TEI-XML document with encoded hagiographical text snippets
├── xslt/
│   └── inMe_XSLT.xslt                 # XSLT transformation rules for TEI-to-HTML conversion
├── yED_files/
│   ├── conceptual_model.graphml       # Source Graffoo file for the conceptual model (yEd)
│   └── theoretical_model.graphml      # Source diagram file for the theoretical model (yEd)
├── index.html                         # Main entry point: project documentation website
├── requirements.txt                   # Python library dependencies
└── README.md                          # Project overview and pipeline documentation
```

## Technical Architecture

The data pipeline follows a strict progression from raw data to structured human-readable interfaces:

1. **Data Modeling & Encoding:** Entities and their relationships are formally identified directly within the **TEI-XML** textual markup. A supplementary **JSON** dataset is used to manage ad-hoc entities and historical context outside the main text flow.
2. **RDF Graph Generation:** A custom **Python** script uses `rdflib` to automatically extract the entities from both the XML and JSON sources, mapping them to the ontology network and serializing the final output as an **RDF Graph** in Turtle format (`.ttl`).
3. **Web Interfaces:** The pipeline generates two distinct HTML outputs to explore the project:
   * **Project Documentation:** The main website. It hosts the theoretical framework and the complete table (created dynamically with Jinja2) of all entities extracted both from the XML and the JSON file.
   * **TEI-XML Reading View:** A standalone HTML page generated directly from the XML sources via an XSLT stylesheet. It provides a structured reading view of the encoded texts, allowing users to explore the marked-up selected snippets.


## How to Run the Pipeline
The Python pipeline automates the data extraction, the RDF serialization, and the dynamic rendering of specific data-driven web components.

### 1. Prerequisites
Ensure Python >=3.14 is installed. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Execute the Pipeline
Navigate to the scripts folder. The three scripts operate independently and handle different aspects of the output generation:
*  ```json_xml_to_rdf.py``` parses the data from the XML and the JSON file and generates the RDF graph;
* ```xml-html_transformation.py``` XSLT-based generation of the html file from the XML file
* ```jinja_template.py``` populate dynamically the Entities tab in the documentation

### 3. View the Output & Query the Data
Open ```index.html``` in the root folder to explore the documentation, or navigate to the ```html_files/inMe_stylised_xml.html``` to view the generated XSLT textual view

To explore the dataset, you can perform custom SPARQL queries using a local RDF graph database such as Blazegraph. You can query two distinct versions of the dataset provided in this repository:
* **The Base Graph** (```inme_graph.ttl```): Contains the explicit historical and art-historical assertions extracted directly from the textual sources and the custom ones that have been defined in the JSON file (```inMe_extra_entities.json```)
* **The Inferred Graph** (```inme_inferred_graph.ttl```): Contains the extended, reasoner-processed dataset.

**Quick Blazegraph setup:**
1. Download the latest blazegraph.jar release;

2. Run the server locally via terminal: java -server -Xmx4g -jar blazegraph.jar;

3. Open the web interface at http://localhost:9999/blazegraph/;

4. Go to the Update tab and upload either the base or the inferred .ttl file;

5. Navigate to the Query tab to run the examples below.

## Authors & License

* **Author**: Daniele Bottaro
* **Context**: Developed as a final project for the 2025-2026 Information Science and Cultural Heritage course at University of Bologna
* **License**: Data and documentation are released under a Creative Commons Attribution 4.0 (CC BY 4.0) license.
