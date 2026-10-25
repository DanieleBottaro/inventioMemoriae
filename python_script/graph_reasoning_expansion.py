from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, OWL

db_graph = Graph()
db_graph.parse("../rdf_dataset/inventio_memoriae_graph.ttl", format="turtle")

namespaces = {
    "crm": Namespace("http://www.cidoc-crm.org/cidoc-crm/"),
    "arco": Namespace("https://w3id.org/arco/ontology/arco/"),
    "arco-cd": Namespace("https://w3id.org/arco/ontology/context-description/"),
    "rico": Namespace("https://www.ica.org/standards/RiC/ontology#"),
    "lrmoo": Namespace("http://iflastandards.info/ns/lrm/lrmoo/"),
    "dcterms": Namespace("http://purl.org/dc/terms/"),
    "skos": Namespace("http://www.w3.org/2004/02/skos/core#")
}

for prefix, uri in namespaces.items():
    db_graph.bind(prefix, uri)

obj_property_list = [
    ("rico:relationHasTarget", "rico:thingIsTargetOfRelation"),
    ("crm:P138_represents","crm:P138i_has_representation"),
    ("crm:P53_has_former_or_current_location","crm:P53i_is_former_or_current_location_of"),
    ("crm:P89_falls_within","crm:P89i_contains"),
    ("crm:P123_resulted_in","crm:P123i_resulted_from"),
    ("crm:P124_transformed","crm:P124i_was_transformed_by"),
    ("crm:P107i_is_current_or_former_member_of","crm:P107_has_current_or_former_member"),
    ("arco:hasCulturalPropertyComponent", "arco:isCulturalPropertyComponentOf"),
    ("crm:P14_carried_out_by","crm:P14i_performed"),
    ("arco-cd:hasCommittent","arco-cd:isCommittentIn"),
    ("crm:P46_is_composed_of","crm:P46i_forms_part_of"),
    ("crm:P4_has_time-span","crm:P4i_is_time-span_of"),
    ("arco-cd:hasCommission", "arco-cd:isCommissionOf"),
    ("crm:P65_shows_visual_item","crm:P65i_is_shown_by"),
    ("crm:P7_took_place_at","crm:P7i_witnessed"),
    ("crm:P67_refers_to","crm:P67i_is_referred_to_by"),
    ("crm:P11_had_participant","crm:P11i_participated_in"),
    ("crm:P148_has_component","crm:P148i_is_component_of"),
    ("rico:hasDirectConstituent", "rico:isDirectConstituentOf"),
    ("crm:P94i_was_created_by","crm:P94_has_created"),
    ("crm:P129_is_about","crm:P129i_is_subject_of"),
    ("rico:creationWithRole","rico:roleIsContextOfCreationRelation"),
    ("lrmoo:R68_is_inspired_by","lrmoo:R68i_is_inspiration_for"),
    ("lrmoo:R1_is_logical_successor_of","lrmoo:R1i_has_successor"),
    ("rico:relationHasSource","rico:thingIsSourceOfRelation"),
    ("rico:isOrWasLeaderOf", "rico:hasOrHadLeader"),
    ("dcterms:creator","arco-cd:isAuthorOf"),
    ("lrmoo:R16_created","lrmoo:R16i_was_created_by")
]

def str_to_uri(prop_str:str):
    prefix, name = prop_str.split(":")
    return URIRef(namespaces[prefix] + name)

for direct_prop_str, inverse_prop_str in obj_property_list:

    direct_uri = str_to_uri(direct_prop_str)
    inverse_uri = str_to_uri(inverse_prop_str)
    
    db_graph.add((direct_uri, RDF.type, OWL.ObjectProperty))
    db_graph.add((inverse_uri, RDF.type, OWL.ObjectProperty))

    db_graph.add((direct_uri, OWL.inverseOf, inverse_uri))
    db_graph.add((inverse_uri, OWL.inverseOf, direct_uri))

data_prop_list = [
    "dcterms:language",
    "dcterms:title",
    "crm:P82_at_some_time_within",
    "crm:P82b_end_of_the_end",
    "crm:P82a_begin_of_the_begin",
    "skos:altLabel"
]

for data_prop_str in data_prop_list:
    data_prop_uri = str_to_uri(data_prop_str)

    db_graph.add((data_prop_uri, RDF.type, OWL.DatatypeProperty))

db_graph.serialize(destination="../rdf_dataset/inme_pre_reasoning.ttl", format="turtle")

print("New file ready for Protégé!!")