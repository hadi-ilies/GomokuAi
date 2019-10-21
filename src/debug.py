import sys

class Debug(object):
    def __init__(self):
        pass
    
    def debug(self, text: str):
        print("MESSAGE", text)
        sys.stdout.flush()

    def error(self, error: str):
        print("ERROR", error)
        sys.stdout.flush()