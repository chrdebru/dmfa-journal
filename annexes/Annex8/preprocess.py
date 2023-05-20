import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2022-2-FR8.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text

    dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = quarterToInteger(elem, "Geldig_vanaf", "Geldig_tot")

    elem.find("DMFA").text = "true" if elem.find("DMFA").text == "Yes" else "false"
    elem.find("DMFAPPL").text = "true" if elem.find("DMFAPPL").text == "Yes" else "false"

    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFromQuarter

    LabelFr = ET.Element("Label")
    LabelFr.text = "CODE PRESTATION: " + Code

    elem.append(ID)
    elem.append(LabelFr)

outfile = "Adjusted_AN2022-2-FR8.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
