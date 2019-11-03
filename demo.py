#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

import tornado.ioloop
import tornado.web
from tornado import gen

from cas import CASHelper
from http_client import get_url


class LoginHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        code = self.get_argument('code')
        retry = int(self.get_argument('retry'))
        user_redirect_url = self.get_argument('redirect')
        if retry == 0:
            raise RuntimeError('max retry')
        base_url = '{protocol}://{host}'.format(protocol=self.request.protocol, host=self.request.host)
        login_redirect_url = get_url(base_url, '/login')
        result = yield CASHelper.async_access_token(login_redirect_url, code)
        access_token, expires = CASHelper.unpack_access_token(result)
        if access_token:
            logging.info('access_token:%s,expires:%s' % (access_token, expires))
            result = yield CASHelper.async_profile(access_token)
            profile_id = CASHelper.unpack_profile(result)
            if profile_id:
                raise gen.Return(self.redirect(user_redirect_url + "?user=" + profile_id))

        login_redirect_url = get_url(base_url, '/login', {'redirect': user_redirect_url, 'retry': retry - 1})
        raise gen.Return(self.redirect(CASHelper.get_login_url(login_redirect_url)))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_argument('user', None)
        if not user:
            base_url = '{protocol}://{host}'.format(protocol=self.request.protocol, host=self.request.host)
            hello_redirect_url = get_url(base_url, '/hello')
            login_redirect_url = get_url(base_url, '/login', data={'retry': 10, 'redirect': hello_redirect_url})
            cas_redirect_url = CASHelper.get_login_url(login_redirect_url, renew=True)
            return self.redirect(cas_redirect_url)
        self.write("Hello, " + user)


def make_app():
    return tornado.web.Application([
        (r"/hello", MainHandler),
        (r"/login", LoginHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
