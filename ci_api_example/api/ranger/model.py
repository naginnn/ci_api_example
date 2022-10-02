import json

from api.utils import non_null


class RangerBase(dict):
    def __init__(self, attrs):
        pass

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(RangerBase, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(RangerBase, self).__delitem__(key)
        del self.__dict__[key]

    def __repr__(self):
        return json.dumps(self)

    def type_coerce_attrs(self):
        pass


class RangerBaseModelObject(RangerBase):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}

        RangerBase.__init__(self, attrs)

        self.id = attrs.get('id')
        self.guid = attrs.get('guid')
        self.type = attrs.get('type')

    def type_coerce_attrs(self):
        super(RangerBaseModelObject, self).type_coerce_attrs()

        self.type = type_coerce_list_dict(self.type, RangerService)


class RangerService(RangerBaseModelObject):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}

        # RangerBaseModelObject.__init__(self, attrs)

        self.name = attrs.get('name')
        # self.tagService = attrs.get('tagService')
        # self.configs = attrs.get('configs')
        # self.policyVersion = attrs.get('policyVersion')
        # self.policyUpdateTime = attrs.get('policyUpdateTime')
        # self.tagVersion = attrs.get('tagVersion')
        # self.tagUpdateTime = attrs.get('tagUpdateTime')


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


def type_coerce_list_dict(obj, objType):
    if isinstance(obj, list):
        ret = objType(obj[0])
    else:
        ret = None

    return ret


if __name__ == '__main__':
    obj = {'id': 1, 'guid': "hello", 'type': [{'name': [1, 2, 3, 4]}]}
    ret = type_coerce(obj, RangerBaseModelObject)
    print(ret.type.name)
