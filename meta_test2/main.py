import json

class Base(dict):
    def __init__(self, attrs):
        pass
                    # vsegda peredau key:value krome str
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

def type_coerce(obj, objType):
    if isinstance(obj, objType):
        ret = BaseChild(obj)
    else:
        ret = obj
    return ret

def type_coerce_list(obj, objType):
    if isinstance(obj, list):
        ret = []
        for entry in obj:
            ret.append(type_coerce(entry, dict))
    else:
        ret = None
    return ret
class BaseChild(Base):
    def __init__(self, attrs):
        if attrs is None:
            attrs = {}

        Base.__init__(self, attrs)

        if isinstance(attrs, dict):
            for key, value in attrs.items():
                key.replace('.', '_')
                if isinstance(value, str):
                    setattr(self, key, value)
                elif isinstance(value, dict):
                    setattr(self, key, BaseChild(value))
                elif isinstance(value, list):
                    setattr(self, key, type_coerce_list(value, BaseChild))


if __name__ == '__main__':
    attrs = { "items" : [
                {
                  "href" : "http://localhost:8080/api/v1/clusters/cc/configurations/service_config_versions?service_name=HDFS&service_config_version=2",
                  "configurations" : [
                    {
                      "config" : {
                        "cluster_name" : "HDP",
                        "stack_id" : "HDP-2.2"
                      },
                      "type" : "core-site",
                      "tag" : "version2",
                      "version" : 2,
                      "properties" : {
                            "security.inter.datanode.protocol.acl" : "*",
                            "security.refresh.usertogroups.mappings.protocol.acl" : "hadoop",
                            "security.client.datanode.protocol.acl" : "*",
                            "security.admin.operations.protocol.acl" : "hadoop",
                            "security.inter.tracker.protocol.acl" : "*",
                            "security.datanode.protocol.acl" : "*",
                            "security.job.client.protocol.acl" : "*",
                            "security.client.protocol.acl" : "*",
                            "security.job.task.protocol.acl" : "*",
                            "security.refresh.policy.protocol.acl" : "hadoop",
                            "security.namenode.protocol.acl" : "*"
                      },
                      "properties_attributes" : { }
                    }
                  ]
                }
            ]
        }
    l = {"person": {"name": "Tom", "age": 20}, "padla": "dasyka", "dictkey": [1, 2, 3, 4, 5]}
    d = {"person": {"name": "Tom", "age": 20}, "padla": "dasyka", "dictkey": [{"krasava": "lala"}]}

    l = BaseChild(l)
    d = BaseChild(d)
    winner = BaseChild(attrs)
    # s = Base(attrs['items'][0]["configurations"][0])
    print(winner.items[0].configurations[0].config.cluster_name)
    # print(l.dictkey)
    # print(d.dictkey[0].krasava)
