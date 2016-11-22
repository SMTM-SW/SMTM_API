import traceback

import requests
from flask import abort
from flask import json

from app import app


class RequestAPI:
    _api_server_host = app.config.get('HOST_CRAWLER')

    def __init__(self):
        pass

    @classmethod
    def http_get(cls, endpoint, params=None):
        response = cls.__make_request(method='GET',
                                      endpoint=endpoint,
                                      params=params)
        if response is None:
            return None, -1

        return response.json(), response.status_code

    @classmethod
    def http_post(cls, endpoint, params=None, payload=None):
        response = cls.__make_request(method='POST',
                                      endpoint=endpoint,
                                      params=params,
                                      payload=payload)
        if response is None:
            return None, -1

        return response.json(), response.status_code

    @classmethod
    def http_put(cls, endpoint, params=None, payload=None):
        response = cls.__make_request(method='PUT',
                                      endpoint=endpoint,
                                      params=params,
                                      payload=payload)
        if response is None:
            return None, -1

        return response.json(), response.status_code

    @classmethod
    def http_delete(cls, endpoint, params=None):
        response = cls.__make_request(method='DELETE',
                                      endpoint=endpoint,
                                      params=params,
                                      payload=None)
        if response is None:
            return None, -1

        return response.json(), response.status_code

    @classmethod
    def __build_url(cls, endpoint):
        return "{0}/{1}".format(cls._api_server_host, endpoint)

    @classmethod
    def __make_request(cls, method, endpoint, params=None, payload=None):

        url = cls.__build_url(endpoint)

        response = None
        try:
            payload_data = json.dumps(payload) if payload is not None else None

            if payload_data is None:
                request = requests.Request(method, url, params=params).prepare()
            else:
                request = requests.Request(method, url, params=params, data=payload_data).prepare()
                request.headers['Content-Type'] = 'application/json'

            req_session = requests.Session()
            response = req_session.send(request)

            response.raise_for_status()

            return response

        except requests.ConnectionError as e:
            tb = ''.join(traceback.format_stack())
            app.logger.error('{0}\n{1}'.format(e.args[0], tb[:len(tb) - 1]))
            abort(500)

        except requests.HTTPError as e:
            tb = ''.join(traceback.format_stack())
            app.logger.error('{0}\n{1}'.format(e.args[0], tb[:len(tb) - 1]))

            if response.headers['Content-Type'] == 'application/json':
                response_json = response.json()
                if 'reason' in response_json:
                    reason = response_json['reason']
                    abort(response.status_code, reason)
                else:
                    abort(response.status_code)
            else:
                abort(response.status_code)


class RequestAnalyzeAPI(RequestAPI):
    _analyze_api_endpoint = 'crawler'

    @classmethod
    def analyze_init(cls, body):
        response_data, status_code = RequestAPI.http_post("{0}/".format(cls._analyze_api_endpoint),
                                                          payload=body)
        return response_data
