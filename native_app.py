import webview
from stateManager import StateManager

appState = StateManager()

def start_app():
    url = f"http://localhost:{appState.getHttpPort()}"
    webview.create_window("ARM-Compiler", url, maximized=True)
    webview.start()
