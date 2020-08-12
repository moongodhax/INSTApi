import urllib
import uuid
import hashlib
import random
import json
import hmac
from datetime import datetime
import base64
import time

from .data.devices import devices

class INSTApi_Utils:
    def call_api(me, endpoint, params = {}, query = None, files = {}, unsigned = False, needs_auth = True, headers = {}, full_url = False):
        if(params != '' and needs_auth == False): params.update(me.authenticated_params)
        
        url = ''
        if not full_url: url = 'https://i.instagram.com/api/v1/{0}'.format(endpoint)
        else: url = endpoint
        
        if query: url += ('?' if '?' not in endpoint else '&') + urllib.parse.urlencode(query)

        headers.update(me.default_headers)
        post_params = {}
        if params or params == '':
            headers['Content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            if params != '': 
                if not unsigned:
                    json_params = json.dumps(params, separators=(',', ':'))
                    hash_sig = me.generate_signature(json_params)
                    post_params = {
                        'ig_sig_key_version': me.key_version,
                        'signed_body': hash_sig + '.' + json_params
                    }
                else:
                    post_params = params

        data = me.s.post(url, data = post_params, files = files, headers = headers)
        
        return data
    
    def generate_uuid(me, return_hex=False, seed=None):
        if seed:
            m = hashlib.md5()
            m.update(seed.encode('utf-8'))
            new_uuid = uuid.UUID(m.hexdigest())
        else:
            new_uuid = uuid.uuid1()
        if return_hex:
            return new_uuid.hex
        return str(new_uuid)
    
    def generate_deviceid(me, seed=None):
        return 'android-{0!s}'.format(me.generate_uuid(True, seed)[:16])
    
    def generate_useragent(me):
        return f'Instagram 76.0.0.15.395 Android ({me.device_string}; en_US 138226743)'
    
    def generate_signature(me, data):
        return hmac.new(
            me.signature_key.encode('ascii'), data.encode('ascii'),
            digestmod=hashlib.sha256).hexdigest()
    
    def generate_adid(me, seed=None):
        modified_seed = seed or me.authenticated_user_name or me.username
        if modified_seed:
            # Do some trivial mangling of original seed
            sha2 = hashlib.sha256()
            sha2.update(modified_seed.encode('utf-8'))
            modified_seed = sha2.hexdigest()
        return me.generate_uuid(False, modified_seed)
  
    def get_device(me):
        # return random.choice(devices)
        return devices[0]

    def gen_user_breadcrumb(me, size):
        """
        Used in comments posting.

        :param size:
        :return:
        """
        key = 'iN4$aGr0m'
        dt = int(time.time() * 1000)

        # typing time elapsed
        time_elapsed = random.randint(500, 1500) + size * random.randint(500, 1500)

        text_change_event_count = max(1, size / random.randint(3, 5))

        data = '{size!s} {elapsed!s} {count!s} {dt!s}'.format(**{
            'size': size, 'elapsed': time_elapsed, 'count': text_change_event_count, 'dt': dt
        })
        return '{0!s}\n{1!s}\n'.format(
            base64.b64encode(hmac.new(key.encode('ascii'), data.encode('ascii'), digestmod=hashlib.sha256).digest()),
            base64.b64encode(data.encode('ascii')))
    
    @property
    def device_payload(me):
        device_parts = me.device_string.split(';')
        (android_version, android_release) = device_parts[0].split('/')
        temp = device_parts[3].split('/')
        model = device_parts[4]
        return {
            'android_version': android_version,
            'android_release': android_release,
            'manufacturer': temp[0],
            'model': model,
        }
    
    @property
    def csrftoken(me):
        """The client's current csrf token"""
        return me.s.cookies.get('csrftoken')

    @property
    def authenticated_user_id(me):
        """The current authenticated user id"""
        return me.s.cookies.get('ds_user_id')
    
    @property
    def authenticated_user_name(me):
        """The current authenticated user name"""
        return me.s.cookies.get('ds_user')
    
    @property
    def default_headers(me):
        return {
            'User-Agent': me.user_agent,
            'Connection': 'close',
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-Capabilities': me.ig_capabilities,
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Connection-Speed': '{0:d}kbps'.format(random.randint(1000, 5000)),
            'X-IG-App-ID': me.application_id,
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-FB-HTTP-Engine': 'Liger',
        }
    
    @property
    def authenticated_params(me):
        return {
            '_csrftoken': me.csrftoken,
            '_uuid': me.uuid,
            '_uid': me.authenticated_user_id
        }
    
    @property
    def phone_id(me):
        """Current phone ID. For use in certain functions."""
        return me.generate_uuid(return_hex=False, seed=me.device_id)
    
    @property
    def timezone_offset(self):
        """Timezone offset in seconds. For use in certain functions."""
        return int(round((datetime.now() - datetime.utcnow()).total_seconds()))
        
    @property
    def radio_type(self):
        """For use in certain endpoints"""
        return 'wifi-none'