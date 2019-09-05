# -*- coding: utf-8 -*-
import db.job as db_job
import simulation.job as simulate_job
from crawler.job import save_newbrand
from crawler.job import save_stock
from crawler.job import sync_brand
from notification.job import brand_notification


def setup():
    db_job.setup()


def save_crawl():
    save_newbrand()
    sync_brand()
    save_stock()


def notification():
    brand_notification()


def simulate():
    simulate_job.simulate()
