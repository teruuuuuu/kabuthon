# -*- coding: utf-8 -*-

import sys
from task import task


def run(argv=sys.argv[1:]):
    import argparse
    parser = argparse.ArgumentParser(description='python kabu simulation')
    parser.add_argument('--setup', action='store_true')
    parser.add_argument('--crawl', action='store_true')
    parser.add_argument('--notification', action='store_true')
    parser.add_argument('--simulate', action='store_true')
    args = parser.parse_args(argv)
    if args.setup:
        task.setup()
    if args.crawl:
        task.save_crawl()
    if args.notification:
        task.notification()
    if args.simulate:
        task.simulate()
