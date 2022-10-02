import json
import logging
import os
from requests import Session, Response
from api.exceptions import HttpClientException
from api.utils import HttpMethod, HTTPStatus

logger = logging.getLogger(__name__)

class HttpClient:
    def __init__(self, url, auth):
        self.url = url
        self.session = Session()
        self.session.auth = auth

    def call_api(self, api, query_params=None, request_data=None):
        ret = None
        params = {'headers': {'Accept': api.consumes, 'Content-type': api.produces}}

        if query_params:
            params['params'] = query_params

        if request_data:
            params['data'] = json.dumps(request_data)

        path = os.path.join(self.url, api.path)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("------------------------------------------------------")
            logger.debug("Call         : %s %s", api.method, path)
            logger.debug("Content-type : %s", api.consumes)
            logger.debug("Accept       : %s", api.produces)

        response = None

        if api.method == HttpMethod.GET:
            response = self.session.get(path, **params)
        elif api.method == HttpMethod.POST:
            response = self.session.post(path, **params)
        elif api.method == HttpMethod.PUT:
            response = self.session.put(path, **params)
        elif api.method == HttpMethod.DELETE:
            response = self.session.delete(path, **params)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("HTTP Status: %s", response.status_code if response else "None")

        if response is None:
            ret = None
        elif response.status_code == api.expected_status:
            try:
                if response.status_code == HTTPStatus.NO_CONTENT or response.content is None:
                    ret = None
                else:
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug("<== __call_api(%s, %s, %s), result=%s", vars(api), params, request_data, response)

                        logger.debug(response.json())

                    ret = response.json()
            except Exception as e:
                print(e)

                logger.exception("Exception occurred while parsing response with msg: %s", e)

                raise HttpClientException(api, response)
        elif response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
            logger.error("Service unavailable. HTTP Status: %s", HTTPStatus.SERVICE_UNAVAILABLE)

            ret = None
        elif response.status_code == HTTPStatus.NOT_FOUND:
            logger.error("Not found. HTTP Status: %s", HTTPStatus.NOT_FOUND)

            ret = None
        else:
            raise HttpClientException(api, response)

        return ret
