""" Contains general misc functions
"""

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def make_page(query, param, per_page=30):
    """ Makes a new paginator as appropriate
    
    The param is the page number to load (defaults to 0 or the max if not in range) and returns a paginator for the
    given query at the given page.
    """
    paginator = Paginator(query, per_page)
    try:
        page = paginator.page(param)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return page
