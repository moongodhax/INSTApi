from ..Utils import INSTApi_Utils

class INSTApi_User(INSTApi_Utils):
    def username_info(me, username):
        res = me.call_api('users/{username!s}/usernameinfo/'.format(**{'username': username})).json()
        return res