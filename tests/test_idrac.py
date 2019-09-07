from server_control.objects.server.idrac_commands_dell import IdracApi

class TestIdrac:

    def __init__(self):
        self.idrac = IdracApi()

    def test_cookies(self):
