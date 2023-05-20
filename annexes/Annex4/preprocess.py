import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2022-2-FR4.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("CodeDMFA").text

    ValidFromQuarter, _ = quarterToInteger(elem, "Vanaf", "Tot")

    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFromQuarter

    LabelFr = ET.Element("Label")
    LabelFr.text = "Déduction code " + Code

    ReductionJurisdiction = elem.find("Ded_FedRegFR").text
    if ReductionJurisdiction == "Fédérale":
        elem.remove(elem.find("Ded_FlemishRegFR"))
        elem.remove(elem.find("Ded_BxlRegFR"))
        elem.remove(elem.find("Ded_WallNoGermanRegFR"))
        elem.remove(elem.find("Ded_WallGermanRegFR"))
    else :
        elem.find("Ded_FlemishRegFR").text = "true" if elem.find("Ded_FlemishRegFR").text == "Oui" else "false"
        elem.find("Ded_BxlRegFR").text = "true" if elem.find("Ded_BxlRegFR").text == "Oui" else "false"
        elem.find("Ded_WallNoGermanRegFR").text = "true" if elem.find("Ded_WallNoGermanRegFR").text == "Oui" else "false"
        elem.find("Ded_WallGermanRegFR").text = "true" if elem.find("Ded_WallGermanRegFR").text == "Oui" else "false"

    elem.find("PresBlcDetFr").text = "true" if elem.find("PresBlcDetFr").text == "Oui" else "false"
    elem.find("LinkBlocFr").text = "http://kg.socialsecurity.be/ont/dmfa#WorkerRecord" if elem.find("LinkBlocFr").text == "Ligne travailleur" else "http://kg.socialsecurity.be/ont/dmfa#Occupation" #There should only be 2 Functional Bloc


    elem.append(ID)
    elem.append(LabelFr)

outfile = "Adjusted_AN2022-2-FR4.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
