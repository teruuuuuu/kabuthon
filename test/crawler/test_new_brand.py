from unittest import TestCase
from crawler.new_brand import get_new_brands2
from datetime import datetime

class TestNewBrand(TestCase):
    def test(self):
        print("Test CrawlNewBrand star")
        today = datetime.now().date()
        mukashi = today.replace(year=today.year-2)
        new_brands = list(get_new_brands2())
        for nb in new_brands:
            self.assertNotEqual(nb[0].strip(), "")
            self.assertEqual(nb[1] >= mukashi, True)
        self.assertEqual(len(new_brands) > 0, True)
        print("Test CrawlNewBrand end")
