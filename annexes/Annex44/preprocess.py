import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2021-1-FR44.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text

    ValidFromQuarter, _ = quarterToInteger(elem, "Geldig_vanaf", "Geldig_tot")

    elem.find("DMFA").text = "true" if elem.find("DMFA").text == "Yes" else "false"
    elem.find("DMFAAPL").text = "true" if elem.find("DMFAAPL").text == "Yes" else "false"
    elem.find("Capelo_DHG").text = "true" if elem.find("Capelo_DHG").text == "Yes" else "false"


    ID = ET.Element("Id")
    ID.text = Code + "-" +  ValidFromQuarter

    LabelFr = ET.Element("Label")
    LabelFr.text = "MESURE DE RÉORGANISATION DU TRAVAIL " + ": " + Code

    elem.append(ID)
    elem.append(LabelFr)

outfile = "Adjusted_AN2021-1-FR44.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
