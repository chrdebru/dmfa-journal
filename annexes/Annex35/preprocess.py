import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2013-1-FR35.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text

    dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = quarterToInteger(elem, "Geldig_vanaf", "Geldig_tot")

    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFromQuarter

    LabelFr = ET.Element("Label")
    LabelFr.text = "Mesure de promotion de l'emploi: " + Code

    elem.append(ID)
    elem.append(LabelFr)


outfile = "Adjusted_AN2013-1-FR35.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
