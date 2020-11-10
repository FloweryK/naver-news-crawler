import os
import time
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from itertools import repeat
from query_crawler import crawl


def crawl_query_by_unit(query, begin, end, save_dir, mode, days=None):
    print('\n====== DATA INFO ======')
    print('time:', datetime.datetime.now())
    print('name:', query)
    print('begin:', begin)
    print('end:', end)

    # get nearest sunday
    partial_end = initialize_partial_end(end, mode)

    while partial_end >= begin:
        partial_begin = update_partial_begin(partial_end, mode, days)
        partial_begin_str = partial_begin.strftime('%Y.%m.%d')
        partial_end_str = partial_end.strftime('%Y.%m.%d')

        print('\nstart crawling: %s from %s to %s' % (query, partial_begin_str, partial_end_str))

        # start crawling
        save_as = os.path.join(save_dir, query, query + '_' + partial_begin_str + '-' + partial_end_str + '.xlsx')

        if os.path.exists(save_as):
            print('\talready crawled. go to next step')
        else:
            # crawl(query, partial_begin_str, partial_end_str, save_as)
            pass

        partial_end = update_partial_end(partial_end, mode, days)


def initialize_partial_end(end, mode):
    if mode == 'weekly':
        # nearest sunday after 'end'
        return end - datetime.timedelta(days=datetime.datetime.weekday(end)) + datetime.timedelta(days=6)
    elif mode == 'monthly':
        return end.replace(day=1) + relativedelta(months=1) - datetime.timedelta(days=1)
    elif mode == 'interval':
        return end


def update_partial_begin(partial_end, mode, days=None):
    if mode == 'weekly':
        # one last monday
        return partial_end - datetime.timedelta(days=6)
    elif mode == 'monthly':
        return partial_end.replace(day=1)
    elif mode == 'interval':
        return partial_end - datetime.timedelta(days=days-1)


def update_partial_end(partial_end, mode, days=None):
    if mode == 'weekly':
        # one last sunday
        return partial_end - datetime.timedelta(days=7)
    elif mode == 'monthly':
        return partial_end.replace(day=1) - datetime.timedelta(days=1)
    elif mode == 'interval':
        return partial_end - datetime.timedelta(days=days)


if __name__ == '__main__':
    crawl_query_by_unit(query='삼성전자',
                        begin=datetime.datetime(2020, 10, 3),
                        end=datetime.datetime(2020, 11, 19),
                        save_dir='test',
                        mode='monthly')


