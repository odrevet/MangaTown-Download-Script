#!/usr/bin/env python
# encoding: utf-8

import sys
import argparse
import os
import urllib.request
import glob
import shutil
import re
import gzip
from itertools import filterfalse
from zipfile import ZipFile
from functools import reduce
from bs4 import BeautifulSoup
from contextlib import closing
from collections import OrderedDict
from io import StringIO
import ssl

PROTOCOL = 'https'
HOSTNAME = 'www.mangatown.com/'
ctx =  ssl.SSLContext(ssl.PROTOCOL_TLSv1)

def get_page_soup(url):
    """Download a page and return a BeautifulSoup object of the html"""
    response = urllib.request.urlopen(url, context=ctx)
    if response.info().get('Content-Encoding') == 'gzip':
        gzipFile = gzip.GzipFile(fileobj=response)
        page_content = gzipFile.read()
    else:
        page_content = response.read()

    soup_page = BeautifulSoup(page_content, "html.parser")

    return soup_page

def get_chapter_urls(manga_name):
    """Get the chapter list for a manga"""
    url = '{0}://{1}manga/{2}/'.format(PROTOCOL, HOSTNAME, manga_name)
    soup = get_page_soup(url)
    ul = soup.find('ul', {'class' : 'chapter_list'})
    links = ul.find_all('a')

    if(len(links) == 0):
        sys.exit('Error: Manga either does not exist or has no chapters')

    #the chapter number is the trailling float of the link text
    get_chapter_from_text = re.compile("([0-9]*\.[0-9]+|[0-9]+)$")

    chapters = OrderedDict()
    for link in links:
        chapters[float(get_chapter_from_text.search(link.text.strip()).group(0))] = PROTOCOL + ':' + link['href']
    ordered_chapters = OrderedDict(sorted(chapters.items()))

    return ordered_chapters

def get_page_numbers(soup):
    """Return the list of page numbers from the parsed page"""
    select_page = soup.findAll('select')[1]
    return (option['value'] for option in select_page.findAll('option'))

def get_chapter_image_urls(url_fragment):
    """Find all image urls of a chapter and return them"""
    chapter = get_page_soup(url_fragment)
    pages = get_page_numbers(chapter)
    image_urls = []
    print('Getting image urls...')
    for page in pages:
        page_soup = get_page_soup(PROTOCOL + ':' + page)
        image = page_soup.find('img', {'id': 'image'})
        if image:
            print('Image  : ', image['src'])
            image_urls.append(image['src'])
        else:
            print("Image not found on page...")
    return image_urls

def get_chapter_number(url_fragment):
    """Parse the url fragment and return the chapter number."""
    return ''.join(url_fragment.rsplit("/")[5:-1])

def download_urls(image_urls, manga_name, chapter_number):
    """Download all images from a list"""
    download_dir = '{0}/{1}/'.format(manga_name, chapter_number)
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)
    for i, url in enumerate(image_urls):
        filename = './{0}/{1}/{2:03}.jpg'.format(manga_name, chapter_number, i)

        print('Downloading {0} to {1}'.format(url, filename))
        while True:
            try:
                urllib.request.urlretrieve(url, filename)
            except urllib.error.HTTPError as http_err:
                print ('HTTP error ', http_err.code, ": ", http_err.reason)
                if http_err.code == 404:
                    break

            except urllib.error.ContentTooShortError:
                print ('The image has been retrieve only partially.')
            except:
                print ('Unknown error')
            else:
                break

def make_cbz(dirname):
    """Create CBZ files for all JPEG image files in a directory."""
    zipname = dirname + '.cbz'
    images = sorted(glob.glob(os.path.abspath(dirname) + '/*.jpg'))
    with closing(ZipFile(zipname, 'w')) as zipfile:
        for filename in images:
            print('writing {0} to {1}'.format(filename, zipname))
            zipfile.write(filename, arcname=os.path.basename(filename))

def download_manga(manga_name, range_start=1, range_end=None, b_make_cbz=False, remove=False):
    """Download a range of a chapters"""

    chapter_urls = get_chapter_urls(manga_name)

    if range_end == None : range_end = max(chapter_urls.keys())

    for chapter, url in filterfalse (lambda chapter_url:
                                     chapter_url[0] < range_start
                                     or chapter_url[0] > range_end,
                                     chapter_urls.items()):
        chapter_number = get_chapter_number(url)

        print('===============================================')
        print('Chapter ' + chapter_number)
        print('===============================================')

        image_urls = get_chapter_image_urls(url)
        download_urls(image_urls, manga_name, chapter_number)
        download_dir = './{0}/{1}'.format(manga_name, chapter_number)
        if b_make_cbz is True:
            make_cbz(download_dir)
            if remove is True: shutil.rmtree(download_dir)

def main():
    parser = argparse.ArgumentParser(description='Manga Fox Downloader')

    parser.add_argument('--manga', '-m',
                        required=True,
                        action='store',
                        help='Manga to download')

    parser.add_argument('--start', '-s',
                        action='store',
                        type=float,
                        default=1,
                        help='Chapter to start downloading from')

    parser.add_argument('--end', '-e',
                        action='store',
                        type=float,
                        default=None,
                        help='Chapter to end downloading to')

    parser.add_argument('--cbz', '-c',
                        action="store_true",
                        default=False,
                        help="Create cbz archive after download")

    parser.add_argument('--remove', '-r',
                        action="store_true",
                        default=False,
                        help="Remove image files after the creation of a cbz archive")

    parser.add_argument('--list', '-l',
                        action="store_true",
                        default=False,
                        help="List chapters")

    args = parser.parse_args()

    if args.list is True:
        chapter_urls = get_chapter_urls(args.manga)
        for chapter_url in chapter_urls:
            print (chapter_url)
    else:
        print('Getting chapter of ', args.manga, 'from ', args.start, ' to ', args.end)
        download_manga(args.manga, args.start, args.end, args.cbz, args.remove)

if __name__ == "__main__":
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0')]
    urllib.request.install_opener(opener)
    main()
