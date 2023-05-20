import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

dictWCT2Abreviation = {
    "Cotisation Fedris" : "CF",
    "Cotisation membre du personnel statutaire exclusivement soumis à la cotisation de pension du secteur public" : "CPSCPSP",
    "Cotisation non liée à une personne physique" : "CNPP",
    "Cotisation ordinaire" : "CO",
    "Cotisation personnelle chômeur avec complément d'entreprise (RCC) ou indemnités complémentaires pour travailleurs âgés (RCIC)" : "CPCCEIDPA",
    "Cotisation spéciale chômeur avec complément d'entreprise (RCC)" : "CSCCE",
    "Cotisation spéciale étudiant" : "CSE",
    "Cotisation spéciale indemnités complémentaires" : "CSIC",
    "Cotisation spéciale travailleur statutaire licencié" : "CSTSL",
    "Cotisation supplémentaire" : "CS",
    "Stagiaires" : "S"
}

root = xmlRoot("AN2022-2-FR2.xml", encoding="iso-8859-1")
for elem in root:
    WorkerCodeType = elem.find("TypeCodeTravailleur").text
    WorkerCode = elem.find("Code").text

    dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = quarterToInteger(elem, "Geldig_vanaf", "Geldig_tot")

    ID = ET.Element("Id")
    ID.text = dictWCT2Abreviation[WorkerCodeType] + WorkerCode + "-" + ValidFromQuarter

    LabelFr = ET.Element("Label")
    LabelFr.text = WorkerCodeType + ": " + WorkerCode

    elem.append(ID)
    elem.append(LabelFr)

outfile = "Adjusted_AN2022-2-FR2.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
