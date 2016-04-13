import config_default
configs = config_default.configs

def merge(dict1, dict2):
    for k,v in dict2.items():
        if not k in dict1 or not isinstance(v,dict):
            dict1[k] = v
        else:
            dict1[k] = merge(dict1[k],v)
    return dict1

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass
