from google.appengine.api import apiproxy_stub_map

from base_test import BaseTest


class DataStoreTest(BaseTest):
    """
    The :py:class:`DataStoreTest` is a base test case that provides helper
    methods for dealing with `Model`_'s.
    
    The main thing that this mixin does is ensure that the local Data Store
    is empty at the start of each test. This way you never have to worry about
    cleaning up after previous ran tests. This becomes especially important
    when you're unsure of the order in which the tests will run.
    
    For example::
    
        from agar.test import DataStoreTest
        
        class MyTestCase(DataStoreTest):
            def test_empty(self):
                self.assertLength(models.MyModel.all(), 0)
                models.MyModel(field="value").put()
                self.assertLength(models.MyModel.all(), 1)
            
            def test_still_empty(self):
                self.assertLength(models.MyModel.all(), 0)
                models.MyModel(field="value").put()
                self.assertLength(models.MyModel.all(), 1)
    
    If the Data Store wasn't emptied out between tests, one of these two 
    would fail. When you inherit from the :py:class:`DataStoreTest`, each test
    is run inside its own little sandbox.
    
    Keep in mind that this test case uses the :py:meth:`~agar.test.DataStoreTest.setUp` method to ensure
    the Data Store is empty between tests. So if you override that in your test case, make sure to call ``super()``::

        from agar.test import DataStoreTest
        
        class MyTestCase(DataStoreTest):
            def setUp(self):
                # Note that you're calling super on MyTestCase, not on DataStoreTest
                super(MyTestCase, self).setUp()
                # Do anything else you want here
            
            def test_sample(self):
                self.assertLength(models.MyModel.all(), 0)
                models.MyModel(field="value").put()
                self.assertLength(models.MyModel.all(), 1)
    """
    def setUp(self):
        """
        This method is called at the start of each test case.
        
        As noted above, if your test case needs to call :py:meth:`~agar.test.DataStoreTest.setUp`, make
        sure to call ``super()``. Otherwise the Data Store might not be set up correctly.
        """
        super(DataStoreTest, self).setUp()
        self.clear_datastore()
    
    def _get_datastore_stub(self):
        return apiproxy_stub_map.apiproxy._APIProxyStubMap__stub_map['datastore_v3']
        
    def clear_datastore(self):
        """
        Clear the Data Store of all its data.
        
        This method can be used inside your tests to clear the Data Store mid-test.
        
        For example::
        
            import unittest
            
            from agar.test import DataStoreTest
            
            class MyTestCase(DataStoreTest):
                def test_clear_datastore(self):
                    # Add something to the Data Store
                    models.MyModel(field="value").put()
                    self.assertLength(models.MyModel.all(), 1)
                    
                    # And then empty the Data Store
                    self.clear_datastore()
                    self.assertLength(models.MyModel.all(), 0)
        """
        self._get_datastore_stub().Clear()
