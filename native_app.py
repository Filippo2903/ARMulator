from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

class NativeApp(QApplication):
    def __init__(self):
        super().__init__([])
        print("calling start_webview")

        # Crea la finestra principale
        window = QMainWindow()
        browser = QWebEngineView()

        # Carica il sito web
        browser.setUrl(QUrl("http://localhost:8000"))  # Adatta l'URL se necessario
        window.setCentralWidget(browser)

        window.setWindowTitle("App Web Nativa")
        window.resize(800, 600)

        # Mostra la finestra
        window.show()
        self.exec_()
