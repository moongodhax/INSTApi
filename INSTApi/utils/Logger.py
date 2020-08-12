import datetime 

class Logger:
    def error(me, text): pass
    
    def write(me, text):
        d = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{d}] {text}")
    
    def start(me, text): pass

logger = Logger()