import logging

from api.http_client import HttpClient
from api.ranger.model import RangerService
from api.utils import type_coerce, API, HttpMethod, HTTPStatus

logger = logging.getLogger(__name__)


class RangerClient:


    URI_BASE = "service/public/v2/api"

    URI_SERVICEDEF = URI_BASE + "/servicedef"
    URI_SERVICEDEF_BY_ID = URI_SERVICEDEF + "/{id}"
    URI_SERVICEDEF_BY_NAME = URI_SERVICEDEF + "/name/{name}"

    URI_SERVICE = URI_BASE + "/service"
    URI_SERVICE_BY_ID = URI_SERVICE + "/{id}"
    URI_SERVICE_BY_NAME = URI_SERVICE + "/name/{name}"
    URI_POLICIES_IN_SERVICE = URI_SERVICE + "/{serviceName}/policy"

    CREATE_SERVICEDEF = API(URI_SERVICEDEF, HttpMethod.POST, HTTPStatus.OK)
    UPDATE_SERVICEDEF_BY_ID = API(URI_SERVICEDEF_BY_ID, HttpMethod.PUT, HTTPStatus.OK)
    UPDATE_SERVICEDEF_BY_NAME = API(URI_SERVICEDEF_BY_NAME, HttpMethod.PUT, HTTPStatus.OK)
    DELETE_SERVICEDEF_BY_ID = API(URI_SERVICEDEF_BY_ID, HttpMethod.DELETE, HTTPStatus.NO_CONTENT)
    DELETE_SERVICEDEF_BY_NAME = API(URI_SERVICEDEF_BY_NAME, HttpMethod.DELETE, HTTPStatus.NO_CONTENT)
    GET_SERVICEDEF_BY_ID = API(URI_SERVICEDEF_BY_ID, HttpMethod.GET, HTTPStatus.OK)
    GET_SERVICEDEF_BY_NAME = API(URI_SERVICEDEF_BY_NAME, HttpMethod.GET, HTTPStatus.OK)
    FIND_SERVICEDEFS = API(URI_SERVICEDEF, HttpMethod.GET, HTTPStatus.OK)


    def __init__(self, url, auth):
        self.client_http = HttpClient(url, auth)

    logging.getLogger("requests").setLevel(logging.WARNING)

    def get_service(self, servicename):
        resp = self.client_http.call_api(RangerClient.GET_SERVICE_BY_NAME.format_path({'name': servicename}))

        return type_coerce(resp, RangerService)


    def test_method(self, testname):
        resp = self.client_http.call_api(RangerClient.GET_SERVICE_BY_NAME.format_path({'name': testname}))

        return type_coerce(resp, RangerService)

