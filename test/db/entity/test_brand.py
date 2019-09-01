from unittest import TestCase
from db.entity.brand import Brand
from datetime import datetime


class TestBrand(TestCase):
    def test(self):
        print("Test Brand start")
        brand1 = Brand(code="3382", name="セブン＆アイ・ホールディングス", short_name="セブン＆アイ",
                       market="東証１", sector="小売業", unit=100)
        self.assertEqual(brand1.code, "3382", "test message")
        self.assertEqual(brand1.name, "セブン＆アイ・ホールディングス", "test message")
        self.assertEqual(brand1.short_name, "セブン＆アイ", "test message")
        self.assertEqual(brand1.market, "東証１", "test message")
        self.assertEqual(brand1.sector, "小売業", "test message")
        self.assertEqual(brand1.unit, 100, "test message")

        with self.assertRaises(Exception):
            Brand(code="", name="セブン＆アイ・ホールディングス", short_name="セブン＆アイ",
                  market="東証１", sector="小売業", unit=100)
        with self.assertRaises(Exception):
            Brand(code="3382", name="", short_name="セブン＆アイ",
                  market="東証１", sector="小売業", unit=100)
        with self.assertRaises(Exception):
            Brand(code="3382", name="セブン＆アイ・ホールディングス", short_name="",
                  market="東証１", sector="小売業", unit=100)
        with self.assertRaises(Exception):
            Brand(code="3382", name="セブン＆アイ・ホールディングス", short_name="セブン＆アイ",
                  market="", sector="小売業", unit=100)
        with self.assertRaises(Exception):
            Brand(code="3382", name="セブン＆アイ・ホールディングス", short_name="セブン＆アイ",
                  market="東証１", sector="", unit=100)
        with self.assertRaises(Exception):
            Brand(code="3382", name="セブン＆アイ・ホールディングス", short_name="セブン＆アイ",
                  market="東証１", sector="小売業", unit=0)
        print("Test Brand end")
