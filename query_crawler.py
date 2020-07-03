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
import datetime
import pandas as pd

# Settings
SLEEP = 1           # secs
TIMEOUT = 30        # secs
TIMEOUT_LIMIT = 5   # counts
PAGE_LIMIT = 50     # pages


def crawl(query, begin, end, save_as, sort, field):
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

        # sleep before starting
        time.sleep(SLEEP + random.random())

        # open url
        try:
            print('opening url:', url)
            html = urlopen(url, timeout=TIMEOUT)

        except (URLError, SSLError) as e:
            print('(Error!) URLError or SSLError', e)
            print('reloading...')
            time.sleep(TIMEOUT)
            continue

        # make bsobj
        try:
            print('parsing html')
            bsobj = BeautifulSoup(html, "html.parser")

        except socket.timeout as e:
            print('(Error!) socket.timeout', e)
            print('reloading...')
            time.sleep(TIMEOUT)
            continue

        # open urls inside, which are included as '네이버뉴스'
        for obj in bsobj.select("._sp_each_url"):
            url = obj['href']

            if url in links:
                print('\turl already crawled:', url)
                continue

            if 'https://news.naver.com' in url:
                time.sleep(0.3 + random.random())

                print('\topening inside', url)
                try:
                    # get news info
                    title, date, article = get_naver_news(url, TIMEOUT, TIMEOUT_LIMIT)

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
        if PAGE_LIMIT and (page > 1 + 10 * PAGE_LIMIT):
            print('page limit exceeded: page(%i) > page_limit(%i)' % (page, PAGE_LIMIT))
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

    # open url
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


if __name__ == '__main__':
    # crawl("트러스제7호", "2019.03.01", "2019.03.31", save_as='test.xlsx')
    # crawl("영현무역", "2016.03.01", "2016.03.31", save_as='test.xlsx')    # no result test
    # crawl("영현무역", "2016.04.01", "2016.04.30", save_as='test.xlsx')    # one page test
    crawl("두산중공업", "2016.03.01", "2016.03.30", save_as='test.xlsx', sort=0, field=1)   # run test
    # crawl("아이유", "2020.01.01", "2020.06.22", save_as='test.xlsx', sort=0, field=1)   #  크롤링 안됨 (연예)
