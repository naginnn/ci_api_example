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
        return json.dumps(attrs)

    def type_coerce_attrs(self):
        pass

def type_coerce_dict(obj):
    if isinstance(obj, dict):
        ret = BaseChild(obj)
    else:
        ret = obj
    return ret

def type_coerce_list(obj):
    if isinstance(obj, list):
        ret = []
        for entry in obj:
            ret.append(type_coerce_dict(entry))
    else:
        ret = None
    return ret

def type_coerce(obj, attrs):
    if isinstance(attrs, dict):
        for key, value in attrs.items():
            if isinstance(value, str):
                setattr(obj, key.replace('.', '_'), value)
            elif isinstance(value, dict):
                setattr(obj, key.replace('.', '_'), BaseChild(value))
            elif isinstance(value, list):
                setattr(obj, key.replace('.', '_'), type_coerce_list(value))
class BaseChild(Base):
    def __init__(self, attrs):
        if attrs is None:
            attrs = {}

        Base.__init__(self, attrs)

        type_coerce(self, attrs)


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
                            "security.inter" : "*",
                            "security.refresh" : "hadoop",
                            "security.client" : "*",
                            "security.admin" : "hadoop",
                      },
                      "properties_attributes" : { }
                    }
                  ]
                }
            ]
        }

    attrs2 = {
                  "href" : "http://localhost:8080/api/v1/clusters/cc/configurations/service_config_versions",
                  "items" : [
    {
      "href" : "http://localhost:8080/api/v1/clusters/cc/configurations/service_config_versions?service_name=YARN&service_config_version=1",
      "cluster_name" : "cc",
      "configurations" : ["lOH"],
      "createtime" : 1430922080177,
      "group_id" : -1,
      "group_name" : "default",
      "hosts" : [ ],
      "is_cluster_compatible" : True,
      "is_current" : True,
      "service_config_version" : 1,
      "service_config_version_note" : "Initial configurations for YARN",
      "service_name" : "YARN",
      "stack_id" : "HDP-2.2",
      "user" : "admin"
    },
    {
      "href" : "http://localhost:8080/api/v1/clusters/cc/configurations/service_config_versions?service_name=ZOOKEEPER&service_config_version=1",
      "cluster_name" : "cc",
      "configurations" : [1, 2, 3, 4, 5],
      "createtime" : 1430922080347,
      "group_id" : -1,
      "group_name" : "default",
      "hosts" : [ ],
      "is_cluster_compatible" : True,
      "is_current" : True,
      "service_config_version" : 1,
      "service_config_version_note" : "Initial configurations for ZooKeeper",
      "service_name" : "ZOOKEEPER",
      "stack_id" : "HDP-2.2",
      "user" : "admin"
    }
  ]
}
    # l = {"person": {"name": "Tom", "age": 20}, "padla": "dasyka", "dictkey": [1, 2, 3, 4, 5]}
    d = [{"person": {"name": "Tom", "age": 20}, "padla": "dasyka", "dictkey": [{"krasava": "lala"}]}]
    #
    # l = BaseChild(l)
    d = BaseChild(d)
    # winner = BaseChild(attrs2)
    # s = Base(attrs['items'][0]["configurations"][0])
    # print(dir(winner))
    print(d.person.name)
    # пофиксить если первый элемент []
    # print(l.dictkey)
    # print(d.dictkey[0].krasava)
