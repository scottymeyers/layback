#!/usr/bin/python
# Layback Machine
# Wayback Machine gif Generator

import re, os
import urllib2 as rq
from   selenium import webdriver
import imageio

class Archive(object):
    def __init__(self, url, download_path):
        self.url = url
        self.prefix = "http://" if self.url.startswith('http://') | self.url.startswith('https://') == False else ""
        self.download_path = download_path + self.url.strip('http://') + '/'

    def initialize(self):
        urls = self.obtain_momentos()
        filenames = self.save_screenshots(urls)
        self.save_as_gif()

    def obtain_momentos(self):
        r = rq.urlopen("https://web.archive.org/web/timemap/link/" + self.prefix + self.url)
        mementos = []

        for line in r:
            mementos.append(re.search("(?P<url>https?://[^\s]+)", line).group("url").replace(">;", ""))

        mementos = mementos[2:]

        return mementos

    def save_screenshots(self, urls):
        num = 0

        driver = webdriver.PhantomJS()
        driver.set_window_size(1024, 768)

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        for url in urls:
            img_name = self.download_path + str(num) + '.jpg'
            driver.get(url)
            driver.save_screenshot(img_name)
            num += 1

        driver.quit()

    def save_as_gif(self):
        image_files = next(os.walk(self.download_path))[2]
        image_data = []

        for image in image_files:
            if os.path.splitext(image)[1] == ".jpg":
                image_data.append(imageio.imread(self.download_path + image))
                os.remove(self.download_path + image)

        imageio.mimsave(self.download_path + 'movie.gif', image_data)

        print "successfully saved gif to " + self.download_path + 'movie.gif'