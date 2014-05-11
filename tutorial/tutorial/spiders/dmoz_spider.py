# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.spider import Spider
import os
import urllib

from scrapy.selector import Selector

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dragonball-multiverse.com/jp/chapters.html",
    ]

    def parse(self, response):
        sel = Selector(response)
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
        self.download_photo('http://www.dragonball-multiverse.com/jp/pages/final/0024.png','1','1.png')
        chapters = sel.xpath('//div[contains(@class, "cadrelect")]')
        i=0
        for chapter in chapters:
            i +=1
            name= chapter.xpath('h4/text()').extract()
            print name
            name = chapter.xpath('a[contains(@href, "page")]/text()').extract()
            print name
            #self.download_photo('http://www.dragonball-multiverse.com/jp/pages/final/0722.png',str(i),)


    def download_photo(self, img_url, folder_name, filename):
        try:
            image_on_web = urllib.urlopen(img_url)
            if image_on_web.headers.maintype == 'image':
                buf = image_on_web.read()
                path = os.getcwd() + '/' + folder_name + '/'
                if not os.path.exists(path):
                    os.makedirs(path)
                file_path = "%s%s" % (path, filename)
                downloaded_image = file(file_path, "wb")
                downloaded_image.write(buf)
                downloaded_image.close()
                image_on_web.close()
            else:
                return False
        except:
            return False
        return True