datafilename = "data.ttl"
datafile = open(datafilename, mode="w")
for i in range(1000,6000):
    datafile.write("""<http://www.example.org/Node> <http://www.example.org/number> "{}"^^<http://www.w3.org/2001/XMLSchema#integer>.\n""".format(i))
