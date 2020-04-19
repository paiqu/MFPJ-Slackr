'''Route implementation for admin/user/permission/change

Slackr user's have two global permissions


1) Owners, who can also modify other owners' permissions. (permission_id 1)
2) Members, who do not have any special permissions. (permission_id 2)


All slackr users are by default members, except for the very first user who signs up, who is an owner
'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, user_id_check
from error import InputError, AccessError
from data import getData


PERMISSION = Blueprint('permission', __name__)


@PERMISSION.route('/admin/userpermission/change', methods=['POST'])
def admin():

    '''
    Gets information from user
    '''
    info = request.get_json()
    token = info['token']
    u_id = int(info['u_id'])

    #can I call this variable below?
    permission_id = int(info['permission_id'])
    admin_permission(token, u_id, permission_id)

    return dumps({})

def admin_permission(token, u_id, permission_id):
    '''
    Change the permission ID to 2, this means that a user is now an owner of a channel
    User must already be a member of a channel in order for permissions to change
    '''

    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']


    # Checks the User ID is valid
    if user_id_check(u_id) == False:
        raise InputError("This is not a valid user or user ID")


    # If the wrong permission ID is entered
    if permission_id != 1:
        raise InputError('This is not a valid permission number')


    for user in users:
        if user['u_id'] == token_to_uid(token):
            admin_user = user


    #print(token_to_uid(token))
    #print(token)

    for user in users:
        if user['u_id'] == u_id:
            sub_user = user



    # The admin user has permission privileges
    if admin_user['global_permission'] != 1:
        raise AccessError("The admin user is not authorised")

    #changes the sub users permission having passed all checks

    #### IS THIS RIGHT?
    sub_user['global_permission'] = permission_id
    sub_user['is_slack_owner'] = True


    for channel in channels:
        for user in channel['members']:
            if user == sub_user:
                channel['owners'].append(sub_user)



    #changes the users permission privileges to owner if they aren't already owner
    #for channel in channels_list(sub_user['token'])['channels']:
        #if sub_user not in channel['owners']:
            #channel_addowner(admin_user['token'], channel['channel_id'], sub_user['u_id'])

    return {}
