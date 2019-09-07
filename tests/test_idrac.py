import requests

from server_control.objects.server.idrac_commands_dell import IdracApi
from mock import patch

class TestIdrac():

    @staticmethod
    @patch('requests.Session.post')
    def test_cookies(patched_post):
        fake_session = requests.Session()
        fake_session = fake_session.cookies._cookies = "test"
        patched_post.side_effect = [fake_session]
        patched_post.assert_called()