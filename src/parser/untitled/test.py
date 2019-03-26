



import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
root = tree.getroot()
if root.tag=='create':
    for child in root:
        if child.tag=='account':
            id1=child.attrib.get('id')
            balance=child.attrib.get('balance')
            print(id1,balance)
        elif child.tag=='symbol':
            symbol=child.attrib.get('sym')
            print(symbol)
            for grandchild in child:
                id2=grandchild.attrib.get('id')
                num=grandchild.text
                print(id2,num)

if root.tag=='transactions':
    id1=root.attrib.get('id')
    print(id1)
    for child in root:
        if child.tag=='order':
            symbol=child.attrib.get('sym')
            amount=child.attrib.get('amount')
            limit = child.attrib.get('limit')
            print(symbol,amount,limit)
        elif child.tag=='query':
            id2 = child.attrib.get('id')
            print(id2)
        elif child.tag=='cancel':
            id2 = child.attrib.get('id')
            print(id2)