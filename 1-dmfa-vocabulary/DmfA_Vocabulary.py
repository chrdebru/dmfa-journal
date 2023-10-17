import csv
import re

import sys
sys.path.append("../")
from helper import *

#TODO think of range of dataproperties

outfile = open("DmfA_Vocabulary.ttl", "w", encoding="utf-8")

# HEADER
# TODO maybe change ontology namespace
outfile.write("""
@prefix : <http://kg.socialsecurity.be/ont/dmfa#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dc: <http://purl.org/dc/terms/#> .
@base <http://kg.socialsecurity.be/ont/dmfa#> .

<http://kg.socialsecurity.be/ont/dmfa#> rdf:type owl:Ontology .
""")

# TODO modify definition
outfile.write("""
:length a owl:AnnotationProperty;
    rdfs:label "length"@en, "longueur"@fr, "lengte"@nl;
    rdfs:comment "La longueur renseignée est la longueur maximale de la donnée."@fr 
.

:presence a owl:AnnotationProperty;
    rdfs:label "presence"@en, "présence"@fr, "aanwezigheid"@nl;
    rdfs:comment \"\"\"La présence d'une donnée dans un bloc fonctionnel ou niveau peut être :
Facultative : L'expéditeur est libre de remplir cette zone.
Obligatoire si : La zone doit être présente si les conditions mentionnées sont remplies.
Indispensable : La zone doit toujours être présente.\"\"\"@fr 
.

:type a owl:AnnotationProperty;
    rdfs:label "type"@en, "type"@fr, "type"@nl;
    rdfs:comment \"\"\"Le type de donnée indique si la donnée contient des signes numériques (uniquement des chiffres) ou alphanumériques (chiffres, lettres MAJUSCULES, signes spéciaux).
Les caractères autres que les majuscules seront traduits en majuscules. De même certains signes spéciaux seront traduits selon la table en annexe 8 du glossaire DIMONA. Les autres caractères ne se trouvant pas dans cette table seront traduits par un blanc (ASCII Hex 20).\"\"\"@fr 
.
""")


domainDict = {}

# Classes - Entities
# TODO think of presence, card,...
rootBFxml = xmlRoot('VersCplt_BFdmfa20223FR.xml', encoding="utf-8")
for bf in rootBFxml:

    className = bf.find("XmlLabel").text
    identifier = bf.find("Code").text
    labelEn = re.sub(r"(\w)([A-Z])", r"\1 \2", className)
    labelFr = bf.find("Nom").text
    commentFr = addTripleQuotes(bf.find("Description").text)
    presenceFr = addTripleQuotes(bf.find("Presence").text)

    strToWrite = ""
    strToWrite = appendIfNotNone(strToWrite, ':{} a owl:Class;', className)
    strToWrite = appendIfNotNone(strToWrite, 'dc:identifier "{}";', identifier)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:label "{}"@en;', labelEn)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:label "{}"@fr;', labelFr)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:comment {}@fr;', commentFr)
    strToWrite = appendIfNotNone(strToWrite, ':presence {}@fr;', presenceFr)

    outfile.write(strToWrite + "\n .")

    attributes = bf.findall("Zones")
    for att in attributes:
        if att.text:
            key = att.text.split(' ', 1)[0]
            if key not in domainDict.keys():
                domainDict[key] = [":" + className]
            else:
                domainDict[key].append(":" + className)


rootBFxml = xmlRoot('VersCplt_FBdmfa20223NL.xml', encoding="utf-8")
for bf in rootBFxml:

    className = bf.find("XmlLabel").text
    labelNl = bf.find("Naam").text
    commentNl = addTripleQuotes(bf.find("Omschrijving").text)
    presenceNl = addTripleQuotes(bf.find("Aanwezigheid").text)

    strToWrite = ""
    strToWrite = appendIfNotNone(strToWrite, ':{} ', className)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:label "{}"@nl;', labelNl)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:comment {}@nl;', commentNl)
    strToWrite = appendIfNotNone(strToWrite, ':presence {}@nl;', presenceNl)

    outfile.write(strToWrite + "\n .")

# DatatypeProperties - Attributes

