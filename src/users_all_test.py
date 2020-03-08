import pytest
from user import user_profile,user_profile_sethandle
from auth import auth_register
from other import users_all
"""
Test return the correct list of users and informations
"""
#This function is to test the normal case to return correct informations
def test_users_all_success():
    #create a new user1 
    user_one = auth_register('z123456@unsw.edu.au', 'z123456', 'Honey', 'Jii')
    user_one_id = user_one["u_id"]
    token_one = user_one["token"] 
    user_one_handle = user_profile_sethandle(token_one, 'hfdjshg')
 
     #create a new user2 
    user_two = auth_register('z5237534@unsw.edu.au', 'z1234534', 'Candy', 'JiJi')
    user_two_id = user_two["u_id"]
    token_two = user_two["token"] 
    user_two_handle = user_profile_sethandle(token_two, 'Chocolate')
    # check whether they are same
    usersDict = users_all(token_one)['users'] # list of dict
    
    assert len(usersDict) == 2
    assert usersDict[0]['u_id'] == user_one_id
    assert usersDict[0]['email'] == 'z123456@unsw.edu.au'
    assert usersDict[0]['name_first'] == 'Honey'
    assert usersDict[0]['name_last'] == 'Jii'
    assert usersDict[0]['handle_str'] == 'hfdjshg'
    
    assert usersDict[1]['u_id'] == user_one_id
    assert usersDict[1]['email'] == 'z123456@unsw.edu.au'
    assert usersDict[1]['name_first'] == 'Candy'
    assert usersDict[1]['name_last'] == 'JiJi'
    assert usersDict[1]['handle_str'] == 'Chocolate'





    


    

    
