import requests


class ApiClass:
    def __init__(self, BASE_URL, HEADERS):
        self.BASE_URL= BASE_URL
        self.HEADERS = HEADERS

    def send_requests(self, url, params):
        response = requests.get(
            f'{self.BASE_URL}{url}',
            params=params,
            headers=self.HEADERS

        )

        return response
