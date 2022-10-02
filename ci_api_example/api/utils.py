import enum

APPLICATION_JSON = 'application/json'


def non_null(obj, defValue):
    return obj if obj is not None else defValue


def type_coerce(obj, objType):
    if isinstance(obj, objType):
        ret = obj
    elif isinstance(obj, dict):
        ret = objType(obj)

        ret.type_coerce_attrs()
    else:
        ret = None

    return ret


def type_coerce_list(obj, objType):
    if isinstance(obj, list):
        ret = []
        for entry in obj:
            ret.append(type_coerce(entry, objType))
    else:
        ret = None

    return ret


def type_coerce_dict(obj, objType):
    if isinstance(obj, dict):
        ret = {}
        for k, v in obj.items():
            ret[k] = type_coerce(v, objType)
    else:
        ret = None

    return ret


def type_coerce_dict_list(obj, objType):
    if isinstance(obj, dict):
        ret = {}
        for k, v in obj.items():
            ret[k] = type_coerce_list(v, objType)
    else:
        ret = None

    return ret


class API:
    def __init__(self, path, method, expected_status, consumes=APPLICATION_JSON, produces=APPLICATION_JSON):
        self.path = path
        self.method = method
        self.expected_status = expected_status
        self.consumes = consumes
        self.produces = produces

    def format_path(self, params):
        return API(self.path.format(**params), self.method, self.expected_status, self.consumes, self.produces)


class HttpMethod(enum.Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"


class HTTPStatus:
    OK = 200
    NO_CONTENT = 204
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503
