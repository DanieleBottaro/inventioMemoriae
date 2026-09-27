import json
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD


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

#creating a dictionary that contains...............
ns_dict = {
    "crm": CRM, "arco": ARCO, "arco-cd": ARCO_CD, "dcterms": DCTERMS, "icon": ICON, "lrmoo": LRMOO, "rico": RICO, "inme": INME, "rdf": RDF
    }  

#function used to normalize the URIs
def normalize_uri(value:str):
    if ":" not in value and "#" not in value:
        return INME[value]
    elif value.startswith('#'):
        value = value[1:]
        return INME[value]
    elif ":" in value and not value.startswith('http'):
        prefix, entity_name = value.split(':', 1)
        if prefix in ns_dict:
            return ns_dict[prefix][entity_name]

#helper function to process timespans
def process_time_span(db_graph, subj_uri, date_dict, is_bibl:bool):

    #creating a new triple with subject composed by the uri of the subject we want to express the timespan adding "_time" at the end
    timespan_uri = URIRef(f"{subj_uri}_time")
    db_graph.add((timespan_uri, RDF.type, CRM["E52_Time-Span"]))

    #if the entity is a literary work, proceed creating specific triples. Otherwise (in case of events) just add a triple connecting the subject to its timespan entity
    if is_bibl:
        creation_uri = URIRef(f"{subj_uri}_creation")
        db_graph.add((creation_uri, RDF.type, LRMOO["F27_Work_Creation"]))
        db_graph.add((creation_uri, LRMOO["R16_created"], subj_uri))        
        db_graph.add((creation_uri, CRM["P4_has_time-span"], timespan_uri))
    else:
        db_graph.add((subj_uri, CRM["P4_has_time-span"], timespan_uri))

    #iterating through the dictionary (that contains the type of the date as key and the date as value)
    for date_type, date_val in date_dict.items():

        if len(date_val) == 4:
            datatype = XSD.gYear
        else:
            datatype = XSD.date

        #creating different conditions with specific triples created for each possible type of date
        if date_type == "when":
            db_graph.add((timespan_uri, CRM["P82_at_some_time_within"], Literal(date_val, datatype=datatype)))
        elif date_type in ["from", "notBefore"]:
            db_graph.add((timespan_uri, CRM["P82a_begin_of_the_begin"], Literal(date_val, datatype=datatype)))
        elif date_type in ["to", "notAfter"]:
            db_graph.add((timespan_uri, CRM["P82b_end_of_the_end"], Literal(date_val, datatype=datatype)))
        
