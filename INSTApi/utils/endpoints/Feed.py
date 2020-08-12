from ..Utils import INSTApi_Utils

class INSTApi_Feed(INSTApi_Utils):
    def feed_timeline(me, **kwargs):
        """
        Get timeline feed. To get a new timeline feed, you can mark a set of media
        as seen by setting seen_posts = comma-separated list of media IDs. Example:
        ``api.feed_timeline(seen_posts='123456789_12345,987654321_54321')``

        :param kwargs:
            - **max_id**: For pagination. Taken from ``next_max_id`` in the previous page.
        """
        
        params = {
            '_uuid': me.uuid,
            '_csrftoken': me.csrftoken,
            'is_prefetch': '0',
            'is_pull_to_refresh': '0',
            'phone_id': me.phone_id,
            'timezone_offset': me.timezone_offset,
        }
        params.update(kwargs)
        
        resp = me.call_api('feed/timeline/', params=params, unsigned=True)
        res = resp.json()
        if (res["status"] != "ok"): return False
        else: return res