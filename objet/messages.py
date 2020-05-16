class User_msg():
    def __init__(self,content):

        self.sender = 'u'
        self.type_msg = 'p'
        self.content = content

class Chatbot_msg():
    def __init__(self,content):
        self.sender = 'c'
        self.type_msg = 'p'
        self.content = content

class Chatbot_list():
    def __init__(self,content):
        self.sender = 'c'
        self.type_msg = 'l'
        self.content = content

class Chatbot_fiche():
    def __init__(self,content):
        self.sender = 'c'
        self.type_msg = 'f'
        self.content = content