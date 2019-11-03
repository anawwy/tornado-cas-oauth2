#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from abc import abstractmethod, ABCMeta
from urllib import urlencode

from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


def get_url(base, uri, data=None):
    if data is not None:
        uri = uri + '?' + urlencode(data)
    return '{base}{uri}'.format(base=base, uri=uri)


class AAsyncHTTPClient(object):
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def _base_url(cls):
        return ''

    @classmethod
    @gen.coroutine
    def async_get(cls, uri, **option):
        client = AsyncHTTPClient()
        headers = option.get('headers', None)
        data = option.get('data')

        url = get_url(cls._base_url(), uri, data)
        request = HTTPRequest(url=url, headers=headers,
                              ca_certs=option.get('ca_certs'),
                              method='GET', follow_redirects=option.get('follow_redirects', False),
                              request_timeout=option.get('request_timeout', 60))
        response = yield client.fetch(request, raise_error=False)

        if response.code != 200:
            logging.error(
                'get method error,code=%s,url=%s,headers=%s,response.error=%s,response.body=%s' % (
                    response.code, url, headers, response.error, response.body))
        raise gen.Return(response.body)
