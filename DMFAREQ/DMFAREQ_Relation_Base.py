import csv

import sys
sys.path.append("../")
from helper import *

relationData = [] # [[From, To, Domain, Range]]
classIdentifierDict = {}

rootBFxml = xmlRoot('VersCplt_BFDMFAREQ20223FR.xml', encoding="iso-8859-1")
for bf in rootBFxml:

    className = bf.find("XmlLabel").text
    identifier = bf.find("Code").text
    classIdentifierDict[identifier] = className
    
    tos = bf.findall("NrBlocLie")
    if tos[0].text != None:
        for to in tos:        
            relationData.append([identifier, to.text, className])

for row in relationData:
    row.append(classIdentifierDict[row[1]])

outfile = open("DMFAREQ_Relation_Base.csv","w", newline='')
writer = csv.writer(outfile)
writer.writerow(["From", "To", "Domain", "Range"])
writer.writerows(relationData)
outfile.close()