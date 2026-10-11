import os
from jinja2 import Environment, FileSystemLoader
from json_xml_to_rdf import parse_tei_xml, parse_json_data

#retrieving data from JSON and XML files
json_entities, json_relations = parse_json_data("../xml_json_files/inMe_extra_entities.json")
xml_entities, xml_relations = parse_tei_xml("../xml_json_files/inMe_TEI.xml")

#merging entities and relations from both sources
all_entities = json_entities.copy()
all_entities.update(xml_entities)

all_relations = json_relations.copy()
all_relations.extend(xml_relations)

#looping through relations to categorize entities based on their types; rel[0] is the subject, rel[1] is the predicate, and rel[2] is the object
entity_type = {}
for rel in all_relations:
    if rel[1] == "rdf:type":
        if rel[0] not in entity_type:
            entity_type[rel[0]] = rel[2].lower()
        else:
            entity_type[rel[0]] += rel[2].lower()

#creating a dictionary to hold categorized entities based on their types
categorized_data = {
    "people": [],
    "events": [],
    "artworks": [],
    "narrative_themes": [],
    "literary_works": [],
    "visual_items": [],
    "other": []
}

#looping through all entities to categorize them based on their types and appending them to the appropriate list in categorized_data
for entity_id, entity_data in all_entities.items():

    entity_data['id'] = entity_id

    type_ent = entity_type.get(entity_id, '')

    if "person" in type_ent:
        categorized_data["people"].append(entity_data)

    elif "event" in type_ent:
        categorized_data["events"].append(entity_data)

    elif "human-made_object" in type_ent or "historicorartisticproperty" in type_ent:
        categorized_data["artworks"].append(entity_data)

    elif "propositional_object" in type_ent:
        categorized_data["narrative_themes"].append(entity_data)
    
    elif "f1_work" in type_ent:
        categorized_data["literary_works"].append(entity_data)

    elif "visual_item" in type_ent:
        categorized_data["visual_items"].append(entity_data)

    else:
        categorized_data["other"].append(entity_data)

#setting up Jinja2 environment to load templates from the specified directory
script_dir = os.path.dirname(os.path.abspath(__file__)) 

#defining the directory where the Jinja2 templates are located
template_dir = os.path.join(script_dir, '../html_files')

#initializing the Jinja2 environment with the template directory
env = Environment(loader=FileSystemLoader(template_dir))

#loading the specific template file to be used for rendering the HTML
template = env.get_template('index_src.html')

#rendering the template with the categorized data to generate the final HTML content
result_html = template.render(categorized_data)

#defining the output path for the generated HTML file
output_path = os.path.join(script_dir, '../html_files/index.html')

#writing the rendered HTML content to the specified output file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(result_html)

print(f"File successfully generated in: {os.path.abspath(output_path)}")
