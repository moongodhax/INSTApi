from ..Utils import INSTApi_Utils


class INSTApi_Friendships(INSTApi_Utils):
    def friendships_create(me, user_id):
        """
        Follow a user
        :param user_id: User id
        :return:
            .. code-block:: javascript
                {
                    "status": "ok",
                    "friendship_status": {
                        "incoming_request": false,
                        "followed_by": false,
                        "outgoing_request": false,
                        "following": true,
                        "blocking": false,
                        "is_private": false
                    }
                }
        """
        
        params = {
            'user_id': user_id, 
            'radio_type': 'wifi-none' # хуй его знает нахуя, но так было в другой либе
        }
        
        resp = me.call_api(f'friendships/create/{user_id}/', params = params)
        res = resp.json()
        if (res["status"] != "ok"): return False
        else: return res