from django.core.exceptions import SuspiciousOperation

def parse_split(get, key, defstart=0, defend=10):
    if key in get:
        try:
            start, end = get[key].split(":")
            start = int(start)
            end = int(end)
        except:
            raise SuspiciousOperation
    else:
        start = defstart
        end = defend
    
    if start < 0 or end < 0 or end < start: raise SuspiciousOperation
    
    if end > start + 200:
        end = start + 200
    
    return start, end
