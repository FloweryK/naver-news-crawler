import os
import argparse
import datetime
from dateutil.relativedelta import relativedelta
from query_crawler import crawl


def crawl_query_by_unit(query, save_dir, begin, end, mode, days=None):
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
        os.makedirs(os.path.join(save_dir, query), exist_ok=True)
        save_as = os.path.join(save_dir, query, query + '_' + partial_begin_str + '-' + partial_end_str + '.xlsx')

        if os.path.exists(save_as):
            print('\talready crawled. go to next step')
        else:
            crawl(query=query,
                  save_as=save_as,
                  begin=partial_begin_str,
                  end=partial_end_str)

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


def get_arguments():
    # Argument configuration
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, required=True, help='query to search on NAVER')
    parser.add_argument('--begin', type=str, required=True, help='crawling begin point (%%Y.%%m.%%d format)')
    parser.add_argument('--end', type=str, required=True, help='crawling end point (%%Y.%%m.%%d format)')
    parser.add_argument('--save_dir', type=str, default='test/', help='save directory')
    parser.add_argument('--mode', type=str, required=True)
    parser.add_argument('--days', type=int, default=7)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_arguments()

    query = args.query
    save_dir = args.save_dir
    begin = args.begin
    end = args.end
    mode = args.mode
    days = args.days

    crawl_query_by_unit(query=query,
                        save_dir=save_dir,
                        begin=datetime.datetime.strptime(begin, '%Y.%m.%d'),
                        end=datetime.datetime.strptime(end, '%Y.%m.%d'),
                        mode=mode,
                        days=days)


