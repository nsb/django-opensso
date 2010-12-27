# -*- coding: utf-8 -*-

from restclient import GET, POST
from django.conf import settings

#REST API
REST_OPENSSO_LOGIN = '/UI/Login'
REST_OPENSSO_LOGOUT = '/identity/logout'
REST_OPENSSO_COOKIE_NAME_FOR_TOKEN = '/identity/getCookieNameForToken'
REST_OPENSSO_COOKIE_NAMES_TO_FORWARD = '/identity/getCookieNamesToForward'
REST_OPENSSO_IS_TOKEN_VALID = '/identity/isTokenValid'
REST_OPENSSO_ATTRIBUTES = '/identity/attributes'


class RestInterface:
    """
    OpenSSO Rest Interface
    http://blogs.sun.com/docteger/entry/opensso_and_rest
    """

    def __init__(self, opensso_url='',):
        """
        @param opensso_url: the url to the opensso server
        """
        if not opensso_url:
            raise AttributeError('This interface needs an OpenSSO url to work!')

        self.opensso_url = opensso_url

    def logout(self, subjectid):
        data = GET(
            ''.join((self.opensso_url, REST_OPENSSO_LOGOUT)), params = {'subjectid':subjectid},
        )

    def isTokenValid(self, tokenid):
        data = GET(
            ''.join((self.opensso_url, REST_OPENSSO_IS_TOKEN_VALID)), params = {'tokenid':tokenid},
        )
        return data == 'boolean=true\n'

    def attributes(self, attributes_names='uid', subjectid=''):
        data = GET(
            ''.join((self.opensso_url, REST_OPENSSO_ATTRIBUTES)),
            params = {'attributes_names':attributes_names, 'subjectid':subjectid},
        )

        attribute_value = ''
        lines = data.splitlines()
        for i, line in enumerate(lines):
            if line == 'userdetails.attribute.name=%s' % attributes_names:
                attribute_value = lines[i + 1].split('=')[1]
                break

        return attribute_value.strip()

    def getCookieNameForToken(self,):

        data = GET(''.join((self.opensso_url, REST_OPENSSO_COOKIE_NAME_FOR_TOKEN)))
        return data.split('=')[1].strip()
