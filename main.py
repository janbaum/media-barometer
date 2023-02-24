import time
import init
import requests
from datetime import datetime


# Create FeedParser-instance for every media
def get_feed(url, table, **kwargs):
    time.sleep(2)
    Feed = init.FeedParser(url=url, main_table=table)
    Feed.parse_feed(**kwargs)
    print('got feed for ' + table)


def do_html(main_table, tag_class, attributes):
    time.sleep(2)
    scr = init.Scraper(main_table)
    scr.add_author_and_tags(tag_class, attributes)
    print('scraped html for ' + main_table)


def do_faz():
    fz = init.Scraper('faz_main_table')
    fz.faz_scraper()
    print('scraped html for faz_main_table')


def do_ts():
    ts = init.Scraper('ts_main_table')
    ts.ts_scraper(tag_class='li', attributes={'class_': 'taglist__element'})
    ts.ts_scraper(tag_class='meta', attributes={'name': 'description'})
    print('scraped html for ts_main_table')


if __name__ == "__main__":
    time.sleep(1)
    # TODO take ressort out of link
    while True:
        try:
            get_feed('https://rss.sueddeutsche.de/app/service/rss/alles/index.rss?output=rss', 'sz_main_table')
            do_html(main_table='sz_main_table', tag_class='meta', attributes=[{'name': 'author'}, {'name': 'keywords'}])
            # TODO Author out of description,
            get_feed('https://www.tagesschau.de/xml/rss2/', 'ts_main_table')
            do_ts()
            get_feed('https://www.faz.net/rss/aktuell/', 'faz_main_table')
            do_html(main_table='faz_main_table', tag_class='meta', attributes=[{'name': 'author'}, {'name': 'keywords'}])
            do_faz()
            get_feed('http://taz.de/!p4608;rss/', 'taz_main_table')
            do_html(main_table='taz_main_table', tag_class='meta', attributes=[{'name': 'author'}, {'name': 'keywords'}])
            get_feed('https://www.spiegel.de/schlagzeilen/index.rss', 'sp_main_table')
            do_html(main_table='sp_main_table', tag_class='meta', attributes=[{'name': 'author'},
                                                                              {'name': 'news_keywords'}])
            # TODO author strip string
            get_feed('https://newsfeed.zeit.de/index', 'zo_main_table')
            do_html(main_table='zo_main_table', tag_class='meta', attributes=[{'property': 'article:author'},
                                                                              {'name': 'keywords'}])
            get_feed('https://www.jungewelt.de/feeds/newsticker.rss', 'jw_main_table')
            do_html(main_table='jw_main_table', tag_class='meta', attributes=[{'name': 'Author'}, {'name': 'keywords'}])
            get_feed('https://www.heise.de/rss/heise.rdf', 'heise_main_table')
            do_html(main_table='heise_main_table', tag_class='meta', attributes=[{'name': 'author'}, {'name': 'keywords'}])

            print('fall asleep at: ', datetime.now())
            time.sleep(1800)  # do work every one hour

        except requests.exceptions.RequestException as e:
            print('ConnectionError', e)
            time.sleep(5)
            continue
