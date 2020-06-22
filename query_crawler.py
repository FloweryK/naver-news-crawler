from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
import os
import re
import time
import random
import datetime
import argparse
import pandas as pd


def crawler(query, begin, end, sleep, page_lmit, sort, field, save_path):
    '''
    :param query:
    :param begin:
    :param end:
    :param sleep:
    :param page_lmit:
    :param sort: 0 (관련도순), 1 (최신순), 2 (오래된순)
    :param field: 0 (전체), 1 (제목)
    :return:
    '''

    links = []
    titles = []
    dates = []
    articles = []

    page = 1
    max_page = 2
    while page <= max_page:
        print('crawling... %s page %i/%i' % (query, 1+page//10, 1+max_page//10))

        # make url
        url = "https://search.naver.com/search.naver?&where=news&query=" + parse.quote(query)
        url += "&sort=%i" % sort
        url += "&field=%i" % field
        url += "&ds=" + begin + "&de=" + end
        url += "&nso=so:r,p:"
        url += "from" + begin.replace(".", "") + "to" + end.replace(".", "")
        url += "&start=" + str(page)
        url += "&refresh_start=0"

        # make bs object
        print('opening url:', url)
        html = urlopen(url)
        bsobj = BeautifulSoup(html, "html.parser")

        # get urls which is included as '네이버뉴스'
        for obj in bsobj.select("._sp_each_url"):
            url = obj['href']
            if 'https://news.naver.com' in url:
                title, date, article = get_news(url)

                links.append(url)
                titles.append(title)
                dates.append(date)
                articles.append(article)

        # get next page
        atags = bsobj.find("div", {"class": "paging"}).find_all("a")
        max_page = max([int(atag["href"].split('start=')[1]) for atag in atags])
        page += 10
        if page_lmit and (page > page_lmit):
            break

        # sleep
        time.sleep(sleep + random.random() + 0.5)

        # save the results
        result = {
            'link': links,
            'title': titles,
            'date': dates,
            'article': articles
        }
        df = pd.DataFrame(result)
        df = df.sort_values(by=['date'])
        df.to_excel(save_path + query + '.xlsx')


def get_news(url):
    def _get_title(bsobj):
        return bsobj.select('h3#articleTitle')[0].text

    def _get_date(bsobj):
        splits = bsobj.select('.t11')[0].text.split(' ')

        date = splits[0] + ' ' + splits[2]
        date = datetime.datetime.strptime(date, '%Y.%m.%d. %H:%M')
        date += datetime.timedelta(hours=12 * int(splits[1] == '오후'))
        return date

    def _get_article(bsobj):
        article = bsobj.select('#articleBodyContents')[0].text

        # basic pre-processing
        article = re.sub('[\n]|[\xa0]', ' ', article)
        article = re.sub('[\[\]]', ' ', article)
        article = re.sub('\s{2,}', '', article)
        return article

    # make bs object
    html = urlopen(url)
    bsobj = BeautifulSoup(html, 'html.parser')

    # extract wanted elements
    title = _get_title(bsobj)
    date = _get_date(bsobj)
    article = _get_article(bsobj)

    return title, date, article


if __name__ == '__main__':
    # Argument configuration
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, required=True, help='query to search on NAVER')
    parser.add_argument('--begin', type=str, required=True, help='crawling begin point')
    parser.add_argument('--end', type=str, required=True, help='crawling end point')
    parser.add_argument('--path', type=str, default='results/', help='saving path for crawling results')
    parser.add_argument('--limit', type=int, default=0, help='crawling page limit on single query, 0 for no limit')
    parser.add_argument('--sort', type=int, default=0, help='search result sorting: 0(relevant), 1(newest), 2(oldest)')
    parser.add_argument('--field', type=int, default=1, help='search field: 0(all), 1(title)')
    parser.add_argument('--sleep', type=float, default=1., help='sleep interval between requests')
    args = parser.parse_args()

    query = args.query
    begin = args.begin
    end = args.end
    path = args.path
    limit = args.limit
    sort = args.sort
    field = args.field
    sleep = args.sleep

    if not os.path.exists(path):
        os.mkdir(path)

    crawler(query,
            begin,
            end,
            sleep=sleep,
            page_lmit=limit,
            sort=sort,
            field=field,
            save_path=path)

    # crawler("두산중공업", "2020.01.04", "2020.03.12", sleep=1, sort=1)
