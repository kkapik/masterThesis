import jwt, time, string, subprocess, shlex, random
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkRequest, QHttpMultiPart, QHttpPart

def sendRequest(url, manager, method, accessToken, conf=None):
    """
    Method to send request to specified URL
    """
    if method == 'GET':
        url = QUrl(url)
        request = QNetworkRequest(url)
        request.setRawHeader(b'Authorization', b"Bearer " + 
        bytes(accessToken, 'UTF-8'))
        reply = manager.get(request)
    elif method == 'POST':
        data = {"conf": conf}
        multi_part = construct_multipart(data)
        if multi_part:
            url = QUrl(url)
            request = QNetworkRequest(url)
            request.setRawHeader(b'Authorization', b'Bearer '+
            bytes(accessToken, 'UTF-8'))
            reply = manager.post(request, multi_part)
            multi_part.setParent(reply)
    return None

def construct_multipart(data):
    """
    Construction of the body of the setConf request.
    """
    multi_part = QHttpMultiPart(QHttpMultiPart.FormDataType)
    for key, value in data.items():
        post_part = QHttpPart()
        post_part.setHeader(QNetworkRequest.ContentDispositionHeader, 
            "form-data; name=\"{}\"".format(key))
        post_part.setBody(str(value).encode())
        multi_part.append(post_part)
    return  multi_part

def isTokenValid(accessToken, refreshToken):
    """
    Check if the access token is still valid and request a new one if refresh token still is
    """
    expAcc = 0
    try:
        expAcc = jwt.decode(accessToken, algorithms=["RS256"],
        options={"verify_signature": False})['exp']
    except:
        print("No token found")
        return False, False

    if expAcc < time.time():
        if jwt.decode(refreshToken, algorithms=["HS256"],
        options={"verify_signature": False})['exp'] < time.time():
            return False, False
        else:
            return False, True
    return True, True

def getTokens(manager, authCode=None, code_verifier=None, refreshToken=None, 
state=None):
    """
    Call of the Keycloak's token andpoint to get the Access, Refresh and ID token.
    """
    data = QByteArray()
    if authCode:
        data.append(b'code=' + bytes(authCode,"UTF-8") +b'&')
        data.append(b'grant_type=authorization_code&')
        data.append(b'code_verifier='+ bytes(code_verifier, 'UTF-8') + b'&')
        data.append(b'session_state=' + bytes(state, 'UTF-8') + b'&')
    if refreshToken:
        data.append(b'refresh_token=' + bytes(refreshToken, 'UTF-8') + b'&')
        data.append(b'grant_type=refresh_token&')
    data.append(b'client_id=QtConf&')
    data.append(b'client_secret=doJwXvfdVK1KHLINx3x9GUPOvmcQd32d&')
    data.append(b'scope=openid&')
    data.append(b'redirect_uri=http://localhost:22222/oidc_callback')
    url = 'http://servix1:8080/realms/conf/protocol/openid-connect/token'
    req = QNetworkRequest(QUrl(url))
    req.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader,
    'application/x-www-form-urlencoded')
    manager.post(req, data)

def cmpCall(window, accessToken, pwd):
    """
    Make a CMP request to the PKI
    """
    #generate key
    s= string.ascii_letters + string.digits
    keyFileName = ''.join(random.sample(s, 10))
    genKeyCmd = window.openssl +' genrsa -out ' + window.certWorkDir + keyFileName + '.pem" 2048'
    subprocess.run(shlex.split(genKeyCmd))
    print('Key Generation : OK')
    username=''
    dn = ''
    try:
        username = jwt.decode(accessToken, algorithms=["RS256"],
        options={"verify_signature": False})['preferred_username']
        dn = jwt.decode(accessToken, algorithms=["RS256"],
        options={"verify_signature": False})['name']
    except:
        print("CP Call : No token found")
    cmpCmd= window.openssl + ' cmp -cmd ir -server ce01.solitude.skyrim -path ejbca/publicweb/cmp/enrollClient -srvcert ".\\certs\\ManagementCA.pem" -ref '+ username +' -secret pass:'+ pwd+' -certout '+ window.certWorkDir + keyFileName +'.crt" -newkey '+ window.certWorkDir + keyFileName +'.pem" -subject "/CN='+dn+'" '
    subprocess.run(shlex.split(cmpCmd))
    print('CMP : OK')
    return keyFileName

def enrollAfterValid(window, accessToken, pwd):
    """
    Generate Key and call the PKI with CMP protocol
    """
    #generate key
    s= string.ascii_letters + string.digits
    keyFileName = ''.join(random.sample(s, 10))
    genKeyCmd = window.openssl +' genrsa -out ' + window.certWorkDir + keyFileName + '.pem" 2048'
    subprocess.run(shlex.split(genKeyCmd))
    print('Key Generation : OK')
    username=''
    dn = ''
    try:
        username = jwt.decode(accessToken, algorithms=["RS256"],
        options={"verify_signature": False})['preferred_username']
        dn = jwt.decode(accessToken, algorithms=["RS256"],
        options={"verify_signature": False})['name']
    except:
        print("CP Call : No token found")
    cmpCmd= window.openssl + ' cmp -cmd ir -server ce01.solitude.skyrim -path ejbca/publicweb/cmp/enrollClient -srvcert ".\\certs\\ManagementCA.pem" -ref '+ username +' -secret pass:'+ pwd+' -certout '+ window.certWorkDir + keyFileName +'.crt" -newkey '+ window.certWorkDir + keyFileName +'.pem" -subject "/CN='+dn+'" '
    subprocess.run(shlex.split(cmpCmd))
    print('CMP : OK')
    return keyFileName