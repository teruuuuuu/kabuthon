from unittest import TestCase

from db.entity.brand import Brand
from db.entity.new_brand import NewBrand
from db.repository.brand_repo import BrandRepo
from datetime import datetime
from datetime import timedelta


class TestBrandRepo(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBrandRepo, self).__init__(*args, **kwargs)
        self.brandRepo = BrandRepo()
        BrandRepo()
        BrandRepo()
        BrandRepo()

    def test(self):
        print("Test BrandRepo start")
        self.brandRepo.setup()
        # 一旦全削除
        self.brandRepo.delete_all()
        self.checkBrand()
        self.checkNewBrand()
        print("Test BrandRepo end")

    def checkBrand(self):
        print("Test Brand start")
        brands1 = [
            Brand(code="3382", name="セブン＆アイ・ホールディングス", short_name="セブン＆アイ", market="東証１", sector="小売業", unit=100),
            Brand(code="4755", name="楽天", short_name="楽天", market="東証１", sector="サービス業", unit=100),
            Brand(code="6861", name="キーエンス", short_name="キーエンス", market="東証１", sector="電気機器", unit=100)]
        self.brandRepo.insert_brands(brands1)
        self.brandRepo.insert_brands(brands1)
        brands2 = [
            Brand(code="6752", name="パナソニック", short_name="パナソニック", market="東証１", sector="電気機器", unit=100),
            Brand(code="6861", name="キーエンス", short_name="キーエンス", market="東証１", sector="電気機器", unit=100)]
        self.brandRepo.insert_brands(brands2)
        print("Test Brand end")

    def checkNewBrand(self):
        this_year1 = datetime.now()
        this_year2 = this_year1 + timedelta(days=1)
        this_year3 = this_year2 + timedelta(days=1)
        last_year1 = this_year1 - timedelta(days=365)
        last_year2 = last_year1 + timedelta(days=1)
        two_years_ago1 = this_year1 - timedelta(days=730)

        print("Test newBrand start")
        newBrands1 = [NewBrand("3000", this_year1.strftime('%Y/%m/%d'), "会社A"),
                      NewBrand("3001", this_year2.strftime('%Y/%m/%d'), "会社B"),
                      NewBrand("3002", this_year3.strftime('%Y/%m/%d'), "会社C"),
                      NewBrand("3003", last_year1.strftime('%Y/%m/%d'), "会社D")]
        self.brandRepo.insert_new_brands(newBrands1)
        self.brandRepo.insert_new_brands(newBrands1)
        newBrands2 = [NewBrand("3002", this_year3.strftime('%Y/%m/%d'), "会社C"),
                      NewBrand("3003", last_year1.strftime('%Y/%m/%d'), "会社D"),
                      NewBrand("3004", last_year2.strftime('%Y/%m/%d'), "会社E"),
                      NewBrand("3005", two_years_ago1.strftime('%Y/%m/%d'), "会社F")]
        self.brandRepo.insert_new_brands(newBrands2)
        dic = dict(list(map(lambda newBrand: (newBrand.code, newBrand), self.brandRepo.select_new_brand_recently())))
        self.assertTrue("3000" in dic)
        self.assertTrue(dic["3000"].format_date() == this_year1.strftime('%Y/%m/%d'))
        self.assertTrue("3001" in dic)
        self.assertTrue(dic["3001"].format_date() == this_year2.strftime('%Y/%m/%d'))
        self.assertTrue("3002" in dic)
        self.assertTrue(dic["3002"].format_date() == this_year3.strftime('%Y/%m/%d'))
        self.assertTrue("3003" in dic)
        self.assertTrue(dic["3003"].format_date() == last_year1.strftime('%Y/%m/%d'))
        self.assertTrue("3004" in dic)
        self.assertTrue(dic["3004"].format_date() == last_year2.strftime('%Y/%m/%d'))
        self.assertFalse("3005" in dic)
        print("Test newBrand end")
