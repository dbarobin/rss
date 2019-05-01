#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python 2.7.10
# Copyright © 2019 Robin Wen <blockxyz@gmail.com>
#
# Distributed under terms of the MIT license.

# rss-opml
#  - lists blog url to opml format

import sys
import os
import requests
from datetime import datetime
from urllib2 import urlopen
from bs4 import BeautifulSoup

reload(sys)
sys.path.append(".")
sys.setdefaultencoding('utf-8')

OPML_START = """<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <head>
        <title>独立 blog 订阅列表 by 利器 liqi.io %(today)s</title>
    </head>
    <body>
        <outline text="独立 blog 订阅列表 by 利器 liqi.io %(today)s" title="独立 blog 订阅列表 by 利器 liqi.io %(today)s">"""

OPML_END = """      </outline>
    </body>
</opml>"""

OPML_OUTLINE_FEED = '          <outline text="%(title)s" title="%(title)s" type="rss" xmlUrl="%(xml_url)s" htmlUrl="%(htmlUrl)s" />'

# Retrieve title of webpage.
def get_tile(domain):
    try:
        res = requests.get(domain)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        return soup.title.text
    except Exception, e:
        print e

def main():

    print("Write result to file. Wait until program exit elegantly.\n")

    today = datetime.today().strftime('%Y%m%d')

    # write to file
    f = open('独立 blog 订阅列表 by 利器 liqi.io '+today+'.xml', 'w')

    f.write(OPML_START % {'today': today})
    f.write('\n')

    with open('blog.log') as inf:
        for line in inf:
            parts = line.split(',')
            url = str(parts[0].rstrip())
            title = str(get_tile(url).lstrip().rstrip())

            if len(parts) > 1:
                feed = str(parts[1].rstrip())
            f.write(OPML_OUTLINE_FEED % {'title': title, 'xml_url': feed, 'htmlUrl': url})
            f.write('\n')

    f.write(OPML_END)
    f.close

if __name__ == "__main__":
    main()