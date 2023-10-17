import sys
sys.path.append("../")
from helper import *

outfile = open("mapping.ttl", "w")
DmfA_xml_filename = "./data/DmfAExamples/DmfAOriginal_2Quarters_Linked.xml"

outfile.write("""
@prefix rml: <http://semweb.mmlab.be/ns/rml#> .
@prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix ql: <http://semweb.mmlab.be/ns/ql#> .
@prefix xs: <http://www.w3.org/2001/XMLSchema#> .

@prefix ont: <http://kg.socialsecurity.be/ont/dmfa#> .
@base <http://kg.socialsecurity.be/resource/> .

""")

rootBFxml = xmlRoot("VersCplt_BFdmfa20223FR.xml", encoding="iso-8859-1")
rootDmfaXsd = xmlRoot("DmfAOriginal_20223.xsd", encoding="utf-8")
elementsDmfaXsd = rootDmfaXsd.findall("./{*}element")

bfCodeDict = {}
for bf in rootBFxml:
    bfCodeDict[bf.find("Code").text] = bf

bfToVisit = [([], "90169")]

def writeBFMapping(path, BFcode):
    bfToWrite = bfCodeDict[BFcode]
    className = bfToWrite.find("XmlLabel").text
    path = path.copy()
    path.append(className)
    iterator = "/" + ("/").join(path)
    outfile.write("""
<#{0}-Mapping>
    a rr:TriplesMap ;

    rml:logicalSource [
        rml:source "{2}" ;
        rml:referenceFormulation ql:XPath ;
        rml:iterator "{1}" ;
    ] ;

    rr:subjectMap [
        rr:class ont:{0};
        rr:termType rr:BlankNode ;
        rr:template "{0}{{@id}}"
    ] ;
    """.format(className, iterator, DmfA_xml_filename))

    attributes = bfToWrite.findall("Zones")
    for att in attributes:
        if att.text:
            code = att.text.split(' ', 1)[0]
            element = [element for element in elementsDmfaXsd if element.find(
                ".//{*}documentation").text == code][0]

            DPName = element.attrib["name"]
            datatype = element.find(".//{*}restriction").attrib["base"]

            outfile.write("""
    rr:predicateObjectMap [
        rr:predicate ont:{0};
        rr:objectMap [
            rml:reference "{0}";
            rr:datatype {1} ;
        ] ;
    ] ;
""".format(DPName, datatype))

    relations = bfToWrite.findall("NrBlocLie")
    if relations[0].text != None:
        for relation in relations:
            rangeClassCode = relation.text
            rangeClassName = bfCodeDict[rangeClassCode].find("XmlLabel").text
            outfile.write("""
    rr:predicateObjectMap [
        rr:predicate ont:R_{0}_{1} ;
        rr:objectMap [ 
            rr:parentTriplesMap <#{2}-Mapping> ;
            rr:joinCondition [
                rr:child "./@id";
                rr:parent "./@parent";
            ] ; 
        ] ;
    ] ;
""".format(BFcode, relation.text, rangeClassName))
            
    outfile.write(".\n")
    if relations[0].text != None:
        for relation in relations:
            bfToVisit.append((path, relation.text))

while bfToVisit:
    path, code = bfToVisit.pop(0)
    writeBFMapping(path, code)
