from plistlib import PlistParser
from xml.parsers.expat import ParserCreate


__all__ = ['load', 'loads']


def load(s):
    p = ExtendedPlistParser()
    return p.parse(s)


def loads(s):
    p = ExtendedPlistParser()
    return p.parse_string(s)


class ExtendedPlistParser(PlistParser):
    def parse_string(self, fileobj):
        self.parser = ParserCreate()
        self.parser.StartElementHandler = self.handleBeginElement
        self.parser.EndElementHandler = self.handleEndElement
        self.parser.CharacterDataHandler = self.handleData
        self.parser.Parse(fileobj)
        return self.root
