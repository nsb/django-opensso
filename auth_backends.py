# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.conf import settings

from restclient import GET
from opensso import RestInterface

class OpenSSOBackend:
    """
    Authenticate against OpenSSO.

    """

    def __init__(self, ):
        self.opensso = RestInterface(opensso_url=getattr(settings, 'LOGIN_URL', ''))

    def authenticate(self, tokenid=None):

        is_authenticated = self.opensso.isTokenValid(tokenid)

        if is_authenticated:
            username = self.opensso.attributes(attributes_names=getattr(settings, 'OPENSSO_USER_ID_NAME', 'uid'), subjectid=tokenid)
            return User.objects.get(username=username)

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
