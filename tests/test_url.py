from webtest import Request
from agar.url import uri_for
from agar.test import BaseTest

from api import application


class UriTest(BaseTest):
    def setUp(self):
        application.set_globals(application, Request.blank("/"))
        self.method = uri_for
        super(UriTest, self).setUp()

    def test_get_uri(self):
        uri = self.method('api-v1')
        self.assertEqual(uri, '/api/v1/model1')

    def test_get_invalid_uri_name(self):
        invalid_uri_name = 'invalid-uri-name'
        try:
            uri = uri_for(invalid_uri_name)
            self.fail("Got uri '%s' for invalid uri name '%s'" % (uri, invalid_uri_name))
        except Exception, e:
            self.assertEqual(e.message, "Route named '%s' is not defined." % invalid_uri_name)
