NbNaturalPersonsArray = [1000, 2000, 3000, 4000, 5000]
ErrorRateArray = [0, 0.5, 1]

for nb in NbNaturalPersonsArray:
    for errorRate in ErrorRateArray:
        datafilename = "data_" + str(nb) + "_ER-" + str(errorRate) + ".ttl"
        datafile = open(datafilename, mode="w")
        datafile.write("_:EmployerDeclaration <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://kg.socialsecurity.be/ont/dmfa#EmployerDeclaration>.")
        iterNaturalPerson = 1
        for i in range(nb):
            datafile.write("""
_:EmployerDeclaration <http://kg.socialsecurity.be/ont/dmfa#R_90007_90017> _:NaturalPerson{0}.
_:NaturalPerson{0} <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://kg.socialsecurity.be/ont/dmfa#NaturalPerson>.
_:NaturalPerson{0} <http://kg.socialsecurity.be/ont/dmfa#NaturalPersonSequenceNbr> "{1}"^^<http://www.w3.org/2001/XMLSchema#integer>.
""".format(i, iterNaturalPerson))
            if i >= errorRate * nb - 1:
                iterNaturalPerson += 1