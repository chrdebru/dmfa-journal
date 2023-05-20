import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2022-1-FR28.xml", encoding="iso-8859-1")
for elem in root:
    WorkerCode = elem.find("Code").text

    ValidFrom, ValidTo = dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = dateToQuarter(elem, "Geldig_vanaf", "Geldig_tot", ValidFrom, ValidTo)

    ONSSCodeElem = elem.find("CodeRSZ")
    if ONSSCodeElem.text == "/":
        elem.remove(ONSSCodeElem)


    ID = ET.Element("Id")
    ID.text = WorkerCode + "-" + ValidFrom

    LabelFr = ET.Element("Label")
    LabelFr.text = "Code travailleurs APL" + ": " + WorkerCode

    elem.append(ID)
    elem.append(LabelFr)

outfile = "Adjusted_AN2022-1-FR28.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
