from unittest import TestCase
from db.entity.new_brand import NewBrand
from datetime import datetime

from db.entity.price import Price


class TestPrice(TestCase):
    def test(self):
        print("Test Price start")
        Price("3000", datetime(2019, 8, 30), 3789.0, 3790.0, 3717.0, 3757.0, 2355700, 3757.0)
        with self.assertRaises(Exception):
            Price(3000, datetime(2019, 8, 30), 3789.0, 3790.0, 3717.0, 3757.0, 2355700, 3757.0)
        with self.assertRaises(Exception):
            Price("", datetime(2019, 8, 30), 3789.0, 3790.0, 3717.0, 3757.0, 2355700, 3757.0)
        with self.assertRaises(Exception):
            Price("3000", "2019/08/30", 3789.0, 3790.0, 3717.0, 3757.0, 2355700, 3757.0)
        with self.assertRaises(Exception):
            Price("3000", datetime(2019, 8, 30), 3789, 3790.0, 3717.0, 3757.0, 2355700, 3757.0)
        with self.assertRaises(Exception):
            Price("3000", datetime(2019, 8, 30), 3789.0, 3790, 3717.0, 3757.0, 2355700, 3757.0)
        with self.assertRaises(Exception):
            Price("3000", datetime(2019, 8, 30), 3789.0, 3790.0, 3717.0, 3757.0, 2355700, 3757)

        print("Test Price")
