# inventioMemoriae
## Mapping the construction of Memory: A Linked Open Data approach to Nicola Pisano’s Arca di San Domenico

*InventioMemoriae* aims to model and represent in Linked Open Data (LOD) format the iconography chosen by the Dominicans to decorate the panels of the sarcophagus of the *Arca di San Domenico* by Nicola Pisano in Bologna, as a visual consecration and monumental objectification of a process of "memory construction".
The project bridges the gap between hagiographic textual narratives and sculptural visual representations by employing a Semantic Web architecture. It extracts entities from critical TEI-XML encoded texts and a supplementary JSON dataset, structuring them into a Linked Open Data knowledge graph .

├── html_files/
│   ├── Index_src.html
│   ├── inMe_stylised_xml.html
│   └── zoom-page.html
├── images/
│   ├── conceptual_model.svg
│   ├── inme_rdf-viewer.svg
│   └── theoretical_model.svg
├── python_script/
│   ├── jinja_template.py
│   ├── json_xml_to_rdf.py
│   └── xml-html_transformation.py
├── rdf_dataset/
│   └── inventio_memoriae_graph.ttl
├── style/
│   ├── doc_style.css
│   └── xsl_style.css
├── xml_json_files/
│   ├── inMe_extra_entities.json
│   └── inMe_TEI.xml
├── xslt/
│   └── inMe_XSLT.xslt
├── yED_files/
│   ├── conceptual_model_def.graphml
│   └── theoretical_model_def.graphml
├── index.html
├── requirements.txt
└── README.md

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

### 3. View the Output
Open ```index.html``` in the root folder to explore the documentation, ora navigate to the ```html_files/inMe_stylised_xml.html``` to view the generated XSLT textual view

## Authors & License

* **Author**: Daniele Bottaro
* **Context**: Developed as a final project for the 2025-2026 Information Science and Cultural Heritage course at University of Bologna
* **License**: Data and documentation are released under a Creative Commons Attribution 4.0 (CC BY 4.0) license.

