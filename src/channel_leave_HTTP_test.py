from json import load, dumps
import urllib.request
import urllib.parse
import pytest

PORT = 5817
BASE_URL = 'http://127.0.0.1:' + str(PORT)

def test_route_channel_leave():
    req = urllib.request.urlopen(f'{BASE_URL}/channel/leave')
    