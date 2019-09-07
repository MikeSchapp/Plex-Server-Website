import requests
import unittest
from server_control.objects.server.idrac_commands_dell import IdracApi
from mock import patch

class TestIdrac(unittest.TestCase):

    @staticmethod
    @patch('requests.Session.post')
    def test_cookies(patched_post):
        fake_session = requests.Session()
        fake_session.cookies._cookies = "test"
        patched_post.side_effect = [fake_session]
        IdracApi()
        print("test")
        patched_post.assert_called_with("test")
