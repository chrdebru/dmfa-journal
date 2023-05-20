datafilename = "data.ttl"
datafile = open(datafilename, mode="w")
for i in range(5000):
    datafile.write("""<http://www.example.org/Node> <http://www.example.org/ActivityWithRisk> "{}"^^<http://www.w3.org/2001/XMLSchema#integer>.\n""".format(i))

    # /!\ should add the annex6