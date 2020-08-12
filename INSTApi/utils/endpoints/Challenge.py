from ..Utils import INSTApi_Utils

class INSTApi_Challenge(INSTApi_Utils):
    def start_challenge(me):
        headers = {
            'X-Requested-With': "XMLHttpRequest",
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': me.csrftoken,
            '17': me.challenge_url
        }
        params = {
            'choice': me.verify_method
        }
        resp = me.call_api(me.challenge_url, params = params, headers = headers, full_url = True)
        
        # print()
        # print("CHALLENGE")
        # print(resp.json())
        # print()
        
        challengeType = resp.json().get('challengeType')
        if (challengeType == "VerifyEmailCodeForm" or challengeType == "VerifySMSCodeForm"):
            return True
        else: return False
    
    def send_code(me, code):
        headers = {
            'X-Requested-With': "XMLHttpRequest",
            'X-Instagram-AJAX': '1',
            'X-CSRFToken': me.csrftoken,
            '17': me.challenge_url
        }
        params = {
            'security_code': code
        }
        resp = me.call_api(me.challenge_url, params = params, headers = headers, full_url = True)
    
        # print()
        # print("VERIFY")
        # print(resp.json())
        # print()
        
        if ("CHALLENGE_REDIRECTION" in resp.text): 
            me.challenge_passed = True
            return True
        else: 
            return False