#function for parsing the extra entities defined in the json file
def parse_json_data(json_filepath):

    #opening and loading the json file  
    with open(json_filepath, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    #creating a dictionary to store the entities with the id as key and the whole entity as value
    json_entities_db = dict()

    #creating a list of lists to store all of the relations
    json_relations = []

    #iterating through the entities, for each one of them create a separate dictionary with its data and storing it in the json_entities_db with the id of the entity as key
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

    #iterating through the relations defined in the json file and adding them as a list of 3 elements: subject, object and predicate
    for relation in json_data["relations"]:
        subject = relation["subject"]["id"]
        predicate = relation["predicate"]
        object = relation["object"]["id"]
        json_relations.append([subject, predicate, object])

        if relation["object"]["source"] == "extra" and object not in json_entities_db:
            print(f"ATTENTO: QUESTA {relation} NON E' SALVATA SUL JSON")
            
        if relation["subject"]["source"] == "extra" and subject not in json_entities_db:
            print(f"ATTENTO: QUESTA {relation} NON E' SALVATA SUL JSON")

    return json_entities_db, json_relations


#function for parsing the entities defined in the xml/TEI file
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
        #looping through the tei persName tags and saving them as label with the respective language (if not present, the labels will be)
        for pers_name in person.findall("tei:persName", xml_ns):

            language = pers_name.get(check_lang)

            if not language:
                pers_names_dict["en"] = pers_name.text
                pers_names_dict["it"] = pers_name.text
            else:
                pers_names_dict[language] = pers_name.text

        core_entity.update({"label":pers_names_dict})

        #creating a dictionary for the multilingual descriptions of each entity to be later added to the dictionary as "description" containing the information of each one of the entities
        descriptions_dict = dict()
        for description in person.findall("tei:note", xml_ns):

            language = description.get(check_lang)

            descriptions_dict[language] = description.text

        core_entity.update({"description":descriptions_dict})

        #creating a dictionary for the authority control (wikidata and viaf) of each entity to be later added to the dictionary containing the information of each one of the entities
        external_links = dict()

        for idno in person.findall("tei:idno", xml_ns):
            
            if idno.get('type').lower() == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type').lower() == "viaf":
                external_links["viaf"] = "https://viaf.org/en/viaf/" + idno.text
            else:
                external_links[idno.get('type')] = idno.text


        core_entity.update({"external_links":external_links})

        #appending the dictionary containing all of the informations of each entity to the dictionary containing all of the entities described in the xml/TEI file

        core_entities_db[core_entity["id"]] = core_entity

    # =========== ORGANIZATIONS =====================

    #looping through each organization element described in the xml/TEI file
    for organization in root.findall('.//tei:org', xml_ns):

        org_id = organization.get(id_node)

        #initializing the dictionary of the current entity with its id
        core_entity = {"id":org_id}

        #creating a list for storing the alternative names of the organizations
        alias_list = []
        org_names_dict = dict()

        #looping all the various names an organization could have, storing the standard one as label, the others are stored in a dictionary
        for org_name in organization.findall("tei:orgName", xml_ns):

            language = org_name.get(check_lang)
            name_type = org_name.get('type')

            if name_type == "standard" or name_type== "official" or not name_type:

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

        #looping through each tei:note element and storing its content as value and language as key in a dictionary
        descriptions_dict = dict()
        for description in organization.findall("tei:note", xml_ns):

            language = description.get(check_lang)

            descriptions_dict[language] = description.text


        core_entity.update({"description":descriptions_dict})

        #looping through the tei:idno values and storing them in the external_links dictionary with the type of authority control as key
        external_links = dict()
        
        for idno in organization.findall("tei:idno", xml_ns):
            if idno.get('type').lower() == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type').lower() == "viaf":
                external_links["viaf"] = "https://viaf.org/en/viaf/" + idno.text
            else:
                external_links[idno.get('type')] = idno.text

        core_entity.update({"external_links": external_links})
        
        #finally adding the entity to the dictionary storing all the core entities
        core_entities_db[core_entity["id"]] = core_entity

    # =========== OBJECTS =====================

    #looping through each tei:object tag to store the artifacts entities
    for artwork in root.findall(".//tei:object", xml_ns):

        artwork_id = artwork.get(id_node)

        #creating a dictionary for each entity adding the id right away
        core_entity = {"id": artwork_id}

        #creating a list to store the various names an artwork could be known
        alias_list = []
        artwork_names_dict = dict()

        #looping through each artwork name, checking each type and storing each alternative name other than "preferred" in a dictionary and then added to a list of dictionaries containing all the different alternative names for that artwork
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
            if idno.get('type').lower() == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type').lower() == "viaf":
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

    # ========== LITERARY WORKS ==============
    for literary_work in root.findall('.//tei:bibl', xml_ns):

        #if present, extract the data of the constituent for official records
        if literary_work.get('type') == "official_record":
        
            related_works = literary_work.findall('.//tei:relatedItem', xml_ns)

            constituents = []
            for item in related_works:
                if item.get('type') == "constituent":

                    inner_bibl = item.find('.//tei:bibl', xml_ns)
                    constituent_data = {
                        "id": inner_bibl.get(id_node),
                        "title": inner_bibl.find("tei:title", xml_ns).text,
                        "languages": [inner_bibl.find("tei:textLang", xml_ns).get("mainLang")],
                    }

                    const_titles_dict = dict()
                    for const_title in inner_bibl.findall("tei:title", xml_ns):
                        print(const_title.text)
                        language = const_title.get(check_lang)
            
                        if language:
                            const_titles_dict[language] = const_title.text
            
                    constituent_data.update({"label": const_titles_dict})
                                
                    const_date_dict = dict()

                    time_attributes = ["when", "from", "to", "notBefore", "notAfter"]

                    date_node = inner_bibl.find("tei:date", xml_ns)

                    if date_node is not None:
                        for attribute in time_attributes:
                            date_value = date_node.get(attribute)
                            if date_value:
                                const_date_dict[attribute] = date_value
            
                    if const_date_dict:
                        constituent_data.update({"date":const_date_dict})

                    const_desc_dict = dict()
                    for note in item.findall("tei:note", xml_ns):
                        language = note.get(check_lang)                        
                        const_desc_dict[language] = note.text

                    constituent_data.update({"description":const_desc_dict})

                    const_external_links = dict()

                    for idno in inner_bibl.findall("tei:idno", xml_ns):

                        if idno.get('type').lower() == "wikidata":
                            const_external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
                        elif idno.get('type').lower() == "viaf":
                            const_external_links["viaf"] = "https://viaf.org/en/viaf/" + idno.text
                        elif idno.get('type').lower() == "bhl":
                            const_external_links["bhl"] = "urn:clavis:bhl:" + idno.text
                        else:
                            const_external_links[idno.get('type')] = idno.text

                    constituent_data.update({"external_links": const_external_links})

                    constituents.append(constituent_data)
                
                core_entity.update({"constituents":constituents})

                core_entities_db[core_entity["id"]] = core_entity

        work_id = literary_work.get(id_node)

        core_entity = {"id": work_id}

        #put a sort of label in order to recognize literary works when populating the graph
        core_entity["type"] = "Literary work"

        work_titles_dict = dict()
        
        for work_title in literary_work.findall("tei:title", xml_ns):
            

            language = work_title.get(check_lang)

            if language:
                work_titles_dict[language] = work_title.text

        core_entity.update({"label": work_titles_dict})

        work_authors_list = []
        for author in literary_work.findall("tei:author", xml_ns):

            author_id = author.get("ref")
            
            if author_id:
                work_authors_list.append(author_id)

        core_entity.update({"authors": work_authors_list})

        all_languages = []
        for language in literary_work.findall("tei:textLang", xml_ns):

            main_lang = language.get("mainLang")
            if main_lang:
                all_languages.append(main_lang)

            other_lang = language.get("otherLangs")
            if other_lang:
                all_languages.extend(other_lang.split(" "))

        core_entity.update({"languages": all_languages})

        date_dict = dict()
        
        time_attributes = ["when", "from", "to", "notBefore", "notAfter"]

        date_tag = literary_work.find(".//tei:date", xml_ns)

        if date_tag is not None:
            for attribute in time_attributes:
                date_value = date_tag.get(attribute)
                if date_value:
                    date_dict[attribute] = date_value

        if date_dict:
            core_entity.update({"date":date_dict})
        

        descriptions_dict = dict()
        
        for description in literary_work.findall("tei:note", xml_ns):

            language = description.get(check_lang)

            descriptions_dict[language] = description.text

        core_entity.update({"description":descriptions_dict})

        external_links = dict()
        
        for idno in literary_work.findall("tei:idno", xml_ns):
            if idno.get('type').lower() == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type').lower() == "viaf":
                external_links["viaf"] = "https://viaf.org/en/viaf/" + idno.text
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
                
            if idno.get('type').lower() == "wikidata":
                external_links["wikidata"] = "https://www.wikidata.org/wiki/" + idno.text
            elif idno.get('type').lower() == "viaf":
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

        #checking if it's a literary work
        if entity_data.get("type") == "Literary work":

            
            bibl_waiting_list = [entity_data]

            while bibl_waiting_list:

                current_entity = bibl_waiting_list.pop(0)

                subj_uri = normalize_uri(current_entity["id"])

                title_value = current_entity["label"]
                for lang_title, title in title_value.items():
                    db_graph.add((subj_uri, RDFS.label , Literal(title, lang = lang_title)))
                    db_graph.add((subj_uri, DCTERMS.title , Literal(title, lang = lang_title)))

                authors = current_entity.get("authors")

                if authors is not None:
                    for author in authors:
                        author = normalize_uri(author)
                        db_graph.add((subj_uri, DCTERMS.creator , URIRef(author)))

                languages = current_entity.get("languages")
                for lang in languages:
                    db_graph.add((subj_uri, DCTERMS.language, Literal(lang)))

                date_dict = current_entity.get("date")

                if date_dict:
                    process_time_span(db_graph, subj_uri, date_dict, True)

                desc_value = current_entity.get("description")

                for lang_desc, desc in desc_value.items():
                    db_graph.add((subj_uri, DCTERMS.description , Literal(desc, lang = lang_desc)))

                aut_cont_value = current_entity.get("external_links")
                
                for aut_code_type, aut_code in aut_cont_value.items():
                    if aut_code_type == "viaf":
                        db_graph.add((subj_uri,  SKOS.exactMatch, URIRef(aut_code)))
                    
                    elif aut_code_type == "wikidata":
                        db_graph.add((subj_uri, OWL.sameAs, URIRef(aut_code)))

                    elif aut_code_type == "bhl":
                        db_graph.add((subj_uri, RICO.hasResourceAssociatedWithSource, URIRef(aut_code)))

                if "constituents" in current_entity:
                    for constituent in current_entity["constituents"]:
                        bibl_waiting_list.append(constituent)

                        constituent_uri = normalize_uri(constituent["id"])
                        db_graph.add((subj_uri, RICO.hasPart, constituent_uri))

        else:
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


            date_dict = entity_data.get("date")
            if date_dict:
                process_time_span(db_graph, subj_uri, date_dict, False)

            alt_names = entity_data.get("alias")

            if alt_names:
                for alt_name in alt_names:
                    name = alt_name.get("name")
                    name_lang = alt_name.get("lang")

                    if name_lang == "unknown" or not name_lang:
                        db_graph.add((subj_uri, SKOS.altLabel, Literal(name)))
                    else:
                        db_graph.add((subj_uri, SKOS.altLabel, Literal(name, lang=name_lang)))


            
    for relation in relations:
        subj = normalize_uri(relation[0])
        pred = normalize_uri(relation[1])
        obj = normalize_uri(relation[2])
        db_graph.add((subj, pred, obj))


    return db_graph

def main():

    json_filepath = "../xml_json_files/inMe_extra_entities.json"
    xml_filepath = "../xml_json_files/inMe_TEI.xml"
    output_filepath = "../rdf_dataset/inventio_memoriae_graph2.ttl"

    # 1. Estrazione JSON
    json_entities, json_relations = parse_json_data(json_filepath)

    # 2. Estrazione XML
    xml_entities, xml_relations = parse_tei_xml(xml_filepath)

    
    print(len(json_entities))
    print(len(xml_entities))
    # 3. Unione dei dati
    all_entities_db = json_entities.copy()
    all_entities_db.update(xml_entities)
    print(len(all_entities_db))

    all_relations = json_relations.copy()
    all_relations.extend(xml_relations)

    # 4. Inizializzazione e popolamento Grafo
    db_graph, ns_dict = setup_rdf_graph()
    db_graph = populate_graph(db_graph, all_entities_db, all_relations)

    # 5. Output
    
    db_graph.serialize(destination=output_filepath, format="turtle", encoding="utf-8") # Consigliato!


if __name__ == "__main__":
    main()