# utf-8
import GlobalVar
import xml.etree.ElementTree as tree


class BasicBeanBuilder:
    def __init__(self):
        bean_xml_file = GlobalVar.cf.get('project', 'beanFile')
        self.xmlTree = tree.parse(bean_xml_file)
        self.root = self.xmlTree.getroot()

    def getAllBean(self):
        return self.root.findall('bean')

    def getAllPages(self, beanElement):
        return beanElement.findall('page')

    def getAllLocations(self, pageElement):
        return pageElement.findall('location')

    def getAllActions(self, locationElement):
        return locationElement.findall('action')

    def getValueByAttr(self, element, attrName):
        return element.get(attrName)

    def getAllAttrs(self, element):
        return element.attrib
