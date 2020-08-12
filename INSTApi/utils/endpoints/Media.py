from ..Utils import INSTApi_Utils

import datetime
import re

class INSTApi_Media(INSTApi_Utils):
    def apply_configure_defaults(me, options, defaults):
        width = options['width'] or 1520
        height = options['height'] or 2048
        
        resp = {
            'device': me.device_payload,
            'extra': {
                'source_width': width, 
                'source_height': height
            }
        }
        resp.update(defaults)
        resp.update(me.authenticated_params)
        
        return resp

    def configure(me, options):
        dt = datetime.date.today()
        now = dt.strftime("%d:%m:%Y %H:%M:%S")
        
        width = options['width'] or 1520
        height = options['height'] or 2048

        params = me.apply_configure_defaults(options, {
            # width,
            # height,
            'upload_id': options['upload_id'] or str(round(time.time() * 1000)),
            'timezone_offset': "10800",
            'date_time_original': now,
            'date_time_digitalized': now,
            'caption': '',
            'source_type': '4',
            'media_folder': 'Camera',
            'edits': {
                'crop_original_size': [width, height],
                'crop_center': [0.0, -0.0],
                'crop_zoom': 1.0,
            },
            'camera_model': me.device_payload['model'],
            'scene_capture_type': 'standard',
            'device_id': me.device_id,
            'creation_logger_session_id': me.session_id,
            'software': '1',
            'camera_make': me.device_payload['manufacturer'],
        })
        
        resp = me.call_api('media/configure/', params = params)
        
        res = resp.json()
        if (res["status"] != "ok"): return False
        else: return res
    
    def configure_to_story(me, options):
        dt = datetime.date.today()
        now = dt.strftime("%d:%m:%Y %H:%M:%S")
        
        width = options['width'] or 1520
        height = options['height'] or 2048

        params = me.apply_configure_defaults(options, {
            'upload_id': options['upload_id'] or str(round(time.time() * 1000)),
            'source_type': '3',
            'configure_mode': '1',
            'client_shared_at': now,
            'edits': {
                'crop_original_size': [width, height],
                'crop_center': [0.0, -0.0],
                'crop_zoom': 1.0,
            }
        })
        
        resp = me.call_api('media/configure_to_story/', params = params)
        
        res = resp.json()
        if (res["status"] != "ok"): return False
        else: return res

    def post_comment(me, media_id, comment_text):
        """
        Post a comment.
        Comment text validation according to https://www.instagram.com/developer/endpoints/comments/#post_media_comments

        :param media_id: Media id
        :param comment_text: Comment text
        :return:
            .. code-block:: javascript

                {
                  "comment": {
                    "status": "Active",
                    "media_id": 123456789,
                    "text": ":)",
                    "created_at": 1479453671.0,
                    "user": {
                      "username": "x",
                      "has_anonymous_profile_picture": false,
                      "profile_pic_url": "http://scontent-sit4-1.cdninstagram.com/abc.jpg",
                      "full_name": "x",
                      "pk": 123456789,
                      "is_verified": false,
                      "is_private": false
                    },
                    "content_type": "comment",
                    "created_at_utc": 1479482471,
                    "pk": 17865505612040669,
                    "type": 0
                  },
                  "status": "ok"
                }
        """

        if len(comment_text) > 300:
            logger.write(f"The total length of the comment cannot exceed 300 characters.")
            return False
        if re.search(r'[a-z]+', comment_text, re.IGNORECASE) and comment_text == comment_text.upper():
            logger.write(f"The comment cannot consist of all capital letters.")
            return False
        if len(re.findall(r'#[^#]+\b', comment_text, re.UNICODE | re.MULTILINE)) > 4:
            logger.write(f"The comment cannot contain more than 4 hashtags.")
            return False
        if len(re.findall(r'\bhttps?://\S+\.\S+', comment_text)) > 1:
            logger.write(f"The comment cannot contain more than 1 URL.")
            return False

        endpoint = 'media/{media_id!s}/comment/'.format(**{'media_id': media_id})
        params = {
            'comment_text': comment_text,
            'user_breadcrumb': me.gen_user_breadcrumb(len(comment_text)),
            'idempotence_token': me.generate_uuid(),
            'containermodule': 'comments_feed_timeline',
            'radio_type': me.radio_type,
        }
        params.update(me.authenticated_params)
        
        resp = me.call_api(endpoint, params=params)
        res = resp.json()
        if (res["status"] != "ok"): return False
        else: return res