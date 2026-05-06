import requests

BASE_URL = "https://petstore.swagger.io/v2"
DEFAULT_TIMEOUT = 10


class PetstoreClient:
    def __init__(self, base_url: str = BASE_URL, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(self._url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str, json=None, **kwargs) -> requests.Response:
        return self.session.post(
            self._url(path), json=json, timeout=self.timeout, **kwargs
        )

    def put(self, path: str, json=None, **kwargs) -> requests.Response:
        return self.session.put(
            self._url(path), json=json, timeout=self.timeout, **kwargs
        )

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.session.delete(self._url(path), timeout=self.timeout, **kwargs)
