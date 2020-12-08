# utf-8
import GlobalVar
import xml.etree.ElementTree as tree


class BasicBeanBuilder:
    def __init__(self):
        bean_xml_file = GlobalVar.cf.get('project', 'beanFile')
        self.xmlTree = tree.parse(bean_xml_file)
