#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from tornado import gen

from http_client import AAsyncHTTPClient, get_url


class CASHelper(AAsyncHTTPClient):
    CA_CERT_PATH = 'XXXXX'

    @classmethod
    def _base_url(cls):
        '''cas server url prefix'''
        return 'https://cas.test.change.it:8443'

    @classmethod
    def get_login_url(cls, redirect_uri, **kwargs):
        kwargs['redirect_uri'] = redirect_uri
        return get_url(cls._base_url(), '/oauth2/authorize', data=kwargs)

    @classmethod
    def get_logout_url(cls, ):
        return get_url(cls._base_url(), '/logout')

    @classmethod
    @gen.coroutine
    def async_access_token(cls, redirect_uri, code):
        result = yield cls.async_get('/oauth2/accessToken',
                                     ca_certs=cls.CA_CERT_PATH,
                                     data={'code': code, 'redirect_uri': redirect_uri})
        raise gen.Return(result)

    @classmethod
    def unpack_access_token(cls, result):
        access_token, expires = None, None
        if result:
            result_array = result.split('&')
            if len(result_array) == 2:
                access_token_array = result_array[0].split('=')
                expires_array = result_array[1].split('=')
                if len(access_token_array) == 2 and access_token_array[0] == 'access_token' \
                        and len(expires_array) == 2 and expires_array[0] == 'expires':
                    access_token = access_token_array[1]
                    expires = float(expires_array[1])
        return access_token, expires

    @classmethod
    @gen.coroutine
    def async_profile(cls, access_token):
        result = yield cls.async_get('/oauth2/profile',
                                     ca_certs=cls.CA_CERT_PATH,
                                     data={'access_token': access_token})
        raise gen.Return(result)

    @classmethod
    def unpack_profile(cls, profile):
        result = json.loads(profile)
        profile_id = result.get('id')
        return profile_id
