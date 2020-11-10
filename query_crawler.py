'''
By Minsang Yu. flowerk94@gmail.com.
'''

from ssl import SSLError
from urllib import parse
from urllib.error import URLError
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import socket
import random
import argparse
import datetime
import pandas as pd


def crawl(query, save_as, begin, end, sort=0, field=1, delay=0.5, timeout=30, page_limit=50):
    # sort: 0 (관련도순), 1 (최신순), 2 (오래된순) | field: 0 (전체), 1 (제목)

    # prerequisite
    df = pd.DataFrame(columns=['link', 'title', 'date', 'article'])
    page = 1
    max_page = 2

    while (page <= max_page) and (page <= 1 + 10 * page_limit):
        print('\n' + 'crawling... %s (page %i/%i)' % (query, 1+page//10, 1+max_page//10))
        url = make_url(query, sort, field, begin, end, page)
        print('making url', url)

        print('making beautifulsoup object from html')
        bsobj = make_bsobj(url, delay, timeout, trial=10)
        if bsobj is None:
            continue

        print('extracting naver news urls from bsobj')
        naver_news_urls = make_naver_news_urls(bsobj)

        for url in naver_news_urls:
            print('\topening:', url)
            news_bsobj = make_bsobj(url, delay, timeout, trial=10)
            if news_bsobj is None:
                continue

            attributes = get_attributes(news_bsobj)
            if attributes is None:
                continue

            date, article, title = attributes
            df = df.append({'link': url, 'title': title, 'date': date, 'article': article}, ignore_index=True)
            print('\t', title)

        print('saving updated df')
        df = df.sort_values(by=['date'])
        df.to_excel(save_as, engine='xlsxwriter')

        print('updating page info')
        page += 10
        max_page = get_max_page(bsobj)
        if max_page is None:
            break
        print('next page:', page//10 + 1)


def make_url(query, sort, field, begin, end, page):
    url = "https://search.naver.com/search.naver?&where=news&query=" + parse.quote(query)
    url += "&sort=%i" % sort
    url += "&field=%i" % field
    url += "&ds=" + begin + "&de=" + end
    url += "&nso=so:r,p:"
    url += "from" + begin.replace(".", "") + "to" + end.replace(".", "")
    url += "&start=" + str(page)
    url += "&refresh_start=0"
    return url


def make_bsobj(url, delay=0.5, timeout=30, trial=10):
    ua = UserAgent(verify_ssl=False)
    count = 0

    while count < trial:
        try:
            time.sleep(delay + random.random())
            html = urlopen(Request(url=url, headers={'User-Agent': ua.random}), timeout=timeout)
            bsobj = BeautifulSoup(html, 'html.parser')
            return bsobj
        except (URLError, SSLError, socket.timeout) as e:
            print('(Error)', e)
            print('reloading...')
            count += 1
            time.sleep(timeout)
    return None


def make_naver_news_urls(bsobj):
    return [link['href'] for link in bsobj.find_all('a', href=True)
            if 'https://news.naver.com/main/read' in link['href']]


def get_attributes(bsobj):
    def _get_title(bsobj):
        title = bsobj.select('h3#articleTitle')[0].text
        title = title.encode('utf-8', 'replace').decode()
        return title

    def _get_article(bsobj):
        article = bsobj.select('#articleBodyContents')[0].text
        article = article.encode('utf-8', 'replace').decode()
        return article

    def _get_date(bsobj):
        splits = bsobj.select('.t11')[0].text.split(' ')
        date = splits[0] + ' ' + splits[2]
        date = datetime.datetime.strptime(date, '%Y.%m.%d. %H:%M')
        date += datetime.timedelta(hours=12 * int(splits[1] == '오후'))
        return date

    try:
        return _get_date(bsobj), _get_article(bsobj), _get_title(bsobj)
    except IndexError:
        print('(Error) crawling failed (maybe url is redirected to somewhere else)')
        return None


def get_max_page(bsobj):
    paging = bsobj.find("div", {"class": "paging"})
    if not paging:
        print('(WARNING!) no results found')
        return None

    atags = paging.find_all('a')
    if not atags:
        print('(WARNING!) there is only one page')
        return None

    return max([int(atag["href"].split('start=')[1]) for atag in atags])




def get_arguments():
    # Argument configuration
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, required=True, help='query to search on NAVER')
    parser.add_argument('--begin', type=str, required=True, help='crawling begin point (%%Y.%%m.%%d format)')
    parser.add_argument('--end', type=str, required=True, help='crawling end point (%%Y.%%m.%%d format)')
    parser.add_argument('--save_as', type=str, default='test.xlsx', help='excel save path')
    parser.add_argument('--sort', type=int, default=0, help='search result sorting: 0(relevant), 1(newest), 2(oldest)')
    parser.add_argument('--field', type=int, default=1, help='search field: 0(all), 1(title)')
    return parser.parse_args()


def test():
    query = '삼성전자'
    begin = '2020.11.09'
    end = '2020.11.12'
    save_as = 'test.xlsx'
    crawl(query, begin, end, save_as)


if __name__ == '__main__':
    args = get_arguments()
    query = args.query
    begin = args.begin
    end = args.end
    save_as = args.save_as
    sort = args.sort
    field = args.field

    crawl(query, save_as, begin, end, sort, field)
