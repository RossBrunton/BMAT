from django.template import defaultfilters

_taggable = {}

def lookup_taggable(name):
    return _taggable.get(name, None)


def taggable(name):
    def decorator(c):
        if not hasattr(c, "tags"):
            raise RuntimeError("Class {} does not have a tags property, but is taggable".format(c))
        
        _taggable[name] = c
        
        return c
    return decorator