visited = []
rootZones = xmlRoot('VersCpltdmfa20223FR.xml', "utf-8")
for zone in rootZones:

    DPName = zone.find("LabelXml").text
    identifier = zone.find("Code").text
    labelEn = re.sub(r"(\w)([A-Z])", r"\1 \2", DPName)
    labelFr = zone.find("Title").text
    commentFr = addTripleQuotes(zone.find("Description").text)
    presenceFr = addTripleQuotes(zone.find("Presence").text)
    isDefinedByFr = addTripleQuotes(zone.find("DomaineDeDefinition").text)

    # The original code contained a bug where multiple yet redundant domain declarations were added
    # Fixed with some memoisation
    # Also simplified approach when there is only one class
    if len(domainDict[identifier]) == 1:
        domain = domainDict[identifier][0]
    else:
        if identifier not in visited:
            domain = """
                    [ a owl:Class ;
                        owl:unionOf ({})
                    ]
            """.format(" ".join(domainDict[identifier]))
            visited.append(identifier)
        else:
            domain = None
    
    length = zone.find("Longueur").text
    typeFr = addTripleQuotes(zone.find("Type").text)

    strToWrite = ""
    strToWrite = appendIfNotNone(
        strToWrite, ':{} a owl:DatatypeProperty;', DPName)
    strToWrite = appendIfNotNone(strToWrite, 'dc:identifier "{}";', identifier)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:label "{}"@en;', labelEn)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:label "{}"@fr;', labelFr)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:comment {}@fr;', commentFr)
    strToWrite = appendIfNotNone(strToWrite, ':presence {}@fr;', presenceFr)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:domain {};', domain)
    strToWrite = appendIfNotNone(
        strToWrite, 'rdfs:isDefinedBy {}@fr;', isDefinedByFr)
    strToWrite = appendIfNotNone(strToWrite, ':length {};', length)
    strToWrite = appendIfNotNone(strToWrite, ':type {}@fr;', typeFr)

    outfile.write(strToWrite + "\n.\n")

rootZones = xmlRoot('VersCpltdmfa20223NL.xml', "utf-8")
for zone in rootZones:

    DPName = zone.find("XmlLabel").text
    labelnl = zone.find("Titel").text
    commentnl = addTripleQuotes(zone.find("Omschrijving").text)
    presencenl = addTripleQuotes(zone.find("Aanwezigheid").text)
    isDefinedBynl = addTripleQuotes(zone.find("ToegelatenDomein").text)

    
    length = zone.find("Lengte").text
    typeFr = addTripleQuotes(zone.find("Type").text)

    strToWrite = ""
    strToWrite = appendIfNotNone(
        strToWrite, ':{} ', DPName)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:label "{}"@nl;', labelnl)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:comment {}@nl;', commentnl)
    strToWrite = appendIfNotNone(strToWrite, ':presence {}@nl;', presencenl)
    strToWrite = appendIfNotNone(strToWrite, 'rdfs:isDefinedBy {}@nl;', isDefinedBynl)
    strToWrite = appendIfNotNone(strToWrite, ':length {};', length)
    strToWrite = appendIfNotNone(strToWrite, ':type {}@nl;', typeFr)

    outfile.write(strToWrite + "\n.\n")

# ObjectProperties - Relation
# CSV file should have been generated with DmfA_Relation_Base.py and annotated
relationCSV = open("Dmfa_Relation.csv", encoding="utf-8")
relationTable = csv.reader(relationCSV, delimiter=",") # From,To,Domain,Range,LabelFr
next(relationTable, None)

for row in relationTable:

    relationName = "R_" + row[0] + "_" + row[1]
    labelFr, labelNl, labelEn = row[4], row[5], row[6]
    domain = row[2]
    range = row[3]

    outfile.write("""
    :{} a owl:ObjectProperty;
        rdfs:label "{}"@fr, "{}"@nl, "{}"@en;
        rdfs:domain :{};
        rdfs:range :{};
    .
    """.format(relationName, labelFr, labelNl, labelEn, domain, range))

relationCSV.close()

outfile.close()

from rdflib import Graph
g = Graph()
g.parse("DmfA_Vocabulary.ttl", format="ttl")
print(len(g))

g.serialize(destination="DmfA_Vocabulary.ttl", format="ttl")
