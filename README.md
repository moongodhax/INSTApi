# INSTApi
Python Instagram Private Api
It's Instagram's mobile API. 
It contains not all possible methods.

Example:

from INSTApi.Client import INSTApi_Client

login = 'YOUR_LOGIN'
password = 'YOUR_PASSWORD'
proxy = login:password@127.0.0.1:5000 # or 127.0.0.1:5000 or None if proxy not needed

try:
    api = INSTApi_Client(login, password, proxy)
    if not api.login_success:
        if (api.challenge):
            method = None
            while(method != "0" and method != "1"):
                print("Enter auth method:")
                print("0 - Send code to mobile phone")
                print("1 - Send code to email")
                print("2 - Cancel")
                method = input("Enter number: ")
                if (method == "2"):
                    method = None
                    break
                
            if (method == None): 
                print('Authorization: cancel')
                return False
            
            api.verify_method = method
            res = api.start_challenge()
            if (res):
                code = input("Введите код: ")
                
                if (code == None): 
                    print('Authorization: cancel')
                    return False
                
                res = api.send_code(code)
        
        if (not api.challenge_passed):
            print('Error: challenge not passed')
            return False

except INSTApi.utils.Errors.ClientLoginError:
    print('Error: wrong login or password')
    return False
except:
    print('Authorization: error')
    return False

