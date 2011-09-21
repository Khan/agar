import unittest2
from google.appengine.ext import testbed

class BaseTest(unittest2.TestCase):
    """
    A base class for App Engine unit tests that sets up API proxy
    stubs for all available services, using testbed.

    Note: the images stub is only set up if PIL is found.

    To use, simply inherit from this class:

        import agar
        
        class MyTestCase(agar.test.BaseTest):
            
            def test_datastore(self):
                model = MyModel(foo='foo')
                model.put()

                # will always be true because the datastore is cleared
                # between test method runs.
                self.assertEqual(1, MyModel.all().count())
    """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_user_stub()
        self.testbed.init_xmpp_stub()

        try:
            from google.appengine.api.images import images_stub
            self.testbed.init_images_stub()
        except ImportError:
            pass
    
