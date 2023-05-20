import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2022-1-FR27.xml", encoding="iso-8859-1")
for elem in root:
    EmployerClass = elem.find("Code").text

    ValidFrom, ValidTo = dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = dateToQuarter(elem, "Geldig_vanaf", "Geldig_tot", ValidFrom, ValidTo)

    ID = ET.Element("Id")
    ID.text = EmployerClass + "-" + ValidFromQuarter

    LabelFr = ET.Element("Label")
    LabelFr.text = "Catégorie Employeur" + ": " + EmployerClass

    elem.append(ID)
    elem.append(LabelFr)

outfile = "Adjusted_AN2022-1-FR27.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
