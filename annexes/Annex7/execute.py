import morph_kgc

config = """
            [CONFIGURATION]
            
            [DataSource1]
            mappings: ./annex7-mapping.ttl
            db_url: duckdb:///:memory:
         """

graph = morph_kgc.materialize(config)

graph.serialize(destination="annex7-data.ttl", format="turtle")