import sys
sys.path.append("../")
from helper import *

outfile = open("shapes_base.ttl", "w")

outfile.write("""
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xs: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ont: <http://kg.socialsecurity.be/ont/dmfa#> .

@prefix kg: <http://kg.socialsecurity.be/resource/shapes/> .
@base <http://kg.socialsecurity.be/resource/shapes/> .

<> 
	sh:declare [
		sh:prefix "xs" ;
		sh:namespace "http://www.w3.org/2001/XMLSchema#"^^xs:anyURI ;
	] ;

	sh:declare [
		sh:prefix "ont" ;
		sh:namespace "http://kg.socialsecurity.be/ont/dmfa#"^^xs:anyURI ;
	] ;
.

kg:DmfAOriginalCountInstancesShape a sh:NodeShape ;
    rdfs:comment "A graph should have exactly one instance of ont:DmfAOriginal" ;
    sh:targetNode ont:DmfAOriginal ;

    sh:property [
        sh:message "Graph does not contain exactly one instance of ont:DmfAOriginal" ;
        sh:path [ sh:inversePath rdf:type ] ;
        sh:maxCount 1 ;
        sh:minCount 1 ;
    ] ;
.
""")

rootBFxml = xmlRoot("../DMFA/VersCplt_BFdmfa20223FR.xml", encoding="iso-8859-1")
rootDmfaXsd = xmlRoot("../DMFA/DmfAOriginal_20223.xsd", encoding="utf-8")
elementsDmfaXsd = rootDmfaXsd.findall("./{*}element")

codeDict = {}
for bf in rootBFxml:
    codeDict[bf.find("Code").text] = bf

attributesDone = set()

bfToVisit = [([], "90169")]

def writeBFShape(path, BFcode):
    bfToWrite = codeDict[BFcode]
    className = bfToWrite.find("XmlLabel").text

    outfile.write("""
kg:{0}Shape a sh:NodeShape ;
    rdfs:comment "Property Shape for {0} ({1})" ;
    sh:targetClass ont:{0} ;
""".format(className, BFcode))

    attributes = bfToWrite.findall("Zones")
    attributesToWrite = []
    for att in attributes:
        if att.text:
            code = att.text.split(' ', 1)[0]
            element = [element for element in elementsDmfaXsd if element.find(
                ".//{*}documentation").text == code][0]

            DPName = element.attrib["name"]
            outfile.write("""
    sh:property kg:{}Shape;""".format(DPName))

            if code not in attributesDone:
                attributesToWrite.append(code)

    outfile.write("\n.\n")

    for attributeCode in attributesToWrite:
        element = [element for element in elementsDmfaXsd if element.find(
            ".//{*}documentation").text == attributeCode][0]

        DPName = element.attrib["name"]
        datatype = element.find(".//{*}restriction").attrib["base"]

        def find(path):
            if element.find(path) != None:
                return element.find(path).attrib["value"]
            return None

        minInclusive = find(".//{*}minInclusive")
        maxInclusive = find(".//{*}maxInclusive")
        if datatype == "xs:date":
            if minInclusive != None:
                minInclusive = '"' + minInclusive + '"'
            if maxInclusive != None:
                maxInclusive = '"' + maxInclusive + '"'
        minLength = find(".//{*}minLength")
        maxLength = find(".//{*}maxLength")
        totalDigits = find(".//{*}totalDigits")
        pattern = find(".//{*}pattern")
        if pattern != None:
            pattern = pattern.replace("\\","\\\\")

        strToWrite = """
kg:{0}Shape a sh:PropertyShape;
    rdfs:comment "Property Shape for {0} ({1})" ;
    sh:path ont:{0};
""".format(DPName, attributeCode)

        strToWrite = appendIfNotNone(strToWrite,"    sh:datatype {};", datatype)
        strToWrite = appendIfNotNone(strToWrite,"    sh:minInclusive {};", minInclusive)
        strToWrite = appendIfNotNone(strToWrite,"    sh:maxInclusive {};", maxInclusive)
        strToWrite = appendIfNotNone(strToWrite,"    sh:minLength {};", minLength)
        strToWrite = appendIfNotNone(strToWrite,"    sh:maxLength {};", maxLength)
        strToWrite = appendIfNotNone(strToWrite,"    sh:maxLength {};", totalDigits)
        strToWrite = appendIfNotNone(strToWrite,'    sh:pattern "{}";', pattern)


        outfile.write(strToWrite + "\n .\n")

        attributesDone.add(attributeCode)

    relations = bfToWrite.findall("NrBlocLie")
    if relations[0].text != None:
        for relation in relations:
            bfToVisit.append((path, relation.text))

while bfToVisit:
    path, code = bfToVisit.pop(0)
    writeBFShape(path, code)

