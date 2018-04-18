from codecs import lookup

__all__ = ['from_sublime', 'to_sublime']


def from_sublime(name):
    return SUBLIME_TO_STANDARD.get(name, None)


def to_sublime(name):
    return STANDARD_TO_SUBLIME.get(lookup(name).name, None)


SUBLIME_TO_STANDARD = {  # noqa: E121
   "UTF-8": "utf-8",
   "UTF-8 with BOM": "utf-8-sig",
   "UTF-16 LE": "utf-16-le",
   "UTF-16 LE with BOM": "utf-16",
   "UTF-16 BE": "utf-16-be",
   "UTF-16 BE with BOM": "utf-16",
   "Western (Windows 1252)": "cp1252",
   "Western (ISO 8859-1)": "iso8859-1",
   "Western (ISO 8859-3)": "iso8859-3",
   "Western (ISO 8859-15)": "iso8859-15",
   "Western (Mac Roman)": "mac-roman",
   "DOS (CP 437)": "cp437",
   "Arabic (Windows 1256)": "cp1256",
   "Arabic (ISO 8859-6)": "iso8859-6",
   "Baltic (Windows 1257)": "cp1257",
   "Baltic (ISO 8859-4)": "iso8859-4",
   "Celtic (ISO 8859-14)": "iso8859-14",
   "Central European (Windows 1250)": "cp1250",
   "Central European (ISO 8859-2)": "iso8859-2",
   "Cyrillic (Windows 1251)": "cp1251",
   "Cyrillic (Windows 866)": "cp866",
   "Cyrillic (ISO 8859-5)": "iso8859-5",
   "Cyrillic (KOI8-R)": "koi8-r",
   "Cyrillic (KOI8-U)": "koi8-u",
   "Estonian (ISO 8859-13)": "iso8859-13",
   "Greek (Windows 1253)": "cp1253",
   "Greek (ISO 8859-7)": "iso8859-7",
   "Hebrew (Windows 1255)": "cp1255",
   "Hebrew (ISO 8859-8)": "iso8859-8",
   "Nordic (ISO 8859-10)": "iso8859-10",
   "Romanian (ISO 8859-16)": "iso8859-16",
   "Turkish (Windows 1254)": "cp1254",
   "Turkish (ISO 8859-9)": "iso8859-9",
   "Vietnamese (Windows 1258)": "cp1258",
}


STANDARD_TO_SUBLIME = {  # noqa: E121
   "cp1258": "Vietnamese (Windows 1258)",
   "cp1250": "Central European (Windows 1250)",
   "cp1251": "Cyrillic (Windows 1251)",
   "cp1252": "Western (Windows 1252)",
   "cp1253": "Greek (Windows 1253)",
   "cp1254": "Turkish (Windows 1254)",
   "cp1255": "Hebrew (Windows 1255)",
   "cp1256": "Arabic (Windows 1256)",
   "cp1257": "Baltic (Windows 1257)",
   "cp437": "DOS (CP 437)",
   "cp866": "Cyrillic (Windows 866)",
   "iso8859-1": "Western (ISO 8859-1)",
   "iso8859-2": "Central European (ISO 8859-2)",
   "iso8859-3": "Western (ISO 8859-3)",
   "iso8859-4": "Baltic (ISO 8859-4)",
   "iso8859-5": "Cyrillic (ISO 8859-5)",
   "iso8859-6": "Arabic (ISO 8859-6)",
   "iso8859-7": "Greek (ISO 8859-7)",
   "iso8859-8": "Hebrew (ISO 8859-8)",
   "iso8859-9": "Turkish (ISO 8859-9)",
   "iso8859-10": "Nordic (ISO 8859-10)",
   "iso8859-13": "Estonian (ISO 8859-13)",
   "iso8859-14": "Celtic (ISO 8859-14)",
   "iso8859-15": "Western (ISO 8859-15)",
   "iso8859-16": "Romanian (ISO 8859-16)",
   "koi8-r": "Cyrillic (KOI8-R)",
   "koi8-u": "Cyrillic (KOI8-U)",
   "mac-roman": "Western (Mac Roman)",
   "utf-16": "UTF-16 LE with BOM",
   "utf-16-be": "UTF-16 BE",
   "utf-16-le": "UTF-16 LE",
   "utf-8": "UTF-8",
   "utf-8-sig": "UTF-8 with BOM",
}
