import morph_kgc

config = """
            [CONFIGURATION]
            
            [DataSource1]
            mappings: ./mapping.ttl
            db_url: duckdb:///:memory:
         """

graph = morph_kgc.materialize(config)

graph.serialize(destination="annex7-data.ttl", format="turtle")