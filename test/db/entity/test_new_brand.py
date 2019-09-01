from unittest import TestCase
from db.entity.new_brand import NewBrand
from datetime import datetime


class TestNewBrand(TestCase):
    def test(self):
        print("NewBrandTest start")
        newBrand1 = NewBrand("3000", "2019/08/30", "company1")
        self.assertEqual(newBrand1.code, "3000", "test message")
        self.assertEqual(newBrand1.date, datetime(2019, 8, 30))

        newBrand2 = NewBrand("3001", "2019/08/31", "company2")
        self.assertEqual(newBrand2.code, "3001", "test message")
        self.assertEqual(newBrand2.date, datetime(2019, 8, 31))

        # 対象外フォーマットでのエラーの検出を確認
        with self.assertRaises(Exception):
            NewBrand("3002", "2019-08-30")

        print("NewBrandTest end")
