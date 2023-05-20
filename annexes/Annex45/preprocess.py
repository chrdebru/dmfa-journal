import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2020-1-FR45.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text

    ValidFrom, ValidTo = dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = dateToQuarter(elem, "Geldig_vanaf", "Geldig_tot", ValidFrom, ValidTo)

    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFromQuarter

    elem.append(ID)

outfile = "Adjusted_AN2020-1-FR45.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
