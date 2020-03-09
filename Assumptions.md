# Assumptions


COMP1531 Major Project 
Markdown for Iteration 1: Test Driven Development 
By Juliette Inglis, Zebin Chen, Haofu Chen, Xinlei Chang, Pai Qu


### Assumptions for auth_login (Juliette Inglis): 
   - When a user is logging in, the password is case sensitive. 
   - User cannot login with their handle or u_id. They must log in with their email.
   - At this stage, there is an unlimited number of log in attempts.

### Assumptions for auth_logout (Juliette Inglis):
   - We will be using the assert function to test for token validity 
   - When user logs out successfully - the token will return True 
   - When user does not log out successfully, token will return False
   - The string ‘Invalid Token’ string is what we use to currently represent an invalid token.

### Assumptions for auth_register (Juliette Inglis): 
   - As of yet, there are no further password restrictions such as needing a capital letter, number etc. Due to this, the only password restriction is that the password must be greater than 6 character (as written in project specifications). Currently password does not have a maximum length.
   - Users are allowed the same first name, last name, password - but not the same email.
   - When using tokens in the parameters of all future functions, we will be using the token returned from the auth_register function.

### Assumptions for channels_Invite (Juliette Inglis): 
   - As aforementioned, the token in parameters is the admin user’s token from their registration 
   - The first user invited to the channel is the admin/owner
   - The owner is not allowed to invite him/herself to the channel - he/she is automatically added during channel creation . As such, a channel invite function cannot hold the same user for token and u_id parameters
   - A user does not need to be logged in in order to invite other users to a channel - the same applies to the user being invited 
   - A user cannot invite himself to a channel within the channel_invite function (this happens in channel_add
   - A user who is not part of a channel himself, is not allowed to invite another user to that channel. I.e. A user must be a member of the channel themselves before inviting someone else.
   - The token called in the function parameter is the returned function of user_register of the admin user
   - Instead of declaring a variable for invalid user or invalid channel , when a user or channel ID should return an error, I wrote the parameters as either: (user_id +5) or (channel_id + 5). I inserted the invalid parameters like this because there could be an instance in the tests where the user/channel ID is the same as a random invalid number variable (which I chose myself) 

### Assumptions for channel_details (Juliette Inglis):
   - The first user added to the channel is the admin/owner
   - Aka the user that the token parameter In channels_create is the owner/admin of the channel 
   - A user who is not part of a channel himself, is not allowed to ask details about that channel . I.e. A user must be a member of the channel themselves before requesting channel details
   - The token called in the function parameter is the returned function of user_register of the admin user 
   - All_members dictionary includes the list of owner_members 
   - Order of member is according to date added (oldest first) 
   - The owner of the slackr is not allowed to print channel details, unless he is part of the channel. This may be changed in the second iteration.

### Assumptions for channel_messages function (Zebin Chen):
   - Assume there is at least one message in channel for all test functions 

### Assumptions for channel_leave (Pai Qu):
   - Assume owner of the channel remains as the owner when he/she leaves the channel
   - If the owner member of the channel leaves the channel, the next oldest user automatically becomes the new owner, if there are currently no other owner members.
   
### Assumptions for channel_join (Pai Qu):
   - The owner of _slackr_ is not allowed to join a private channel if he/she is not the owner
   - Owner of _slackr_ is not allowed to join the channel if he/she has not been invited by a member of said chnnel 

### Assumptions for channel_addowner (Pai Qu):
   - One channel can have multiple owners, but cannot exist with no owners 

### Assumptions for channel_removeowner (Pai Qu):
   - A channel has to have one owner (at least)
   - A user who is removed as an owner of the channel is still a member of said channel 

### Assumptions in channels_list function (Zebin Chen):
   - user_token is valid
   - user_token variable is the returned token of user_register function 
   - Only the user can call the channels_list function (telling them which channels they belong to)
   - return the channels details function in the order by which the channels were created

### Assumptions in channels_listall function (Zebin Chen):
   - user_token is vaild
   - user_token variable is the returned token of user_register function 
   - return the channels' detial in the order that channels were been created

### Assumptions for channels_create function (Xinlei Zhang):
  - All users can create channel a channel (there are no limits on the number of channels at one time)
  - The creator of the channel is the admin/owner of the channel - unless manually changed in another function 
  - Channel name cannot be 0 characters or greater than 20 characters
  - Different channels cannot have the same name.
  - A private channel also cannot have the same name as a public channel
  - When user creates the second channel, it will not leave the first channel it creates.
  - A user does not need to be logged in. Once a user has been registered, it will log in automatically. 

### Assumptions for message_send function (Xinlei Zhang):
  - All the users in channel can send messages.(no limit on the number)
  - The contents of messages sent can be the same.
  - Empty message cannot be sent.
  - Message content must be less than 1000 characters.
  - A user does not need to be logged in. Once a user has been registered, it will log in automatically. 

### Assumptions for message_remove function (Xinlei Zhang):
  - Messages only can be removed by the sender or the owner/admin of this channel.
  - The information related to the removed message (message_id, sending time) will also be removed when the message is removed.
  - At least one message must have been sent when calling message_remove function.
  - A user does not need to be logged in. Once a user has been registered, it will log in automatically. 
  - I used (channel_id + 5) to make sure that it is definitely different to the channel_id when calling errors. Because channel_id is a random return value, if I use a random number, it may be the same in some cases.

### Assumptions in message_edit function (Zebin Chen):
   - new texts are less than 1000 characters
   - If new text is edited to be empty, the message is automatically deleted.
   - user that calls this function to edit is a valid user
   - user calling the message_edit function is a part of this channel

### Assumptions for user_profile function (Xinlei Zhang):
   - All users can call the user profile function.
   - A user does not need to be logged in. Once a user has been registered, it will log in automatically. 
   - I used (user_id + 4) to make sure that it is definitely different with the user_id. Because user_id is a random return value, if I use a random number, it may be the same in some cases.

### Assumption in User_profile_setname (Haofu CHEN):
   - This function is to update the authorised user's first and last name after user has registered.
   - User cannot enter more than 100 letters for the first and last name, and also cannot enter the zero or negative for the first and last name.
   - When the user entered the words of first and last name that is not between 1 and 50, this function will return the error.

### Assumption in User_profile_setemail (Haofu CHEN):
   - This function is to update the authorised user's email address when user has registered.
   - When the user enters an email address that is invalid or email address has already used by another user, the test function will return an eror

### Assumption in User_profile_sethandle (Haofu CHEN):
   - This function is to update the authorised user's handle when user has registered.
   - If the user enters a character length less than 3 or greater than 20, returns error
   - If handle name is already being used by another user, returns error 

### Assumption in Users_all_test (Haofu CHEN):
   - This function will return a list of all users and their information.
   - We assume that there will always be at least one user registered 
   - When use this function, it return the all users associated details.
    (like "user'id", "user's email", "user's first and last name", "user's handle name")
 
### Assumptions for search (Pai Qu):
   - Messages in the private channel can be searched
   - The search is case-sensitive
