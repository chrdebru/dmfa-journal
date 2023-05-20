import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2001-3-1FR10.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text

    elem.find("begin_geldigheid").text = "0" + elem.find("begin_geldigheid").text 
    elem.find("einde_geldigheid").text = "0" + elem.find("einde_geldigheid").text 

    ValidFrom, ValidTo = dateToXSDFormat(elem, "begin_geldigheid", "einde_geldigheid")
    ValidFromQuarter, _ = dateToQuarter(elem, "Geldig_vanaf", "Geldig_tot", ValidFrom, ValidTo)
   
    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFromQuarter

    elem.append(ID)

outfile = "Adjusted_AN2001-3-1FR10.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
