import requests
from secret_store.config import *


class IdracApi:
    def __init__(self):
        self._session = requests.Session()
        self.retrieve_idrac_cookie()

    def retrieve_idrac_cookie(self):
        self._session = requests.Session()
        data = {
            'user': idrac_user,
            'password': idrac_pw
        }
        retry_count = 0
        while retry_count < 3:
            r = self._session.post(idrac_ip + '/data/login', data, verify=False)
            cookie_jar = r.cookies
            if len(cookie_jar._cookies) > 0:
                return r
            else:
                retry_count += 1
                continue
        raise TimeoutError

    def logout(self):
        r = self._session.get(idrac_ip + '/data/logout', verify=False)
        return r

    def turn_on(self):
        with self._session as session:
            r = session.post(idrac_ip + '/data?set=pwState:1', verify=False)
            return r

    def retrieve_idrac_data(self):
        with self._session as session:
            data = {
                'get': 'pwState'
            }
            r = session.post(idrac_ip + '/data?get=pwState', data, verify=False)
            if r.status_code != 200:
                self.retrieve_idrac_cookie()
                self.retrieve_idrac_data()
            if "0" in str(r.content):
                status = "off"
            else:
                status = "on"
            return status

    def turn_off(self):
        with self._session as session:
            r = session.post(idrac_ip + '/data?set=pwState:0', verify=False)
            return r