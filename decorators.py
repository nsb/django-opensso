# -*- coding: utf-8 -*-
from urlparse import urljoin

from django.shortcuts import redirect
from django.utils.http import urlquote
from django.contrib.auth import authenticate, login
from django.conf import settings

from opensso import RestInterface
OPENSSO_COOKIE_NAME = 'iPlanetDirectoryPro'

def opensso_login_required(f, login_url='', redirect_field_name='goto'):

    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(request, *args, **kwargs)
        else:
            ri = RestInterface(opensso_url=login_url)
            cookie_name = ri.getCookieNameForToken()
            if cookie_name in request.COOKIES:
                user = authenticate(tokenid=request.COOKIES[cookie_name])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return f(request, *args, **kwargs)
                    else:
                        # return disabled account page
                        pass
                else:
                    # Return an 'invalid login' error message.
                    pass
        path = urlquote(''.join(('http://', request.get_host(), request.get_full_path())))
        tup = getattr(settings, 'LOGIN_URL_EXTERNAL', ''), redirect_field_name, path
        return redirect('%s?%s=%s' % tup)

    return wrapper
