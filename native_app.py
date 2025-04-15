from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtNetwork import QNetworkCookie
from stateManager import StateManager

appState = StateManager()

class NativeApp(QApplication):
    def __init__(self):
        super().__init__([])
        print("calling start_webview")
        # Crea la finestra principale
        window = QMainWindow()
        browser = QWebEngineView()

        # Carica il sito web
        browser.setUrl(QUrl(f"http://localhost:{appState.getHttpPort()}"))  # Adatta l'URL se necessario
        window.setCentralWidget(browser)

        window.setWindowTitle("App Web Nativa")
        window.resize(800, 600)

        profile = QWebEngineProfile("storage", window)
        cookie_store = profile.cookieStore()
        cookie_store.cookieAdded.connect(self.onCookieAdded)
        self.cookies = []

        window.show()
        self.exec_()

    def onCookieAdded(self, cookie):
        for c in self.cookies:
            if c.hasSameIdentifier(cookie):
                return
        self.cookies.append(QNetworkCookie(cookie))