from google.appengine.ext import deferred
from agar.test import BaseTest

import main

def do_something():
    return True

class TestWebTest(BaseTest):

    def test_assert_tasks_in_queue(self):
        self.assertTasksInQueue(0)
        
        deferred.defer(do_something, _name="hello_world")

        self.assertTasksInQueue(1)
        self.assertTasksInQueue(1, name='hello_world')
        self.assertTasksInQueue(0, name='something else')
        self.assertTasksInQueue(0, url='/foobar')
        self.assertTasksInQueue(1, url='/_ah/queue/deferred')
        self.assertTasksInQueue(1, queue_names='default')
        self.assertTasksInQueue(0, queue_names='other')
