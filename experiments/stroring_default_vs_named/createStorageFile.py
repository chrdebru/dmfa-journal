import re

defaultStorageFilename = "storageDefault.nq"
namedStorageFilename = "storageNamed.nq"

defaultStorageFile = open(defaultStorageFilename, "w", encoding="utf-8")
namedStorageFile = open(namedStorageFilename, "w", encoding="utf-8")

for i in range (1000):
    declaration = open("dmfa.ttl", "r", encoding="utf-8")
    ref = str(i).zfill(3)
    for line in declaration.readlines():
        lineMod = re.sub(r"urn:ss:000", "urn:ss:" + ref, line)
        defaultStorageFile.write(lineMod)
        namedStorageFile.write(lineMod[:-2] + " <urn:ss:"+ ref + ">.\n")
    