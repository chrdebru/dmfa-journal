import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2015-2-FR31.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text

    ValidFrom, ValidTo = dateToXSDFormat(elem, "Date_debut_validite", "Date_fin_validite")
    ValidFromQuarter, _ = dateToQuarter(elem, "Geldig_vanaf", "Geldig_tot", ValidFrom, ValidTo)
   
    elem.find("Code_DmfAppl").text = "true" if elem.find("Code_DmfAppl").text == "YES" else "false"
    elem.find("Maribel_Social_ONSSAPL").text = "true" if elem.find("Maribel_Social_ONSSAPL").text == "YES" else "false"


    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFrom

    LabelFr = ET.Element("Label")
    LabelFr.text = "Code NACE " + ": " + Code

    elem.append(ID)
    elem.append(LabelFr)

outfile = "Adjusted_AN2015-2-FR31.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
