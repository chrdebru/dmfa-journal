import xml.etree.ElementTree as ET

import sys
sys.path.append("../../")
from helper import *

root = xmlRoot("AN2015-1-FR42.xml", encoding="iso-8859-1")
for elem in root:
    Code = elem.find("Code").text
  
    ValidFromQuarter, _ = quarterToInteger(elem, "Geldig_vanaf", "Geldig_tot")

    ID = ET.Element("Id")
    ID.text = Code + "-" + ValidFromQuarter

    elem.append(ID)

outfile = "Adjusted_AN2015-1-FR42.xml"
tree = ET.ElementTree(root)
tree.write(outfile, encoding="utf-8")
