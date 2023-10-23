import logging

from flask import Flask, request, g, abort
from flask_oidc import OpenIDConnect
from requests import Session
from zeep import Client, Transport

import random, string



#logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False, # If True cookis are sent only with https
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True, #If true, client can access user's data
    'OIDC_SCOPES': ['openid', 'email', 'profile', 'roles'], # What scopes will the client request from the AS
    'OIDC_OPENID_REALM': 'conf',
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_TOKEN_TYPE_HINT': 'access_token'
})

oidc = OpenIDConnect(app)

@app.route('/getConf', methods=['GET'])
@oidc.accept_token(require_token=True, scopes_required=["openid"])
def getConf():
    """OAuth 2.0 protected API endpoint accessible via AccessToken"""
    xml = open("config.xml", 'r')
    return xml

@app.route('/setConf', methods=['POST'])
@oidc.accept_token(require_token=True, scopes_required=['openid'])
def setConf():
    """OAuth 2.0 protected API endpoint accessible via AccessToken"""
    roles = g.oidc_token_info['realm_access']['roles']
    if 'confEditor' in roles:
        if request.form["conf"]:
            f =open("config.xml", "w")
            f.write(request.form['conf'])
            f.close()
            return "Upload successful"
        else:
            return "An error has occured"
    else:
        return abort(403)

@app.route('/enrollAuto', methods=['GET'])
@oidc.accept_token(require_token=True, scopes_required=["openid"])
def enrollAuto():
    username= g.oidc_token_info['preferred_username']
    email = g.oidc_token_info['email']
    dn = 'CN='+g.oidc_token_info['name']
    pwd = add_user(username, email, dn)
    return pwd

@app.route('/enrollValid', methods=['GET'])
@oidc.accept_token(require_token=True, scopes_required=["openid"])
def enrollAuth():
    username= g.oidc_token_info['preferred_username']
    email = g.oidc_token_info['email']
    dn = 'CN='+g.oidc_token_info['name']
    pwd = add_userValid(username, email, dn)
    return pwd



def add_user(username, email, dn):
    #gen random password
    s = string.ascii_letters + string.digits
    randpwd=''.join(random.sample(s, 5))

    #API call
    session= Session()
    session.verify = False
    session.cert = (
        'C:\\Users\\admin\\Documents\\flaskapp-conf\\certs\\flask.crt',
        'C:\\Users\\admin\\Documents\\flaskapp-conf\\certs\\flask.key')
    transport = Transport(session=session)
    wsdl = 'https://ce01.solitude.skyrim/ejbca/ejbcaws/ejbcaws?wsdl'
    client= Client(wsdl=wsdl, transport=transport)
    userDataType = client.get_type('ns0:userDataVOWS')
    userData = userDataType(
        caName='ManagementCA',
        status= 10,
        certificateProfileName='ENDUSER',
        tokenType='USERGENERATED',
        clearPwd= True,
        keyRecoverable=False,
        sendNotification=False ,
        endEntityProfileName= "EMPTY",
        password= randpwd,
        subjectDN= dn,
        username= username,
        email= email)
    client.service.editUser(userData)
    return randpwd


def add_userValid(username, email, dn):
    #gen random password
    s = string.ascii_letters + string.digits
    randpwd=''.join(random.sample(s, 5))
    print(randpwd)

    #API call
    session= Session()
    session.verify = False
    session.cert = (
        'C:\\Users\\admin\\Documents\\flaskapp-conf\\certs\\flask.crt',
        'C:\\Users\\admin\\Documents\\flaskapp-conf\\certs\\flask.key')
    transport = Transport(session=session)
    wsdl = 'https://ce01.solitude.skyrim/ejbca/ejbcaws/ejbcaws?wsdl'
    client= Client(wsdl=wsdl, transport=transport)
    userDataType = client.get_type('ns0:userDataVOWS')
    userData = userDataType(
        caName='ManagementCA',
        status = 10,
        certificateProfileName='ENDUSERCustom',
        tokenType='USERGENERATED',
        clearPwd= True,
        keyRecoverable=False,
        sendNotification=False ,
        endEntityProfileName= "EEProfilesSOValidation",
        password= randpwd,
        subjectDN= dn,
        username= username,
        email= email)
    client.service.editUser(userData)
    return randpwd




if __name__ == '__main__':
    app.run(host='0.0.0.0')