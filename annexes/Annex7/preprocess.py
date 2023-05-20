import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2021-4-FR7.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text

    ValidFrom, ValidTo = dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = dateToQuarter(elem, "Geldig_vanaf", "Geldig_tot", ValidFrom, ValidTo)
   
    elem.find("DMFA").text = "true" if elem.find("DMFA").text == "Yes" else "false"
    elem.find("ADRS").text = "true" if elem.find("ADRS").text == "Yes" else "false"

    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFromQuarter

    LabelFr = ET.Element("Label")
    LabelFr.text = "CODE RÉMUNÉRATION: " + Code

    elem.append(ID)
    elem.append(LabelFr)

outfile = "Adjusted_AN2021-4-FR7.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
