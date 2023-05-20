import xml.etree.ElementTree as ET

def xmlRoot(filename, encoding):
    xmlfile = open(filename, encoding=encoding)
    xmlstr = xmlfile.read().encode("utf-8", "replace").decode("utf-8")
    xmlfile.close()
    return ET.ElementTree(ET.fromstring(xmlstr)).getroot()

def addTripleQuotes(s):
    if s:
        return '"""' + s + '"""'
    else:
        return None


def appendIfNotNone(strToAppend, strFormat, value):
    if value:
        return strToAppend + "\n" + strFormat.format(value)
    else:
        return strToAppend



def dateToXSDFormat(elem, validFromXML, validToXML):
    ValidFromElem = elem.find(validFromXML)
    ValidToElem = elem.find(validToXML)
    ValidFrom = "-".join(ValidFromElem.text.split('/')[::-1])
    if ValidFrom == "1900-01-01":
        ValidFrom = "2003-01-01"
    ValidTo = "-".join(ValidToElem.text.split('/')[::-1])
    if ValidFrom == "9999-01-01":
        ValidFrom = "9999-12-31"
    ValidFromElem.text = ValidFrom
    ValidToElem.text = ValidTo

    return ValidFrom, ValidTo

def quarterToInteger(elem, validFromQuarterXML, validToQuarterXML):
    ValidFromQuarterElem = elem.find(validFromQuarterXML)
    ValidToQuarterElem = elem.find(validToQuarterXML)
    ValidFromQuarterElem.text = ValidFromQuarterElem.text.replace("/",'')
    ValidToQuarterElem.text = ValidToQuarterElem.text.replace("/",'')

    return ValidFromQuarterElem.text, ValidToQuarterElem.text

def dateToQuarter(elem, validFromQuarterXML, validToQuarterXML, ValidFrom, ValidTo):
    fromYear = int(ValidFrom[:4]) 
    toYear = int(ValidTo[:4]) 

    if fromYear < 2003:
        ValidFromQuarter = "20031"
    else :
        fromQuarter = int(ValidFrom[5:7]) 
        match fromQuarter:
            case 1:
                ValidFromQuarter = str(fromYear * 10 + 1)
            case 4: 
                ValidFromQuarter = str(fromYear * 10 + 2)
            case 7: 
                ValidFromQuarter = str(fromYear * 10 + 3)
            case 10: 
                ValidFromQuarter = str(fromYear * 10 + 4)
            case _:
                print("Month does not match beggining of quarter")
                exit()
    if toYear == 9999:
        ValidToQuarter = "99994"
    else :
        toQuarter = int(ValidTo[5:7]) 
        match toQuarter:
            case 3:
                ValidToQuarter = str(toYear * 10 + 1)
            case 6: 
                ValidToQuarter = str(toYear * 10 + 2)
            case 9: 
                ValidToQuarter = str(toYear * 10 + 3)
            case 12: 
                ValidToQuarter = str(toYear * 10 + 4)
            case _:
                print("Month does not match ending of quarter")
                exit()    

    ValidFromQuarterElem = ET.Element(validFromQuarterXML)
    ValidToQuarterElem = ET.Element(validToQuarterXML)
    ValidFromQuarterElem.text = ValidFromQuarter
    ValidToQuarterElem.text = ValidToQuarter

    elem.append(ValidFromQuarterElem)
    elem.append(ValidToQuarterElem)

    return ValidFromQuarter, ValidToQuarter


    