# import threading
# threading._DummyThread._Thread__stop = lambda x: 42
import json


class customtype(type):  ## Определить новый метакласс
    def __init__(cls, cls_name, bases, attrs):
        temp_list = []
        if isinstance(attrs, dict):
            for k, v in attrs.items():
                if isinstance(v, dict):
                    attrs[k] = customtype('', (customtype, ), v)()
                    break
                elif isinstance(v, list):
                    for attr in v:
                        if isinstance(attr, dict):
                            for k, v in attr.items():
                                if isinstance(v, dict):
                                    attrs[k] = customtype('', (), v)()
                                    break
                                else:
                                    temp_list.append(attr[k])
                                    attrs[k] = temp_list
                        else:
                            temp_list.append(attr)
                            attrs[k] = temp_list


# class Base(dict):
#     def __init__(self, attrs):
#         if isinstance(attrs, dict):
#             for key, value in attrs.items():
#                 if isinstance(value, dict):
#                     setattr(self, key, Base(value))
#                 else:
#                     setattr(self, key, value)


class Base(dict):
    def __init__(self, attrs):
        temp = []
        if isinstance(attrs, dict):
            for key, value in attrs.items():
                if isinstance(value, dict):
                    setattr(self, key, Base(value))
                if isinstance(value, list):
                    for val in value:
                        if isinstance(val, dict):
                            for key, value in attrs.items():
                                setattr(self, key, type('', (dict, ), {attrs[key]}))
                        else:
                            setattr(self, key, value)
                else:
                    setattr(self, key, value)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Base, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Base, self).__delitem__(key)
        del self.__dict__[key]

    def __repr__(self):
        return json.dumps(self)

    def type_coerce_attrs(self):
        pass

# class SimpleBase:
#     def __init__(self, attrs):
#         if attrs:
#             setattr(self, key, SimpleBase(attrs))


if __name__ == '__main__':
    # w = {"Person": {"name": "Tom", "age": 20, "childrens": [{"name": "Vasya"}, {"name": "Sergey"}]}}
    w = {"person": {"name": "Tom", "age": 20}, "padla": "dasyka", "dictkey": [{"inner_dict": "prikol"}]}
    d = [{"name": "Anton", "age": 20}, {"name": "Sergey", "age": 32}]
    # d = {"name": "Anton", "age": 20}
    # print(w)
    # MyShinyClass = type('', (), w)()
    # MyShinyClass.__setattr__({"name": "lala"})
    # print(MyShinyClass.name)
    s = Base(w)
    print(s.dictkey)
