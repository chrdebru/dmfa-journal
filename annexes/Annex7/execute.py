import morph_kgc

config = """
            [CONFIGURATION]
            udfs: ../functions.py
            
            [DataSource1]
            mappings: ./mapping.ttl
         """

graph = morph_kgc.materialize(config)

print(len(graph))

graph.serialize(destination="annex7-data.ttl", format="turtle")