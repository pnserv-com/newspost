# -*- coding: utf-8 -*-

import os
import sys
import json
import glob
import datetime


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


def main():
    path = sys.argv[1]
    rule = os.path.join(expandpath(path), '*_char54_*.json')

    for filename in glob.glob(rule):
        register(filename)


if __name__ == '__main__':
    main()
