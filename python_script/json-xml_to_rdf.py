import json
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL


CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
ARCO = Namespace("https://w3id.org/arco/ontology/arco/")
ARCO_CD = Namespace("https://w3id.org/arco/ontology/content-description/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
FABIO = Namespace("http://purl.org/spar/fabio/")
ICON = Namespace("http://www.w3id.org/icon/ontology/")
LRMOO = Namespace("http://iflastandards.info/ns/lrm/lrmoo/")
RICO = Namespace("http://www.ica.org/standards/RiC/ontology/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

INME = Namespace("http://example.org/inventio-memoriae/")

ns_dict = {
    "crm": CRM, "arco": ARCO, "arco-cd": ARCO_CD, "dcterms": DCTERMS, "fabio": FABIO, "icon": ICON, "lrmoo": LRMOO, "rico": RICO, "inme": INME, "rdf": RDF
    }  

def normalize_uri(value:str):
    if ":" not in value:
        return INME[value]
    elif ":" in value and not value.startswith('http'):
        prefix, entity_name = value.split(':', 1)
        if prefix in ns_dict:
            return ns_dict[prefix][entity_name]


def parse_json_data(json_filepath):

    #opening and loading the json file  
    with open(json_filepath, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    #creating a dictionary to store the entities with the id as key and the whole entity as value
    json_entities_db = dict()

    #creating a list of lists to store all of the relations
    json_relations = []


    for entity in json_data["extra_entities"]:
        entity_to_add = {"id": entity["id"], "label": entity["label"], "description": entity["description"], "external_links": entity["external_links"]}

        if "date" in entity:
            entity_to_add["date"] = entity["date"]

        json_entities_db[entity["id"]] = entity_to_add

    #since the json entities contain "ontological_classes" element in which are contained the classes they belong to, I add them to the json_relations using rdf:type as predicate
    for entity in json_data["extra_entities"]:

        for class_type in entity["ontological_classes"]:
            subject = entity["id"]
            predicate = "rdf:type"
            object = class_type

            json_relations.append([subject, predicate, object])

    for relation in json_data["relations"]:
        subject = relation["subject"]["id"]
        predicate = relation["predicate"]
        object = relation["object"]["id"]

    if relation["object"]["source"] == "extra" and object not in json_entities_db:
        print(f"ATTENTO: QUESTA {relation} NON E' SALVATA SUL JSON")
        
    if relation["subject"]["source"] == "extra" and subject not in json_entities_db:
        print(f"ATTENTO: QUESTA {relation} NON E' SALVATA SUL JSON")

    
    json_relations.append([subject, predicate, object])

    return json_entities_db, json_relations


def parse_tei_xml(xml_filepath):
    #loading the xml file
    tree = ET.parse(xml_filepath)

    #extracting the root of the file
    root = tree.getroot()

    #creating a dictionary to store the dictionaries describing the entities defined in the xml/tei file using the id of the entity as a key
    core_entities_db = dict()

    xml_ns = {"tei":"http://www.tei-c.org/ns/1.0","xml": "http://www.w3.org/XML/1998/namespace"}

    id_node = f"{{{xml_ns['xml']}}}id"
    check_lang = f"{{{xml_ns['xml']}}}lang"

    # =========== PEOPLE =====================

    #looping through each tei:person tag to store the person entities
    for person in root.findall('.//tei:person', xml_ns):
        
        person_id = person.get(id_node)

        #creating a dictionary for each entity adding the id right away
        core_entity = {"id": person_id}
        
        #creating a dictionary for the italian and english names of each entity to be later added to the dictionary containing the information of each one of the entities
        pers_names_dict = dict()
        for pers_name in person.findall("tei:persName", xml_ns):

            language = pers_name.get(check_lang)

            if not language:
                pers_names_dict["en"] = pers_name.text
                pers_names_dict["it"] = pers_name.text
            else:
                pers_names_dict[language] = pers_name.text

        core_entity.update({"label":pers_names_dict})

        #creating a dictionary for the multilingual descriptions of each entity to be later added to the dictionary containing the information of each one of the entities
        descriptions_dict = dict()
        for description in person.findall("tei:note", xml_ns):

            language = description.get(check_lang)

            descriptions_dict[language] = description.text

        core_entity.update({"description":descriptions_dict})

        #creating a dictionary for the authority control (wikidata and viaf) of each entity to be later added to the dictionary containing the information of each one of the entities
        external_links = dict()

        for idno in person.findall("tei:idno", xml_ns):
            
            if idno.get('type') == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type') == "viaf":
                external_links["viaf"] = "https://viaf.org/en/viaf/" + idno.text
            else:
                external_links[idno.get('type')] = idno.text


        core_entity.update({"external_links":external_links})

        #appending the dictionary containing the information of each entity to the list containing the dictionary describing each entity

        core_entities_db[core_entity["id"]] = core_entity

    # =========== ORGANIZATIONS =====================

    for organization in root.findall('.//tei:org', xml_ns):

        org_id = organization.get(id_node)

        core_entity = {"id":org_id}

        alias_list = []
        org_names_dict = dict()

        for org_name in organization.findall("tei:orgName", xml_ns):

            language = org_name.get(check_lang)
            name_type = org_name.get('type')

            if name_type == "standard" or not name_type:

                if not language:
                    org_names_dict["en"] = org_name.text
                    org_names_dict["it"] = org_name.text
                else:
                    org_names_dict[language] = org_name.text

            else:

                other_name = {
                    "name": org_name.text,
                    "type": name_type,
                    "lang": language if language else "unknown"
                }
                alias_list.append(other_name)
            core_entity.update({"label": org_names_dict})

            if alias_list:
                core_entity.update({"alias": alias_list})


        descriptions_dict = dict()
        for description in organization.findall("tei:note", xml_ns):

            language = description.get(check_lang)

            descriptions_dict[language] = description.text


        core_entity.update({"description":descriptions_dict})

        external_links = dict()

        for idno in organization.findall("tei:idno", xml_ns):
            if idno.get('type') == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type') == "viaf":
                external_links["viaf"] = "https://viaf.org/en/viaf/" + idno.text
            else:
                external_links[idno.get('type')] = idno.text

        core_entity.update({"external_links": external_links})
        

        core_entities_db[core_entity["id"]] = core_entity

    # =========== OBJECTS =====================

    for artwork in root.findall(".//tei:object", xml_ns):

        artwork_id = artwork.get(id_node)

        core_entity = {"id": artwork_id}

        alias_list = []
        artwork_names_dict = dict()

        for artwork_name in artwork.findall(".//tei:objectName", xml_ns):

            language = artwork_name.get(check_lang)
            name_type = artwork_name.get('type')

            if name_type == "preferred" or not name_type:
                if not language:
                    artwork_names_dict["en"] = artwork_name.text
                    artwork_names_dict["it"] = artwork_name.text
                else:
                    artwork_names_dict[language] = artwork_name.text

            else:

                other_name = {
                    "name": artwork_name.text,
                    "type": type,
                    "lang": language if language else "unknown"
                }
                alias_list.append(other_name)

        core_entity.update({"label":artwork_names_dict})

        if alias_list:
            core_entity.update({"alias": alias_list})

        descriptions_dict = dict()

        for description in artwork.findall("tei:note", xml_ns):

            language = description.get(check_lang)

            descriptions_dict[language] = description.text

        core_entity.update({"description":descriptions_dict})

        external_links = dict()

        for idno in artwork.findall("tei:idno", xml_ns):
            if idno.get('type') == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type') == "viaf":
                external_links["viaf"] = "https://viaf.org/en/viaf/" + idno.text
            else:
                external_links[idno.get('type')] = idno.text

        core_entity.update({"external_links": external_links})
            
        core_entities_db[core_entity["id"]] = core_entity


    # =========== PLACES =====================

    for place in root.findall(".//tei:place", xml_ns):

        place_id = place.get(id_node)

        core_entity = {"id": place_id}

        place_names_dict = dict()

        for place_name in place.findall("tei:placeName", xml_ns):

            language = place_name.get(check_lang)

            if not language:
                place_names_dict["en"] = place_name.text
                place_names_dict["it"] = place_name.text
            else:
                place_names_dict[language] = place_name.text

        core_entity.update({"label":place_names_dict})

        descriptions_dict = dict()

        for description in place.findall("tei:note", xml_ns):

            language = description.get(check_lang)
            
            descriptions_dict[language] = description.text
            
        core_entity.update({"description":descriptions_dict})

        external_links = dict()

        for idno in place.findall("tei:idno", xml_ns):
                
            if idno.get('type').lower() == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type').lower() == "viaf":
                external_links["viaf"] = "https://viaf.org/en/viaf/" + idno.text
            elif idno.get('type').lower() == "geonames":
                external_links["GeoNames"] = "https://sws.geonames.org/" + idno.text
            else:
                external_links[idno.get('type')] = idno.text
        
        
        core_entity.update({"external_links":external_links})

        core_entities_db[core_entity["id"]] = core_entity

    # =========== EVENTS =====================

    for event in root.findall('.//tei:event', xml_ns):

        event_id = event.get(id_node)

        core_entity = {"id": event_id}

        event_names_dict = dict()
        for event_name in event.findall("tei:label", xml_ns):

            language = event_name.get(check_lang)

            if not language:
                event_names_dict["en"] = event_name.text
                event_names_dict["it"] = event_name.text
            else:
                event_names_dict[language] = event_name.text

        core_entity.update({"label":event_names_dict})

        descriptions_dict = dict()

        for description in event.findall("tei:desc", xml_ns):

            language = description.get(check_lang)

            descriptions_dict[language] = description.text

        core_entity.update({"description":descriptions_dict})

        external_links = dict()

        for idno in event.findall("tei:idno", xml_ns):
                
            if idno.get('type') == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type') == "viaf":
                external_links["viaf"] = "https://viaf.org/en/viaf/" + idno.text
            else:
                external_links[idno.get('type')] = idno.text
        
        core_entity.update({"external_links":external_links})

        date_dict = dict()

        time_attributes = ["when", "from", "to", "notBefore", "notAfter"]

        for attribute in time_attributes:
            date_value = event.get(attribute)
            if date_value:
                date_dict[attribute] = date_value

        if date_dict:
            core_entity.update({"date":date_dict})

        core_entities_db[core_entity["id"]] = core_entity


    xml_relations =  []

    for relation in root.findall('.//tei:relation', xml_ns):
        
        subject = relation.get('active')
        if subject.startswith('#'):
            subject = subject[1:]

        predicate = relation.get('name')
        if predicate.startswith('#'):
            predicate = predicate[1:]

        object = relation.get('passive')
        if object.startswith('#'):
            object = object[1:]

        xml_relations.append([subject, predicate, object])

    #print(xml_relations)

    return core_entities_db, xml_relations


# ======== GRAPH CREATION ================


def setup_rdf_graph():
    db_graph = Graph() 

    db_graph.bind("crm", CRM)
    db_graph.bind("arco", ARCO)
    db_graph.bind("arco-cd", ARCO_CD)
    db_graph.bind("dcterms", DCTERMS)
    db_graph.bind("fabio", FABIO)
    db_graph.bind("icon", ICON)
    db_graph.bind("lrmoo", LRMOO)
    db_graph.bind("rico", RICO)
    db_graph.bind("inme", INME)

    return db_graph, ns_dict


def populate_graph(db_graph, entities_db, relations):

    for entity_id, entity_data  in entities_db.items():
        subj_uri = normalize_uri(entity_id)

        label_value = entity_data["label"]

        for lang_label, label in label_value.items():
            db_graph.add((subj_uri, RDFS.label , Literal(label, lang = lang_label)))
        
        
        desc_value = entity_data["description"]

        for lang_desc, desc in desc_value.items():
            db_graph.add((subj_uri, DCTERMS.description , Literal(desc, lang = lang_desc)))
        

        aut_cont_value = entity_data["external_links"]

        for aut_code_type, aut_code in aut_cont_value.items():
            if aut_code_type == "viaf" or aut_code_type == "iconclass":
                db_graph.add((subj_uri,  SKOS.exactMatch, URIRef(aut_code)))
            
            elif aut_code_type == "wikidata" or aut_code_type == "GeoNames":
                db_graph.add((subj_uri, OWL.sameAs, URIRef(aut_code)))

        #if entity_data["date"] != None:
        #    for date in entity_data["date"].items():

            
    for relation in relations:
        subj = normalize_uri(relation[0])
        pred = normalize_uri(relation[1])
        obj = normalize_uri(relation[2])
        db_graph.add((subj, pred, obj))


    return db_graph

def main():

    json_filepath = "Jsoning_mingus.json"
    xml_filepath = "Mapping_mingus.xml"
    output_filepath = "inventio_memoriae_graph.ttl"

    # 1. Estrazione JSON
    json_entities, json_relations = parse_json_data("Jsoning_mingus.json")

    # 2. Estrazione XML
    xml_entities, xml_relations = parse_tei_xml("Mapping_mingus.xml")

    

    # 3. Unione dei dati
    all_entities_db = json_entities.copy()
    all_entities_db.update(xml_entities)

    all_relations = json_relations.copy()
    all_relations.extend(xml_relations)

    # 4. Inizializzazione e popolamento Grafo
    db_graph, ns_dict = setup_rdf_graph()
    db_graph = populate_graph(db_graph, all_entities_db, all_relations)

    # 5. Output
    
    db_graph.serialize(destination=output_filepath, format="turtle", encoding="utf-8") # Consigliato!


if __name__ == "__main__":
    main()