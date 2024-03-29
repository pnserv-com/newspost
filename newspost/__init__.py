# -*- coding: utf-8 -*-

import os
import json
import glob
import time
import datetime
from argparse import ArgumentParser
from ConfigParser import SafeConfigParser

from nckvsclient import KVSClient


def expandpath(path):
    return os.path.abspath(os.path.expanduser(path))


def parse(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def prepare(filename, timestamp):
    name = os.path.splitext(os.path.basename(filename))[0]
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    return [dict(article=item['article'].encode('utf-8'),
                 seq='{:02}'.format(item['seq']),
                 type=name.split('_')[-1],
                 delivered_at=mtime.isoformat(),
                 timestamp=timestamp)
            for item in parse(filename)]


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

    data = []
    timestamp = int(time.time())
    rule = os.path.join(expandpath(args.dir), '*_char54_*.json')
    for filename in glob.glob(rule):
        data.extend(prepare(filename, timestamp=timestamp))

    nckvs = KVSClient(**config)
    upsert(nckvs, data)


if __name__ == '__main__':
    main()
