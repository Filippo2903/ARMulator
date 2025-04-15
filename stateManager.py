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
