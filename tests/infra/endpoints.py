import json
import logging
import requests


class FastApiError(Exception):

    def __init__(self, **kwargs):
        self.http_code = kwargs.get('status_code')
        self.reason = kwargs.get('reason')
        self.message = kwargs.get('text')

    def __str__(self) -> str:
        return f'{self.message}'


def validate_response(r: requests.Response):
    if r.status_code >= 400:

        logging.debug(f'{r.request.method} {r.url} failed with code {r.status_code}: {r.reason}')
        raise FastApiError(status_code=r.status_code, reason=r.reason, text=r.text)


class Base:

    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000'


class ApiSingle(Base):

    def retrieve(self, uid: int) -> dict:
        url = f'{self.base_url}{self.endpoint}/{uid}'
        response = requests.get(url)
        validate_response(response)
        return response.json()

    def create(self, payload: dict) -> dict:
        url = f'{self.base_url}{self.endpoint}'
        response = requests.post(url, data=json.dumps(payload))
        validate_response(response)
        return response.json()

    def update(self, uid: int, payload: dict) -> dict:
        url = f'{self.base_url}{self.endpoint}/{uid}'
        response = requests.put(url, data=json.dumps(payload))
        validate_response(response)
        return response.json()

    def delete(self, uid: int):
        url = f'{self.base_url}{self.endpoint}/{uid}'
        response = requests.delete(url)
        validate_response(response)
        return response


class ApiListing(Base):

    def retrieve(self, **request_params) -> list[dict]:
        url = f'{self.base_url}{self.endpoint}'
        response = requests.get(url, params=request_params)
        validate_response(response)
        return response.json()


class Post(ApiSingle):

    @property
    def endpoint(self):
        return '/posts'


class Posts(ApiListing):

    @property
    def endpoint(self):
        return '/posts'
