from ..Utils import INSTApi_Utils

import time
import random
import json

class INSTApi_Upload(INSTApi_Utils):
    def upload_photo(me, file_bytes):
        upload_id = str(round(time.time() * 1000))
        name = f'{upload_id}_0_$' + str(random.randint(1000000000, 9999999999))
        content_length = str(len(file_bytes))
        
        headers = me.default_headers
        params = me.authenticated_params
        
        headers.update({
            'X_FB_PHOTO_WATERFALL_ID': me.generate_uuid(),
            'X-Entity-Type': 'image/jpeg',
            'Offset': '0',
            'X-Instagram-Rupload-Params': json.dumps(me.create_photo_rupload_params(upload_id)), # options, 
            'X-Entity-Name': name,
            'X-Entity-Length': content_length,
            'Content-Type': 'application/octet-stream',
            'Content-Length': content_length,
            'Accept-Encoding': 'gzip'
        })
        
        url = f'https://i.instagram.com/rupload_igphoto/{name}'
        resp = me.s.post(url, data = file_bytes, params = params, headers = headers)
        
        res = resp.json()
        if (res["status"] != "ok"): return False
        else: return upload_id
    
    def create_photo_rupload_params(me, upload_id): # options, 
        ruploadParams = {
            'retry_context': json.dumps({'num_step_auto_retry': 0,' num_reupload': 0,' num_step_manual_retry': 0}),
            'media_type': '1',
            'upload_id': str(upload_id),
            'xsharing_user_ids': json.dumps([]),
            'image_compression': json.dumps({'lib_name': 'moz', 'lib_version': '3.1.m', 'quality': '80'}),
        }
        # if (options.isSidecar):
            # ruploadParams.is_sidecar = '1'
        return ruploadParams