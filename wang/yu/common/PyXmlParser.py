import xmltodict


class PyXmlParser:
    def __init__(self, xml_directory=None):
        self.xml_directory = xml_directory

    def translate_file_to_text(self):
        # translate xml file to string
        with open(self.xml_directory, encoding='utf-8') as xml_file:
            temp = xml_file.read()
            return temp

    def do_parse(self):
        # parse properties.xml to json object.
        if self.xml_directory is None:
            return None
        return xmltodict.parse(self.translate_file_to_text())

