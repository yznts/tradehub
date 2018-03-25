import collections


# Working with nested data

def merge(d, u):
    if not d:
        return u
    if not u:
        return d
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = merge(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def get(_dict, keys, default=None):
    for key in keys:
        if isinstance(_dict, dict):
            _dict = _dict.get(key, default)
        else:
            return default
    return _dict