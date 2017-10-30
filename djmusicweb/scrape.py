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


def process_song(source):
    print(source)


def djmusicweb(url):
    soup = make_soup(url)
    for atag in soup.findAll("a"):
        if atag["href"].endswith(".mp3"):
            process_song(atag["href"])


if __name__ == '__main__':
    djmusicweb("http://nyk.djmusicweb.com/djnyk-single-music.php")
    djmusicweb("http://shireen.djmusicweb.com/djshireen-single-music.php#start")
    djmusicweb("http://lemon.djmusicweb.com/djlemon-single-music.php#start")
    djmusicweb("http://akhil.djmusicweb.com/djakhiltalreja-single-music.php")
    djmusicweb("http://aftermorning.djmusicweb.com/aftermorning-single-music.php#start")
    djmusicweb("http://tejas.djmusicweb.com/djtejas-single-music.php#start")