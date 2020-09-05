from .utils.endpoints.Account import INSTApi_Account 
from .utils.endpoints.Media import INSTApi_Media
from .utils.endpoints.Upload import INSTApi_Upload
from .utils.services.Publish import INSTApi_Publish
from .utils.endpoints.Feed import INSTApi_Feed
from .utils.endpoints.Challenge import INSTApi_Challenge
from .utils.endpoints.User import INSTApi_User
from .utils.endpoints.Friendships import INSTApi_Friendships

import requests

class INSTApi_Client(
                     INSTApi_Account, 
                     INSTApi_Media, 
                     INSTApi_Upload, 
                     INSTApi_Publish, 
                     INSTApi_Feed, 
                     INSTApi_Challenge, 
                     INSTApi_User, 
                     INSTApi_Friendships
                    ):
    def __init__(me, username, password, proxy = None, device_string = None):
        me.s = requests.Session()
        
        if proxy:
            me.s.proxies = {
                'http': 'http://' + str(proxy),
                'https': 'http://' + str(proxy)
            }
        
        me.username = username
        me.password = password
        
        me.device_string = device_string if device_string != None else me.get_device()
        me.uuid = me.generate_uuid(False)
        me.device_id = me.generate_deviceid()
        me.session_id = me.generate_uuid(False)
        me.signature_key = '19ce5f445dbfd9d29c59dc2a78c616a7fc090a8e018b9267bc4240a30244c53b'
        me.key_version = '4'
        me.ig_capabilities = '3brTvw=='
        me.application_id = '567067343352427'
        me.user_agent = me.generate_useragent()
        me.ad_id = me.generate_adid()
        
        me.challenge = False
        me.challenge_passed = False
        me.challenge_url = ""
        me.verify_method = 1
        
        me.login_success = me.login()