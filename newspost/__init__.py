# -*- coding: utf-8 -*-

import os
import json
import glob
import datetime
from argparse import ArgumentParser
from ConfigParser import SafeConfigParser

from nckvsclient import KVSClient


def expandpath(path):
    return os.path.abspath(os.path.expanduser(path))


def parse(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def extract(news):
    return [x['article'] for x in sorted(news, key=lambda x: x['seq'])]


def prepare(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    return {
        "type": name.split('_')[-1],
        "articles": extract(parse(filename)),
        "updated_at": mtime.isoformat()
    }


def upsert(nckvs, data):
    data = [dict(id='-1', **x) for x in data]
    return nckvs.set(data)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('dir')
    parser.add_argument('-c', '--config', default='newspost.ini')
    return parser.parse_args()


def main():
    args = parse_args()

    parser = SafeConfigParser()
    parser.read(args.config)
    config = dict(parser.items('nckvs'))
    config['datatypeversion'] = int(config.get('datatypeversion', '1'))
    nckvs = KVSClient(**config)

    rule = os.path.join(expandpath(args.dir), '*_char54_*.json')
    data = [prepare(x) for x in glob.glob(rule)]
    print upsert(nckvs, data)


if __name__ == '__main__':
    main()
