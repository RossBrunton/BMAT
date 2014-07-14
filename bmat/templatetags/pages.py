from django import template

register = template.Library()

@register.inclusion_tag('pages.html')
def pages(url="", count=0, start=0, end=0, dchar="r", division=10, **kwargs):
    p = []
    
    kwargs["url"] = url
    kwargs["dchar"] = dchar
    
    cpage = end / division
    mpage = count / division
    kwargs["cpage"] = cpage
    
    # Old code, maybe make it better?
    '''# Always display first three pages
    if count > division * 0:
        p.append({"no":1, "start":division*0, "end":division*1})
    
    if count > division * 1:
        p.append({"no":2, "start":division*1, "end":division*2})
    
    if count > division * 2:
        p.append({"no":3, "start":division*2, "end":division*3})
    
    # Display page 4 and 5 with no ".." if the current page is < 7
    if cpage <= 7:
        if count > division * 3 and cpage >= 2:
            p.append({"no":4, "start":division*3, "end":division*4})
        
        if count > division * 4 and cpage >= 3:
            p.append({"no":5, "start":division*4, "end":division*5})
        
        if count > division * 5 and cpage >= 4:
            p.append({"no":6, "start":division*5, "end":division*6})
    else:
        # Otherwise display a ".." and two below the current page
        p.append({"no":"..", "start":0, "end":0})
        
        if count > division * (cpage-3):
            p.append({"no":cpage-2, "start":division*(cpage-3), "end":division*(cpage-2)})
        
        if count > division * (cpage-2):
            p.append({"no":cpage-1, "start":division*(cpage-2), "end":division*(cpage-1)})
        
    if cpage > 7 and count > division * (cpage-1):
        p.append({"no":cpage, "start":division*(cpage-1), "end":division*(cpage-0)})
    
    if cpage <= mpage - 3 and mpage > 6:
        p.append({"no":"..", "start":0, "end":0})
        
        p.append({"no":mpage-2, "start":division*(mpage-3), "end":division*(mpage-2)})
        
        p.append({"no":mpage-1, "start":division*(mpage-2), "end":division*(mpage-1)})
        
        p.append({"no":mpage, "start":division*(mpage-1), "end":division*(mpage-0)})'''
    
    for i in range(1, mpage+1):
        p.append({"no":i, "start":division*(i-1), "end":division*i})
    
    kwargs["pages"] = p
    
    return kwargs
