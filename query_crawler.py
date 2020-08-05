'''
By Minsang Yu. flowerk94@gmail.com.
'''

from ssl import SSLError
from urllib import parse
from urllib.error import URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import socket
import random
import argparse
import datetime
import pandas as pd


def crawl(query, begin, end, save_as, sort=0, field=1, delay=0.5, timeout=30, page_limit=10):
    # sort: 0 (관련도순), 1 (최신순), 2 (오래된순)
    # field: 0 (전체), 1 (제목)

    links = []
    titles = []
    dates = []
    articles = []

    page = 1
    max_page = 2
    while page <= max_page:
        print('\n' + 'crawling... %s (page %i/%i)' % (query, 1+page//10, 1+max_page//10))

        # make url
        url = "https://search.naver.com/search.naver?&where=news&query=" + parse.quote(query)
        url += "&sort=%i" % sort
        url += "&field=%i" % field
        url += "&ds=" + begin + "&de=" + end
        url += "&nso=so:r,p:"
        url += "from" + begin.replace(".", "") + "to" + end.replace(".", "")
        url += "&start=" + str(page)
        url += "&refresh_start=0"

        # open url
        try:
            print('opening url:', url)
            time.sleep(delay + random.random())
            html = urlopen(url, timeout=timeout)

        except (URLError, SSLError, socket.timeout) as e:
            print('(Error!)', e)
            print('reloading...')
            time.sleep(timeout)
            continue

        # make bsobj
        try:
            print('parsing html')
            bsobj = BeautifulSoup(html, "html.parser")

        except socket.timeout as e:
            print('(Error!) socket.timeout', e)
            print('reloading...')
            time.sleep(timeout)
            continue

        # open urls inside, which are included as '네이버뉴스'
        naver_news_urls = [link['href'] for link in bsobj.find_all('a', href=True) if 'https://news.naver.com/main/read' in link['href']]

        for url in naver_news_urls:
            if url in links:
                print('\turl already crawled:', url)
                continue

            if 'https://news.naver.com' in url:
                print('\topening inside', url)
                try:
                    # get news info
                    time.sleep(delay + random.random())
                    title, date, article = get_naver_news(url)
                    print('\t', title)

                    # add results
                    links.append(url)
                    titles.append(title)
                    dates.append(date)
                    articles.append(article)

                except TimeoutError as e:
                    print('\t(Error!) TimeoutError, Exceeded timeout limit', e)

                except IndexError:
                    print('\t(Error!) crawling failed (maybe url is redirected to somewhere else)')

        # save the results
        print(len(titles), 'are saved as naver news')
        result = {
            'link': links,
            'title': titles,
            'date': dates,
            'article': articles
        }
        df = pd.DataFrame(result)
        df = df.sort_values(by=['date'])
        df.to_excel(save_as, engine='xlsxwriter')

        # get paging info
        paging = bsobj.find("div", {"class": "paging"})
        if not paging:
            print('(WARNING!) no results found')
            break

        atags = paging.find_all('a')
        if not atags:
            print('(WARNING!) there is only one page')
            break

        # update page info
        max_page = max([int(atag["href"].split('start=')[1]) for atag in atags])
        page += 10

        # check if page is over page limit
        if page_limit and (page > 1 + 10 * page_limit):
            print('page limit exceeded: page(%i) > page_limit(%i)' % (page, page_limit))
            break


def get_naver_news(url, timeout=30, timeout_limit=5):
    def _get_title(bsobj):
        return bsobj.select('h3#articleTitle')[0].text

    def _get_date(bsobj):
        splits = bsobj.select('.t11')[0].text.split(' ')
        date = splits[0] + ' ' + splits[2]
        date = datetime.datetime.strptime(date, '%Y.%m.%d. %H:%M')
        date += datetime.timedelta(hours=12 * int(splits[1] == '오후'))
        return date

    def _get_article(bsobj):
        return bsobj.select('#articleBodyContents')[0].text

    # open url and get html
    count = 0
    while True:
        try:
            html = urlopen(url, timeout=timeout)
            bsobj = BeautifulSoup(html, 'html.parser')
            break

        except (URLError, SSLError, socket.timeout) as e:
            print('\t(Error!) Timeout (%i sec), trying again... (count=%i) %s' % (timeout, count, e))
            count += 1
            timeout += timeout
            time.sleep(timeout)

            if count > timeout_limit:
                raise TimeoutError

    # extract wanted elements
    title = _get_title(bsobj)
    date = _get_date(bsobj)
    article = _get_article(bsobj)

    return title, date, article


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
    query = 'LG화학'
    begin = '2019.08.02'
    end = '2019.08.02'
    save_as = 'test.xlsx'
    sort = 0
    field = 1
    crawl(query, begin, end, save_as, sort, field)


if __name__ == '__main__':
    test()
    exit()


    args = get_arguments()
    query = args.query
    begin = args.begin
    end = args.end
    save_as = args.save_as
    sort = args.sort
    field = args.field

    # crawl
    crawl(query, begin, end, save_as, sort, field)




