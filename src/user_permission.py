'''Route implementation for admin/user/permission/change

Members in a channel have one of two channel permissions.


1) Owner of the channel (the person who created it, and whoever else that creator adds)
2) Members of the channel


Slackr user's have two global permissions


1) Owners, who can also modify other owners' permissions. (permission_id 1)
2) Members, who do not have any special permissions. (permission_id 2)


All slackr users are by default members, except for the very first user who signs up, who is an owner
'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from token_functions import generate_token
from class_file import User, Channel
from data import DATA, getData


PERMISSION = Blueprint('permission', __name__)


@PERMISSION.route('/admin/userpermission/change', methods=['POST'])


def admin():

    info = request.get_json()
    token = info['token']
    u_id = info['token']

    #can I call this variable below?
    permission_id = info['permission_id']
    admin_permission(token, u_id, permission_id)

    return dumps({})

def admin_permission(token, u_id, permission_id):
    '''
    Change the permission ID to 2, this means that a user is now an owner of a channel
    User must already be a member of a channel in order for permissions to change  
    '''
    for user in users:
        if user['u_id'] == token_to_uid(token):
            admin_user = user
    for user in users:
        if user['u_id'] == u_id:
            sub_user = user         

    # Checks the User ID is valid
    if user_id_check(u_id) == True:

        # The admin user has permission priviledges 
        if admin_user['global_permission'] == 1 || admin_user['channel_permission'] == 3:

            if permission_id == 1:

                if admin_user['global_permission'] == 1:
                    sub_user['global_permission'] == permission_id
                    sub_user['channel_permission'] == 3 
                else: 
                    raise AccessError("The admin user does not have global permission privileges")   
            elif permission_id == 3:
                if admin_user['channel_permission'] == 3:
                    sub_user['channel_permission'] == permission_id
                else:
                    raise AccessError("The admin user does not have channel permission privileges")

            else: 
                raise InputError('This is not a valid permission number')


        else: 
            raise AccessError("The admin user is not authorised")    

    else: 
        raise InputError("This is not a valid user or user ID")    
    '''
    if admin_user[permission_id] == 2
        permission_user['permission_id'] = 2 
    '''
    return {}

    

