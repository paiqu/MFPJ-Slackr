# may need a function to transfer token to u_id
class User:
    def __init__(self, u_id, email, name_first, name_last, handle):
        self.u_id = u_id
        self.email = email
        self.name_first = name_first
        self.name_last = name_last
        self.handle = handle
        self.is_slack_owner = False

class Channel:
    def __init__(self, channel_id, channel_name):
        # DONT'T FORGET TO UPDATE members and owners when create a new channel
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.members = [] # a list of users who are members
        
        self.owners = []  # a list of users who are owners
        self.is_public = True
    
class Message:
    def __init__(self, message_content, message_id, channel_id, sender_token):
        self.message_content = message_content
        self.message_id = message_id
        self.channel_id = channel_id
        self.sender_token = sender_token
        self.is_pin = False