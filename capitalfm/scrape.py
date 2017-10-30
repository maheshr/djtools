#!/usr/bin/env python

import os.path
import re
import urllib.request
from urllib.error import HTTPError

from bs4 import BeautifulSoup


def make_soup(url):
    with urllib.request.urlopen(url) as url:
        content = url.read()
        soup = BeautifulSoup(content, "html.parser")
        return soup


def process_youtube(src):
    print(src)


def process_filecdn(src, name):
    regex = r"\{mp3:\"(.*)\"\}"
    dest = name + ".mp3"
    dest = dest.replace("/", "_")
    print("Dest:", dest)
    if os.path.exists(dest):
        print("skipping filecdn as already downloaded")
        return

    soup = make_soup(src)
    for script in soup.findAll("script"):
        if script.text:
            m = re.search(regex, script.text, re.MULTILINE)
            if m:
                print(m.group(1))
                source = m.group(1)
                urllib.request.urlretrieve(source, dest)
            else:
                print("no match")


def process_soundcloud(src):
    try:
        regex = r'\"permalink_url\":\"(.*?)\"'
        with urllib.request.urlopen(src) as url:
            content = url.read()
            content = content.decode('utf-8')
            m = re.search(regex, content, re.MULTILINE)
            if m:
                print(m.group(1))
            else:
                print("no match")
    except HTTPError:
        pass


def process_song(h3):
    name = h3.text.strip()
    if not name:
        print("h3 has no name")
        return

    print(name)

    p = h3.find_next_sibling("p")
    if not p:
        print("failed to find p")
        return

    iframe = p.contents[0]
    if iframe.name != 'iframe':
        print("failed to find iframe")
        return

    src = iframe["src"].strip()

    if "www.youtube.com" in src:
        process_youtube(src)

    if "filescdn.com" in src:
        process_filecdn(src, name)

    if "soundcloud.com" in src:
        process_soundcloud(src)


def capitalfm(url):
    soup = make_soup(url)
    for h3 in soup.findAll("h3"):
        if h3.parent.name == 'article':
            process_song(h3)


if __name__ == '__main__':
    #capitalfm("http://www.capitalfm.com/new-music/remixes/best-this-week-27-november-2015/")
    #capitalfm("http://www.capitalfm.com/new-music/remixes/january-2016/")
    #capitalfm("http://www.capitalfm.com/new-music/remixes/february-2016/")
    #capitalfm("http://www.capitalfm.com/new-music/remixes/march-2016/")
    #capitalfm("http://www.capitalfm.com/new-music/remixes/april-2016/")
    #capitalfm("http://www.capitalfm.com/new-music/remixes/may-2016/")
    #capitalfm("http://www.capitalfm.com/new-music/remixes/december-2016/")
    #capitalfm("http://www.capitalfm.com/new-music/remixes/january-2017/")
    capitalfm("http://www.capitalfm.com/new-music/remixes/february-2017/")
