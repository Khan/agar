import webtest
from unittest2 import TestCase

class WebTest(TestCase):
    """
    A base class for testing web requests. Provides a wrapper around
    the webtest package that is compatable with gaetestbed's.

    To use, inherit from the WebTest class and define a class-level
    variable called APPLICATION that is set to the WSGI application
    under test.
    """

    @property
    def app(self):
        if not getattr(self, '_web_test_app', None):
            self._web_test_app = webtest.TestApp(self.APPLICATION)

        return self._web_test_app
            
    def get(self, url, params=None, headers=None, extra_environ=None):
        return self.app.get(url, params=params, headers=headers, status="*", expect_errors=True)

    def assertOK(self, response):
        self.assertEqual(200, response.status_int)

    
