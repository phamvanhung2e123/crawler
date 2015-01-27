# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.spider import Spider
import os
import urllib
import re
from scrapy.selector import Selector

class KiemtienSpider(Spider):
    name = "kiemtien"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "file:///Users/phamvanhung/Downloads/chokai/chokai1.1/index.php.html"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        sel = Selector(response)
        audios = sel.xpath('//audio/source/@src').extract()
        for audio in audios:
            print audio
            audio_url = 'http://old.lophoctiengnhat.com/' + audio
            audio_name = re.split('/',audio)[2]
            print audio_url
            print audio_name
            self.download_audio(filename,audio_name,audio_url)
        with open(filename, 'wb') as f:
            f.write(response.body)

    def download_audio(self, folder_name, audio_name, audio_url):
        try:
            image_on_web = urllib.urlopen(audio_url)
            if image_on_web.headers.maintype == 'audio':
                print audio_url
                print audio_name
                buf = image_on_web.read()
                path = '/Users/phamvanhung/Downloads/chokai/' + folder_name + '/Audio/FD6/'
                if not os.path.exists(path):
                    os.makedirs(path)
                file_path = "%s%s" % (path, audio_name)
                downloaded_image = file(file_path, "wb")
                downloaded_image.write(buf)
                downloaded_image.close()
                image_on_web.close()
            else:
                return False
        except:
            return False
        return True


