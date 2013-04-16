# -*- coding: utf-8 -*-

import os
import json
import glob
import datetime
from argparse import ArgumentParser


def expandpath(path):
    return os.path.abspath(os.path.expanduser(path))


def parse(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def extract(news):
    return [x['article'] for x in sorted(news, key=lambda x: x['seq'])]


def register(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    param = {
        "type": name.split('_')[-1],
        "articles": extract(parse(filename)),
        "updated_at": datetime.datetime.now().isoformat()
    }
    print json.dumps(param, ensure_ascii=False)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('dir')
    return parser.parse_args()


def main():
    args = parse_args()
    rule = os.path.join(expandpath(args.dir), '*_char54_*.json')

    for filename in glob.glob(rule):
        register(filename)


if __name__ == '__main__':
    main()
