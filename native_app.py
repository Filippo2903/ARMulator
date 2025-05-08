import os
from PyQt5.QtCore import QUrl, QFileSystemWatcher, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtNetwork import QNetworkCookie
from stateManager import StateManager

appState = StateManager()

class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print("\n====== JavaScript Console Log ======")
        print(f"{message}\n")
        print(f"Line: {lineNumber} - Source: {sourceID}")
        print("====================================\n")

class NativeApp(QApplication):
    def __init__(self):
        super().__init__([])
        print("calling start_webview")

        self.window = QMainWindow()
        self.browser = QWebEngineView()

        self.profile = QWebEngineProfile("storage", self.window)
        self.profile.clearHttpCache()

        page = CustomWebEnginePage(self.profile, self.browser)
        self.browser.setPage(page)

        self.cookies = []
        cookie_store = self.profile.cookieStore()
        cookie_store.cookieAdded.connect(self.onCookieAdded)

        self.browser.setUrl(QUrl(f"http://localhost:{appState.getHttpPort()}"))
        self.browser.page().loadFinished.connect(self.injectConsoleFormatter)

        self.window.setCentralWidget(self.browser)
        self.window.setWindowTitle("ARM-Compiler")
        self.window.resize(800, 600)
        self.window.show()

        self.watcher = QFileSystemWatcher(self)
        self.addInitialWatchedFiles("interface")
        self.watcher.fileChanged.connect(self.onFileChanged)

        self.aboutToQuit.connect(self.cleanup)

        self.exec_()

    def injectConsoleFormatter(self):
        self.browser.page().runJavaScript("""
            (function () {
                const logTypes = ['log', 'warn', 'error'];
                logTypes.forEach(type => {
                    const original = console[type];
                    console[type] = function (...args) {
                        original(...args);
                        try {
                            const formatted = args.map(arg => {
                                if (typeof arg === 'object') {
                                    return JSON.stringify(arg, null, 2);
                                }
                                return String(arg);
                            }).join(' ');
                            original(formatted);
                        } catch (e) {
                            original("Error serializing console." + type + " arguments", e);
                        }
                    };
                });
            })();
        """)

    def addInitialWatchedFiles(self, path):
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                if os.path.isfile(full_path):
                    self.watcher.addPath(full_path)

    def onFileChanged(self, path):
        print(f"File modificato: {path}")
        QTimer.singleShot(300, self.browser.reload)

    def onCookieAdded(self, cookie):
        for c in self.cookies:
            if c.hasSameIdentifier(cookie):
                return
        self.cookies.append(QNetworkCookie(cookie))

    def cleanup(self):
        print("Cleaning up WebEngine resources...")
        if self.browser:
            self.browser.setPage(None)
            self.browser.deleteLater()
        if self.window:
            self.window.close()