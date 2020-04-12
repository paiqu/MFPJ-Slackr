# may need a function to transfer token to u_id
class User:
    def __init__(self, u_id, email, name_first, name_last):
        self.u_id = u_id
        self.email = email
        self.password = ''
        self.name_first = name_first
        self.name_last = name_last
        self.handle = ""
        self.global_permission= 2
        self.is_slack_owner = False
        self.is_login = False
         

class Channel:
    def __init__(self, channel_id, channel_name):
        # DONT'T FORGET TO UPDATE members and owners when create a new channel
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.members = [] # a list of users who are members
        
        self.owners = []  # a list of users who are owners
        self.is_public = True
        self.is_standup_active = False
        self.game_on = False
    
class Message:
    def __init__(self, message_content, message_id, channel_id, sender_id, time):
        self.message_content = message_content
        self.message_id = message_id
        self.channel_id = channel_id
        self.sender_id = sender_id
        self.time_created = time
        self.is_pin = False
        
class React:
    def __init__(self, message_id, u_id, react_id):
        self.message_id = message_id
        self.u_id = u_id
        self.react_id = react_id

class Standup:
    def __init__(self, channel_id, time_end):
        self.channel_id = channel_id
        self.time_end = time_end
        self.messages = []
