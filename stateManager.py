import os
import inspect
from translation.dictionary import create_main_dict

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class StateManager():
    def __init__(self, httpPort="8000", webPort="31415", lang = "en"):
        self.httpPort = httpPort
        self.webPort = webPort
        self.lang = lang
        self.mainDict = create_main_dict()
        pass

    def getHttpPort(self):
        return self.httpPort

    def setHttpPort(self, httpPort):
        self.httpPort = httpPort

    def getWebPort(self):
        return self.webPort

    def setWebPort(self, webPort):
        self.webPort = webPort

    def getLang(self):
        return self.lang

    def setLang(self, lang):
        self.lang = lang

    # Shorthand for "getTranslation"
    # Usable even with key-values in dictionaries by changing from list to dictionary
    # as values for each file
    def getT(self, index):
        caller_filename = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]

        try:
            return self.mainDict[self.lang][caller_filename][index]
        except (KeyError, IndexError):
            return f"[{self.lang}:{caller_filename}:{index}] NOT FOUND"