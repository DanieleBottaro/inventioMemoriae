import os
from jinja2 import Environment, FileSystemLoader
from json_xml_to_rdf import parse_tei_xml, parse_json_data


    
json_entities, json_relations = parse_json_data("../xml_json_files/inMe_extra_entities.json")
xml_entities, xml_relations = parse_tei_xml("../xml_json_files/inMe_TEI.xml")

all_entities = json_entities.copy()
all_entities.update(xml_entities)

all_relations = json_relations.copy()
all_relations.extend(xml_relations)

entity_type = {}
for rel in all_relations:
    if rel[1] == "rdf:type":
        entity_type[rel[0]] = rel[2].lower()

categorized_data = {
    "people": [],
    "places": [],
    "events": [],
    "artworks": [],
    "narrative_themes": [],
    "literary_works": [],
    "visual_items": [],
    "other": []
}

for entity_id, entity_data in all_entities.items():

    entity_data['id'] = entity_id

    type_ent = entity_type.get(entity_id, '')

    if "person" in type_ent:
        categorized_data["people"].append(entity_data)

    elif "place" in type_ent:
        categorized_data["places"].append(entity_data)

    elif "event" in type_ent:
        categorized_data["events"].append(entity_data)

    elif "human-made_object" in type_ent:
        categorized_data["artworks"].append(entity_data)

    elif "propositional_object" in type_ent:
        categorized_data["narrative_themes"].append(entity_data)
    
    elif "f1_work" in type_ent:
        categorized_data["literary_works"].append(entity_data)

    elif "visual_item" in type_ent:
        categorized_data["visual_items"].append(entity_data)

    else:
        categorized_data["other"].append(entity_data)

script_dir = os.path.dirname(os.path.abspath(__file__)) 

# Sali di un livello e scendi nella cartella dei template 
# ATTENZIONE: Modifica '../templates' con il percorso relativo corretto 
# per arrivare dalla cartella del tuo script alla cartella dei template.
template_dir = os.path.join(script_dir, '../documentation')

# Diciamo a Jinja2 di cercare in questa cartella
env = Environment(loader=FileSystemLoader(template_dir))

# 3. CARICAMENTO DEL TEMPLATE
# Ora Jinja cercherà 'index2.html' dentro 'template_dir'
template = env.get_template('index2.html')

# 4. RENDERIZZAZIONE
risultato_html = template.render(categorized_data)

# 5. SALVATAGGIO
# Salviamo il file HTML generato. 
# Anche qui, possiamo decidere di salvarlo nella cartella root o altrove.
output_path = os.path.join(script_dir, '../documentation/documentazione_finale.html')

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(risultato_html)

print(f"File generato con successo in: {os.path.abspath(output_path)}")
