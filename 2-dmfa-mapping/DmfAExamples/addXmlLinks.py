import xml.etree.ElementTree as ET

tagCount = {}

def addLink(node):
    parentId = node.attrib["id"]
    for child in node:
        child.set("parent", parentId)
        
        if child.tag not in tagCount.keys():
            tagCount[child.tag] = 0
        else :
            tagCount[child.tag] += 1
        
        child.set("id", str(tagCount[child.tag]) )
        addLink(child)


inputfile = input("inputfile: ")
tree = ET.parse(inputfile)
root = tree.getroot()

root.set("id", "0")
addLink(root)

outfile = "Linked_" + inputfile
tree.write(outfile)