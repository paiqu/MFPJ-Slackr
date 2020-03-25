import hashlib
from json import dumps
import jwt
from flask import Flask, request
from data import * 
        
def getData():
    global data
    return data

def generateToken(u_id):
    global SECRET
    encoded = jwt.encode({'u_id': u_id}, SECRET, algorithm=["HS256"])
    print(encoded)
    return str(encoded)