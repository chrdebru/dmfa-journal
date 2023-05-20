import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2021-1-FR46.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text

    ValidFrom, ValidTo = dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = dateToQuarter(elem, "Geldig_vanaf", "Geldig_tot", ValidFrom, ValidTo)
   
    elem.find("PublicSectorFR").text = "true" if elem.find("PublicSectorFR").text == "Oui" else "false"
    elem.find("PrivateSectorFR").text = "true" if elem.find("PrivateSectorFR").text == "Oui" else "false"

    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFromQuarter

    elem.append(ID)

outfile = "Adjusted_AN2021-1-FR46.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
