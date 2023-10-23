import json

from PyQt5.QtNetwork import QNetworkReply

import network




def getConf(window,reply, refreshToken):
    """
    Handle response of the request for the getConf API.
    """
    print(reply.url())
    er = reply.error()
    if er == QNetworkReply.NetworkError.NoError:
        bytes_string = reply.readAll()
        with open("C:\\Users\\admin\\conf\\conf.txt", 'w+') as f:
            f.write(str(bytes_string, 'utf-8'))
        window.texteConf.setTextDisplay('Configuration downloaded')
    elif er == 204:
        try:
            network.getTokens(manager=window._nam, refreshToken=refreshToken )
        except:
            pass
        window.getConf()
    else:
        print("Error occured: ", er)
        print(reply.errorString())


def setConf(window,reply, refreshToken):
    """
    Handle response of the request for the setConf API.
    """
    er = reply.error()
    if er == QNetworkReply.NetworkError.NoError:
        bytes_string = reply.readAll()
        window.uploadText.setTextDisplay(str(bytes_string, 'utf-8'))
    elif er == 201:
        window.uploadText.setTextDisplay("Forbidden")
    elif er == 204:
        try:
            network.getTokens(manager=window._nam, refreshToken=refreshToken )
        except:
            pass
        window.enroll()
    else:
        print("Error occured: ", er)
        print(reply.errorString())


def enrollAuto(window, reply, accessToken, refreshToken):
    """
    Handle response of the request for the enroll API. Trigger the CMP protocol if the response is successful
    """
    er = reply.error()
    certName = ''
    if er == QNetworkReply.NetworkError.NoError:
        bytes_string = reply.readAll()
        tmpPwd=(str(bytes_string, 'utf-8'))
        certName = network.cmpCall(window=window, accessToken=accessToken, pwd = tmpPwd)
    elif er == 204:
        try:
            network.getTokens(manager=window._nam, refreshToken=refreshToken )
        except:
            pass
        window.enrollAuto()
    else:
        print("Error occured: ", er)
        print(reply.errorString())
    return certName

def enrollValid(window, reply, accessToken, refreshToken):
    """
    Handle response of the request for the enroll API. Trigger the CMP protocol if the response is successful
    """
    er = reply.error()
    certName = ''
    if er == QNetworkReply.NetworkError.NoError:
        bytes_string = reply.readAll()
    elif er == 204:
        try:
            network.getTokens(manager=window._nam, refreshToken=refreshToken )
        except:
            pass
        window.enrollValid()
    else:
        print("Error occured: ", er)
        print(reply.errorString())
    return certName

def tokens(window, reply):
    """
    Handle the response from the Keycloak's token endpoint request
    """
    print('response of token is handle')
    er = reply.error()
    if er == QNetworkReply.NetworkError.NoError:
        bytes_string = reply.readAll()
        json_ar = json.loads(str(bytes_string, 'utf-8'))
        accessToken=json_ar['access_token']
        refreshToken=json_ar['refresh_token']
        idToken=json_ar['id_token']
        print("\n Access Token: ", accessToken, '\n')
        print("\n Refresh Token: ", refreshToken, '\n')
        print("\n ID Token: ", idToken, '\n')
        window.setToken(accessToken= accessToken, refreshToken= refreshToken,
        idToken = idToken)
        window.confDisplay.setTextDisplay("You're logged in")
    else:
        print('Error occurred: ', er)
        print(reply.errorString())
    return None