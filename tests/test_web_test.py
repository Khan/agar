from agar.test import BaseTest, WebTest

import main 

class TestWebTest(BaseTest, WebTest):

    APPLICATION = main.application

    def test_get(self):
        response = self.get("/")
        self.assertOK(response)

    def test_delete(self):
        response = self.delete("/")
        self.assertEqual(405, response.status_int)

