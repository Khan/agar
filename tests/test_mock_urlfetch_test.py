from google.appengine.api import urlfetch
from agar.test import MockUrlfetchTest

class MockHTTPRequestTest(MockUrlfetchTest):

    def test_get_google(self):
        self.set_response("http://google.com/foobar", "foobar", 404)
        
        result = urlfetch.fetch("http://google.com/foobar")

        self.assertEqual(404, result.status_code)
        self.assertEqual("foobar", result.content)

    def test_get_unregistered_url(self):
        self.assertRaises(Exception,  urlfetch.fetch, "http://google.com/foobar")
