import xml.dom.minidom
import os
# Файл с Мосбиржы со списком облигаций в XML
xml_file="res/bond_list.xml"

cwd = os.path.dirname(__file__)
xml_file = os.path.join(cwd, os.pardir, xml_file)
xml_file = os.path.normpath(xml_file)

doc = xml.dom.minidom.parse(xml_file)
rows = doc.getElementsByTagName("row")
print (len(rows))
for row in rows:
    print (row.getAttribute("secid"), row.getAttribute("name"), row.getAttribute("issuedate"))