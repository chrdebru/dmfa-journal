import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2022-3-FR21.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text

    dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = quarterToInteger(elem, "Geldig_vanaf", "Geldig_tot")

    elem.find("DescrSSCode").text = "true" if elem.find("DescrSSCode").text == "Yes" else "false"
    elem.find("DescrSSAPLCode").text = "true" if elem.find("DescrSSAPLCode").text == "Yes" else "false"

    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFromQuarter

    elem.append(ID)

outfile = "Adjusted_AN2022-3-FR21.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
