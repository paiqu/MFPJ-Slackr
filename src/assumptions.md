#### Assumptions in channel_messages_test function
    - returns '-1' in 'end' when no more messages to load after this return
    - returns the most recent messages in the channel up to last 50

#### Assumptions in channels_list function:
    - user_token is valid
    - return the channels' detial in the order that channels were been created
    
#### Assumptions in channels_list function:
    - user_token is vaild
    - return the channels' detial in the order that channels were been created

#### Assumptions in message_edit function:
    - new texts are less than 1000 characters
    - new texts could be empty
    - user that calling this function to edit is a valid user
    - user is a part of this channel
