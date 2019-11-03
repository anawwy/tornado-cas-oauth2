Tornado-cas-oauth2
=====================

Tornado-cas-oauth2  is a Python2 `tornado<https://github.com/tornadoweb/tornado>`_`cas<https://github.com/go-cas/cas>`_ oauth2 client

Settings
--------

You must setting CA_CERT_PATH and _base_url to the ``CASHelper``, in cas.py::

  class CASHelper(AAsyncHTTPClient):
      CA_CERT_PATH = 'XXXXX'

      @classmethod
      def _base_url(cls):
          '''cas server url prefix'''
          return 'https://cas.test.change.it:8443'
          
Demo
--------
see demo.py
