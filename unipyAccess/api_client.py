import requests
from .users import UserManager
from .hardware import HardwareManager
from .utils import configure_logging

configure_logging()

class UnipyAccess:
    def __init__(self, base_url, username, password, verify=True):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.verify = False
        self.session = requests.Session()
        self.csrf_token = None
        self._login()

        # Initialize managers
        self.users = UserManager(self)
        self.hardware = HardwareManager(self)

    def _login(self):
        if not self.verify:
            requests.packages.urllib3.disable_warnings(
                requests.packages.urllib3.exceptions.InsecureRequestWarning
            )

        login_url = f"{self.base_url}/api/auth/login"
        login_payload = {
            "username": self.username,
            "password": self.password,
            "token": "",
            "rememberMe": False,
        }
        login_headers = {
            'Content-Type': 'application/json',
            'Origin': self.base_url,
        }

        response = self.session.post(
            login_url,
            headers=login_headers,
            json=login_payload,
            verify=self.verify,
        )

        if response.status_code != 200:
            raise AuthenticationError(f"Login failed: {response.text}")

        self.csrf_token = response.headers.get('x-csrf-token')
        if not self.csrf_token:
            raise AuthenticationError("x-csrf-token not found in login response")

        # Update session headers
        self.session.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': self.base_url,
            'x-csrf-token': self.csrf_token,
        })

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, verify=self.verify, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get(self, endpoint):
        return self.request('GET', endpoint)
    
    def post(self, endpoint, payload):
        return self.request('POST', endpoint, json=payload)
    
    def put(self, endpoint, data=None):
        return self.request('PUT', endpoint, json=data)
    
    def delete(self, endpoint):
        return self.request('DELETE', endpoint)