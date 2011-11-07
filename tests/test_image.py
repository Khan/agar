from google.appengine.api import images

from agar.image import Image
from agar.test import BaseTest


TEST_IMAGE_PATH = 'tests/media/appengine-noborder-120x30.jpg'


class ImageTest(BaseTest):
    def setUp(self):
        super(ImageTest, self).setUp()
        self.image_file = open(TEST_IMAGE_PATH)
        self.image_bytes = self.image_file.read()
        self.image_file.close()

    def test_create_with_data(self):
        image = Image.create(data=self.image_bytes, filename=TEST_IMAGE_PATH)
        self.assertMemcacheItems(0)
        self.assertEqual(image.get_serving_url(), images.get_serving_url(str(image.blob_key)))
        self.assertMemcacheItems(1)
        self.assertMemcacheHits(0)
        self.assertEqual(image.get_serving_url(), images.get_serving_url(str(image.blob_key)))
        self.assertMemcacheHits(1)
        image2 = Image.create(data=self.image_bytes, filename=TEST_IMAGE_PATH)
        self.assertNotEqual(image.get_serving_url(), images.get_serving_url(str(image2.blob_key)))
        self.assertMemcacheItems(1)
        self.assertMemcacheHits(2)
        self.assertEqual(image2.get_serving_url(), images.get_serving_url(str(image2.blob_key)))
        self.assertMemcacheItems(2)
        self.assertMemcacheHits(2)
