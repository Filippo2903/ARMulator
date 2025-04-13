from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

def main():
    print("calling start_webview")

    # Crea l'applicazione PyQt
    app = QApplication([])

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

    # Avvia il loop dell'applicazione PyQt
    app.exec_()

if __name__ == "__main__":
    main()