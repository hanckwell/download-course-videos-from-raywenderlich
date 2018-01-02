#!/usr/bin/env python3

# Author: moomons
# https://github.com/moomons/RayWenderlich-Crawler

import re
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import requests
import uncurl
from urllib.parse import urlparse
import youtube_dl
import os

# Tried to add referer in the youtube_dl header to download vimeo videos directly but failed
#import youtube_dl.utils
#youtube_dl.utils.std_headers['referer'] = 'https://videos.raywenderlich.com/'
#print(youtube_dl.utils.std_headers)

# Note: Replace str_curl with your cURL
str_curl = "..."

vimeo_pfx = "https://player.vimeo.com/video/"
ydl_opts = {'writesubtitles': True}


def get_host(url):
    data = urlparse(url)
#    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return data.netloc
            

def download_vimeo(vimeo_id):
    vimeo_url = vimeo_pfx + vimeo_id
    print(vimeo_url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([vimeo_url])


def main():

#    response = HtmlResponse(url='https://videos.raywenderlich.com/courses/90-programming-in-swift/lessons/1', **kwargs)
    cmd_curl = uncurl.parse(str_curl)
    response = eval(cmd_curl)
    fmt_curl = cmd_curl.replace(response.url, "%s")
    body = response.text
    tables = Selector(text=body).xpath('//ul[@class="lesson-table"]')#.extract()
    host = "https://" + get_host(response.url)
    
    title = Selector(text=body).xpath('//h2[@class="course-title"]/text()').extract_first()
    
    try:
        if not os.path.exists(title):
            os.makedirs(title)
        else:
            print('Already downloaded! Quitting.')
            exit(0)
    except OSError:
        print('FATAL: Error creating directory. ' + directory)
        exit(-1)
    
    fi = open('%s/info.txt' % title, "w")
    f = open('%s/videos.txt' % title, "w")
    
    # http://masnun.com/2016/09/18/python-using-the-requests-module-to-download-large-files-efficiently.html
    def download_file(url, filename):
        response = requests.get(url, stream=True)
        handle = open(title + '/' + filename, "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)
    
    def grab(part, number, curl, time, name):
        r = eval(curl)
        body = r.text
        with open('%s/%s-%s %s.htm' % (title, part, number, name), 'w') as src:
            src.write(body)
        fi.write(r.url + '\n')
        materials = Selector(text=body).xpath('//a[@class="download-materials"]')
        if materials:
            materials_filename = materials.xpath('@download').extract_first()
            materials_url = host + materials.xpath('@href').extract_first()
            fi.write(materials_url + ' ' + materials_filename + '\n')
    #        materials = li.xpath('//section[@id="video-info"]')
    #        print(materials.extract(), materials_filename, materials_url)
            download_file(materials_url, "%s-%s %s" % (part, number, materials_filename))
        vimeo_id = Selector(text=body).xpath('//div[@id="vimeo-player"]/@data-vimeo-id').extract_first()
#        download_vimeo(vimeo_id)
        vimeo_url = vimeo_pfx + vimeo_id
        fi.write(vimeo_url + '\n\n')
        f.write(vimeo_url + '\n')
    
    for part, table in enumerate(tables, 1):
        print("Part %d" % part)
        for li in table.xpath('li'):
            number = li.xpath('span[@class="lesson-number"]/text()').extract_first()
            url = response.url
            name = li.xpath('span[@class="lesson-name"]/a/text()').extract_first()
            if not name:  # Trick. Contains class 'active'
                name = li.xpath('span[@class="lesson-name"]/text()').extract_first()
            else:
                url = host + li.xpath('span[@class="lesson-name"]/a/@href').extract_first()
            time = li.xpath('span[@class="lesson-time"]/text()').extract_first()
            print(number, url, name, time)
            fi.write(str(part) + '-' + number + ' ' + name + '\n')
            grab(part, number, fmt_curl % url, time, name)
    
    f.close()
    fi.close()
    
    # Launch youtube-dl
    print('\nRun the following command to download videos:')
    print('cd "%s" && youtube-dl -a videos.txt --referer https://videos.raywenderlich.com/ --all-subs -o "%(autonumber)s %(id)s %(title)s.%(ext)s" --external-downloader aria2c --external-downloader-args "-c -j 3 -x 3 -s 3 -k 1M" && for f in *.vtt; do ffmpeg -i $f $f.srt; done"' % title)
#    os.chdir(title)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python3 rwcrawl.py [URL]')
        exit(0)
        
    str_curl = str_curl % sys.argv[1]
    main()
    