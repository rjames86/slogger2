from xml.etree.ElementTree import Element, SubElement, Comment, tostring, XML

class XMLBuilder(object):
    @staticmethod
    def dict(key, elem):
        d = Element('dict')
        k = SubElement(d, 'key')
        k.text = key
        d.append(elem)
        return d

    @staticmethod
    def by_key(key, text):
        e = Element(key)
        e.text = text
        return e

    @staticmethod
    def add_subelement(elem, sub_elem):
        elem.append(sub_elem)
        return elem

    @staticmethod
    def array(key, items):
        array = Element('array')
        array_items = [XMLBuilder.by_key('string', item) for item in items]
        array.extend(array_items)
        return array

