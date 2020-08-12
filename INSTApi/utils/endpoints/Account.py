from ..Utils import INSTApi_Utils

from ..Errors import ClientError, ClientLoginError

class INSTApi_Account(INSTApi_Utils):
    def login(me):
        resp = me.call_api(
            'si/fetch_headers/',
            params = '',
            query = {
                'challenge_type': 'signup', 
                'guid': me.generate_uuid(True)
            },
        )

        if not me.csrftoken:
            raise ClientError('Unable to get csrf from prelogin.')

        login_params = {
            'device_id': me.device_id,
            'guid': me.uuid,
            'adid': me.ad_id,
            'phone_id': me.phone_id,
            '_csrftoken': me.csrftoken,
            'username': me.username,
            'password': me.password,
            'login_attempt_count': '0',
        }

        resp = me.call_api('accounts/login/', params = login_params)
        
        if not me.csrftoken:
            raise ClientError('Unable to get csrf from login.')
        
        login_json = resp.json()
        
        if (login_json.get('status') != 'ok'):
            if login_json.get('message') == 'challenge_required':
                me.challenge = True
                me.challenge_url = login_json.get('challenge', {}).get('url')
                return False
            elif not login_json.get('logged_in_user', {}).get('pk'):
                raise ClientLoginError('Unable to login.')
        else: return True
            
    def current_user(me):
        resp = me.call_api('accounts/current_user/', query = {'edit': 'true'})
        res = resp.json()
        if (res["status"] != "ok"): return False
        else: return res

    def edit_profile(me, first_name = False, biography = False, external_url = False, email = False, phone_number = False, gender = False):
        cur_info = me.current_user()
        
        if not cur_info: return False
        
        if not first_name:
            first_name = cur_info["user"]["full_name"]
        if not biography:
            biography = cur_info["user"]["biography"]
        if not external_url:
            external_url = cur_info["user"]["external_url"]
        if not email:
            email = cur_info["user"]["email"]
        if not phone_number:
            phone_number = cur_info["user"]["phone_number"]
        if not gender:
            gender = cur_info["user"]["gender"]

        params = {
            'username': me.authenticated_user_name,
            'gender': int(gender),
            'phone_number': phone_number,
            'first_name': first_name,
            'biography': biography,
            'external_url': external_url,
            'email': email,
        }
        
        resp = me.call_api('accounts/edit_profile/', params = params)
        res = resp.json()
        if (res["status"] != "ok"): return False
        else: return res
        
    def change_profile_picture(me, filename):
        photo_data = open(filename, 'rb').read()
        upload_id = me.upload_photo(photo_data)
        if not upload_id: return False
        
        params = {
            'use_fbuploader': True,
            'upload_id': upload_id,
        }
        
        resp = me.call_api('accounts/change_profile_picture/', params = params, unsigned = True)
        
        res = resp.json()
        if (res["status"] != "ok"): return False
        else: return res