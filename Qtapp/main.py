import sys, re, base64, os, hashlib, subprocess, shlex
from PyQt5 import QtNetwork
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QGroupBox, QVBoxLayout

import network, widgets, webengine, responsehandler


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__()
        #Class Variables
        self.__accessToken = ""
        self.__refreshToken = "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI1MTM5OGY1Ny1kZDQ4LTQwMTgtOGYyZS0wOWJmZTQ5M2M1MTIifQ.eyJleHAiOjE2NzM0Mzc1MTgsImlhdCI6MTY3MzQzNTcxOCwianRpIjoiODEzZWFmZDQtM2I5My00ODQ1LTk5MWMtOTI4MjM4ODIxMDZmIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9jb25mIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9jb25mIiwic3ViIjoiNTM1NjA0MzQtZmI2NC00ZDc4LWIyNWItY2FlNmYxY2JmODIyIiwidHlwIjoiUmVmcmVzaCIsImF6cCI6IlF0Q29uZiIsInNlc3Npb25fc3RhdGUiOiJhOWQyOTExOS03NWZjLTQyMWEtYTU0ZC04MTkzMWZiMTM1OWMiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiYTlkMjkxMTktNzVmYy00MjFhLWE1NGQtODE5MzFmYjEzNTljIn0.G1zVZjTXpNX93vVmMLjGJ8spLxHwA4DzSp3sJ0ScmL0"
        self.__idToken = ""
        self.__authCode ="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI1ZmJiM0QxeW1CNnJmZmxrVlc0Tkw3bGZRZEVqNGpIdzg5VUhKVVVzSWhnIn0.eyJleHAiOjE2NzM2MDEyNDQsImlhdCI6MTY3MzYwMTE4NCwiYXV0aF90aW1lIjoxNjczNjAxMTgwLCJqdGkiOiJhZDVmMzhlMi01YjBmLTRiNTgtODYyZi0xOWUxNWMxMjkwYTciLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvcmVhbG1zL2NvbmYiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiNTM1NjA0MzQtZmI2NC00ZDc4LWIyNWItY2FlNmYxY2JmODIyIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiUXRDb25mIiwic2Vzc2lvbl9zdGF0ZSI6IjI2ZjgyZDE1LTU4ZDktNDYyZS04MDY5LWNjN2NmZGI1YzI1ZiIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1jb25mIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiIyNmY4MmQxNS01OGQ5LTQ2MmUtODA2OS1jYzdjZmRiNWMyNWYiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlRvdG8gVEFUQSIsInByZWZlcnJlZF91c2VybmFtZSI6InRvdG8iLCJnaXZlbl9uYW1lIjoiVG90byIsImZhbWlseV9uYW1lIjoiVEFUQSIsImVtYWlsIjoidG90b0B0b3RvLmZyIn0.oMaCpHLLq8HqW2n1WLIhKGP5WXmCcATYhytodIZ9J9P4_7HYdkYhiEUiCTe9BhjVa_nnGtofXEpVTfMgL5OebfE57cb-cHBWXNsGd1SPV9ftwK313Z2_Rj9YCSEGbBamisitet3gmlgIluS9vdmB0qf4Mdd7GaffM--jkb_3NlxP2j5HTmjqPkmnxMm-QSjRxNHYyjNt3AINrA4xJ4WIXQkV_7NrRGzTSrnpZE4TFIuGZTKIf86g8MnoW_rHC7WsEqMYoL6jgLBm5EMKbCqEsU9_cPYeNADtPT2jXK6LuyzfvSH_aAvYLW3tZRzUB8S96kL9EpoIY4Xm6Xzl_y4c-w"
        self.openssl = '"C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe"'
        self.certWorkDir = '"C:\\Users\\admin\\certs\\' # CHANGE THIS
        self.servUrl = 'http://localhost:5000'
        self.certName = 'j68QyGzh2r'


        # generate code verifier and code challenge
        self.__codeVerifier = base64.urlsafe_b64encode(
            os.urandom(40)).decode("utf-8")
        self.__codeVerifier = re.sub("[^a-zA-Z0-9]+", "", self.__codeVerifier)
        print(type(self.__codeVerifier), self.__codeVerifier,
        len(self.__codeVerifier))
        self.__codeChallenge = hashlib.sha256(
            self.__codeVerifier.encode("utf-8")).digest()
        self.__codeChallenge = base64.urlsafe_b64encode(
            self.__codeChallenge).decode("utf-8")
        self.__codeChallenge = self.__codeChallenge.replace("=", "")
        print(type(self.__codeChallenge), self.__codeChallenge)


        #Creation of all network manager
        self._netManagerGet = QtNetwork.QNetworkAccessManager()
        self._netManagerGet.finished.connect(self.handleResponse)

        self._netManagerSet = QtNetwork.QNetworkAccessManager()
        self._netManagerSet.finished.connect(self.handleResponse)

        self._netManagerEnroll = QtNetwork.QNetworkAccessManager()
        self._netManagerEnroll.finished.connect(self.handleResponse)

        self._netManagerTokens = QtNetwork.QNetworkAccessManager()
        self._netManagerTokens.finished.connect(self.handleResponse)


        #Construction of layout
        layout = QGridLayout()

        # Authentication Part
        self.groupBoxAuthLayout= QVBoxLayout()
        self.groupBoxAuth = QGroupBox('Authentication')
        self.groupBoxAuth.setLayout(self.groupBoxAuthLayout)
        layout.addWidget(self.groupBoxAuth,0,0,1,1)

        self.groupBoxAuthLayout.addWidget(widgets.CustomButton("Login",
        self.launchAuthWeb))
        self.groupBoxAuthLayout.addWidget(widgets.CustomButton("Logout",
        self.logout))

        self.confDisplay = widgets.TextDisplay("Not logged in")
        self.groupBoxAuthLayout.addWidget(self.confDisplay)



        # Configuration Part
        self.groupBoxConfLayout= QVBoxLayout()
        self.groupBoxConf = QGroupBox('Configuration')
        self.groupBoxConf.setLayout(self.groupBoxConfLayout)
        layout.addWidget(self.groupBoxConf,0,1,1,1)

        self.texteConf = widgets.TextDisplay("")
        self.groupBoxConfLayout.addWidget(self.texteConf)

        self.groupBoxConfLayout.addWidget(widgets.CustomButton("Get Conf",
        self.getConf))
        self.groupBoxConfLayout.addWidget(widgets.CustomButton("View Conf",
        self.viewConf))

        self.pathInput=QLineEdit()
        self.pathInput.setFixedWidth(200)
        self.groupBoxConfLayout.addWidget(self.pathInput)

        self.groupBoxConfLayout.addWidget(widgets.CustomButton("Upload Config",
        self.setConf))

        self.uploadText = widgets.TextDisplay("Result of upload")
        self.groupBoxConfLayout.addWidget(self.uploadText)



        # Key Part
        self.groupBoxKeyLayout= QVBoxLayout()
        self.groupBoxKey = QGroupBox('Key')
        self.groupBoxKey.setLayout(self.groupBoxKeyLayout)
        layout.addWidget(self.groupBoxKey,1,0,1,1)

        self.groupBoxKeyLayout.addWidget(widgets.CustomButton("Enroll Auto",
        self.enrollAuto))

        self.groupBoxKeyLayout.addWidget(widgets.CustomButton("Enroll With Validation",
        self.enrollValid))

        self.enrollCodeInput=QLineEdit()
        self.enrollCodeInput.setFixedWidth(200)
        self.groupBoxKeyLayout.addWidget(self.enrollCodeInput)

        self.groupBoxKeyLayout.addWidget(widgets.CustomButton("Get Certificate with Code",
        self.getCertificate))

        self.groupBoxKeyLayout.addWidget(widgets.CustomButton("View Certificate",
        self.viewCert))


        # Key Research Part
        self.groupBoxRandLayout= QVBoxLayout()
        self.groupBoxRand = QGroupBox('Research a key')
        self.groupBoxRand.setLayout(self.groupBoxRandLayout)
        layout.addWidget(self.groupBoxRand,1,1,1,1)

        self.groupBoxRandLayout.addWidget(widgets.CustomButton("OCSP check",
        self.ocspCheck))


        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,1)

        #Building the main window
        widget = QWidget()
        widget.setLayout(layout)
        self.setWindowTitle("KTH - Poncet Console")
        self.setGeometry(100,100,1000,800)
        self.setCentralWidget(widget)




    def launchAuthWeb(self):
        """
        Launch the webpage to get the Authorization code
        """
        self.w = webengine.Window(self, self.__codeChallenge)
        self.w.show()
        self.hide
        return None

    def setAuthCode(self, authCode, state):
        """
        Save the Authorization Code for the call of Keycloak's token endpoint.
        """
        self.__authCode = authCode
        print("Authorization Code:", self.__authCode)
        network.getTokens(self._netManagerTokens, authCode= self.__authCode,
        code_verifier= self.__codeVerifier, state=state)
        return None

    def logout(self):
        """
        Delete all token stored in the application
        """
        self.__authCode=""
        self.__accessToken = ""
        self.__idToken= ""
        self.__refreshToken = ""
        self.confDisplay.setTextDsiplay("Logged out")
        return None

    def setToken(self, accessToken, refreshToken, idToken):
        """
        Set all token stored in application
        """
        self.__accessToken = accessToken
        self.__refreshToken = refreshToken
        self.__idToken = idToken
        return None




    def getConf(self):
        """
        Call the getConf API with Access token  in headers
        """
        res = network.isTokenValid(self.__accessToken, self.__refreshToken)
        if res[0]:
            network.sendRequest(url=self.servUrl + '/getConf',
            manager=self._netManagerGet, method='GET',
            accessToken=self.__accessToken)
        elif res[1]:
            network.getTokens(manager=self._netManagerTokens,
            refreshToken=self.__refreshToken )
            network.sendRequest(url=self.servUrl + '/getConf',
            manager=self._netManagerGet,method='GET',
            accessToken=self.__accessToken)
        else:
             self.confDisplay.setTextDsiplay("You need to log in")
        return None

    def setConf(self):
        """
        Read the content of the file selected and call the API to set the configuration
        """
        try:
            f = open(self.pathInput.text(), 'r')
            res = network.isTokenValid(self.__accessToken, self.__refreshToken)
            if res[0]:
                network.sendRequest(url=self.servUrl + '/setConf',
                manager=self._netManagerSet,method='POST',
                accessToken=self.__accessToken, conf=f.read())
            elif res[1]:
                network.getTokens(manager=self._netManagerTokens,
                refreshToken=self.__refreshToken )
                network.sendRequest(url=self.servUrl + '/setConf',
                manager=self._netManagerSet,method='POST',
                accessToken=self.__accessToken, conf=f.read())
            else:
                self.confDisplay.setTextDsiplay("You need to log in")
            return None
        except:
            self.uploadText.setTextDsiplay("File doesn't exist")


    def enrollAuto(self):
        """
        Call the enrollement API endpoint with an acces token in headers
        """
        res = network.isTokenValid(self.__accessToken, self.__refreshToken)
        if res[0]:
            network.sendRequest(url=self.servUrl + '/enrollAuto',
            manager=self._netManagerEnroll,method='GET',
            accessToken=self.__accessToken)
        elif res[1]:
            network.getTokens(manager=self._netManagerTokens,
            refreshToken=self.__refreshToken )
            network.sendRequest(url=self.servUrl + '/enrollAuto',
            manager=self._netManagerEnroll,method='GET',
            accessToken=self.__accessToken)
        else:
             self.confDisplay.setTextDsiplay("You need to log in")
        return None

    def enrollValid(self):
        """
        Call the enrollement API endpoint with an acces token in headers
        """
        res = network.isTokenValid(self.__accessToken, self.__refreshToken)
        if res[0]:
            network.sendRequest(url=self.servUrl + '/enrollValid',
            manager=self._netManagerEnroll,method='GET',
            accessToken=self.__accessToken)
        elif res[1]:
            network.getTokens(manager=self._netManagerTokens,
            refreshToken=self.__refreshToken )
            network.sendRequest(url=self.servUrl + '/enrollValid',
            manager=self._netManagerEnroll,method='GET',
            accessToken=self.__accessToken)
        else:
             self.confDisplay.setTextDsiplay("You need to log in")
        return None

    def handleResponse(self, reply):
        url= QUrl.toString(reply.url())
        if 'getConf' in url:
            responsehandler.getConf(window=self, reply=reply,
            refreshToken= self.__refreshToken)
        elif 'setConf' in url:
            responsehandler.setConf(window=self, reply=reply,
            refreshToken= self.__refreshToken)
        elif 'enrollAuto' in url:
            self.certName = responsehandler.enrollAuto(window= self, reply= reply,
            accessToken=self.__accessToken, refreshToken= self.__refreshToken)
            print(self.certName)
        elif 'enrollValid' in url:
            self.certName = responsehandler.enrollValid(window= self, reply= reply,
            accessToken=self.__accessToken, refreshToken= self.__refreshToken)
            print(self.certName)
        elif 'realms' in url:
            responsehandler.tokens(window=self, reply=reply)
        return None

    def viewCert(self):
        cmd = '%SystemRoot%\\system32\\rundll32.exe cryptext.dll,CryptExtOpenCER '+ self.certWorkDir[1:] + self.certName +'.crt'
        os.system(cmd)
        return None

    def viewConf(self):
        os.system("notepad.exe C:\\Users\\admin\\conf\\conf.txt")
        return None

    def ocspCheck(self):
        cmd = self.openssl + ' ocsp -issuer ".\\certs\\ManagementCA-chain.pem" -cert ' + self.certWorkDir + self.certName + '.crt" -text -url http://ce01.solitude.skyrim:80/ejbca/publicweb/status/ocsp'
        a = subprocess.run(shlex.split(cmd), capture_output=True)
        if 'revoked' in str(a.stdout, 'UTF-8'):
            print("-----------------ALARM WARNING-----------------")
            print("----------This certificate is REVOKED----------")
        else:
            print("All Good")
        return None

    def getCertificate(self):
        if self.enrollCodeInput.text() == "" :
            print("You need to enter a code")
        else:
            network.cmpCall(window=self, accessToken= self.__accessToken, pwd= self.enrollCodeInput.text())
        return None







if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
