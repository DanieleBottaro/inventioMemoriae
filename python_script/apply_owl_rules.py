from rdflib import Graph

DATA_GRAPH  = "../rdf_dataset/inme_graph.ttl"
OWL_RULES   = "../rdf_dataset/owl_rules.ttl"
OUTPUT_FILE = "../rdf_dataset/inme_graph_pre_reasoning.ttl"

#load the RDF data graph generated from the source XML/JSON files
data_graph = Graph()
data_graph.parse(DATA_GRAPH, format="turtle")
print(f"Data graph loaded: {len(data_graph)} triples  ({DATA_GRAPH})")

#load the OWL axioms defined in Protégé and stored separately from the instance data
rules_graph = Graph()
rules_graph.parse(OWL_RULES, format="turtle")
print(f"OWL rules loaded: {len(rules_graph)} triples  ({OWL_RULES})")

#merge the two graphs into a single one ready for the external reasoner (HermiT/Pellet)
merged_graph = data_graph + rules_graph
print(f"Merged graph: {len(merged_graph)} triples")

#serialize the merged graph as turtle, then feed this file to Protege for OWL reasoning
merged_graph.serialize(destination=OUTPUT_FILE, format="turtle")
print(f"\nOutput file: {OUTPUT_FILE}")
print("Load it in Protégé, run the reasoner, then export the inferred axioms.")
