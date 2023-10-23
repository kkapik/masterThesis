from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl

class Window(QMainWindow):
    """
    Display the webpage to authenticate an get the Authorization code.
    """
    def __init__(self, mainwin, codeChallenge,*args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.__codeChallenge = codeChallenge
        self.mainWindow = mainwin
        self.webview = QWebEngineView()
        profile = QWebEngineProfile("storage", self.webview)
        webpage = QWebEnginePage(profile, self.webview)
        self.webview.setPage(webpage)
        self.webview.load(
            QUrl("http://localhost:8080/realms/conf/protocol/openid-connect/auth?response_type=code&client_id=QtConf&scope=openid&redirect_uri=http://localhost:22222/oidc_callback&code_challenge_method=S256&code_challenge="+ self.__codeChallenge))
        self.setCentralWidget(self.webview)
        self.webview.urlChanged.connect(self.onUrlChanged)
        self.cookies_list_info = []

    
    def onUrlChanged(self):
        """
        Close the web engine et save the Authorization code when the callback URL is reach.
        The Authorization Code is transmitted to the main window.
        """
        print("http://localhost:22222/oidc_callback?" in self.webview.url().toString())
        if "http://localhost:22222/oidc_callback?" in self.webview.url().toString():
            print(self.webview.url().toString().split("code=")[1],'State: ',
            self.webview.url().toString().split("&code=")[0].split("session_state=")[1] )
            self.mainWindow.setAuthCode(
                self.webview.url().toString().split("code=")[1].replace("#",""),
                self.webview.url().toString().split("&code=")[0].split("session_state=")[1])
            self.close()
        return None
