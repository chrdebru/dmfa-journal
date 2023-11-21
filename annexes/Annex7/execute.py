import morph_kgc

config = """

            [CONFIGURATION]
            output_file: annex7-data.ttl

            [DataSource1]
            mappings: ./mapping.ttl
         """

graph = morph_kgc.materialize(config)

print(len(graph))