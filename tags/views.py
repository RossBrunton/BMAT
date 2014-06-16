from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_POST
from django.contrib.auth import logout as alogout, login as alogin, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.template.response import TemplateResponse
from django.template import defaultfilters
from django.views.decorators.cache import cache_page

from collections import OrderedDict


