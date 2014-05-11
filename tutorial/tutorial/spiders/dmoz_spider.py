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
            name =chapter.xpath('h4/text()').extract()
            if name:
                print unicode(name.pop())
            images = chapter.xpath('p/a[contains(@href, "page")]/text()').extract()
            if images:
                print 'http://www.dragonball-multiverse.com/jp/pages/small/'+ self.getpng(images[0])
                #self.download_photo('http://www.dragonball-multiverse.com/jp/pages/small/'+ self.getpng(images[0]), str(i), 'small_' + self.getpng(images[0]))
                for image in images:
                    print 'http://www.dragonball-multiverse.com/jp/pages/final/' + self.getpng(image)
                #    self.download_photo('http://www.dragonball-multiverse.com/jp/pages/final/' + self.getpng(image),str(i), self.getpng(image))


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

    def getpng(self,id):
        return "%4s.jpg" %id
