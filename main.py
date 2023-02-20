import time
import init


# Create FeedParser-instance for every media
def get_feed(url, table, **kwargs):
    time.sleep(2)
    Feed = init.FeedParser(url=url, main_table=table)
    Feed.parse_feed(**kwargs)
    print(table, 'inserted')


def do_html(main_table, tag_class, attributes):
    time.sleep(2)
    scr = init.Scraper(main_table)
    scr.add_author_and_tags(tag_class, attributes)


def do_faz():
    fz = init.Scraper('faz_main_table')
    fz.faz_scraper()


if __name__ == "__main__":
    time.sleep(1)
    while True:
        # try:
        # TODO AUTHOR!,  take ressort out of link
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
        break
        # time.sleep(1800)  # do work every one hour
        
        # TODO exepction for connection error
        # except socket.gaierror or ConnectionError or requests.exceptions.ConnectionError:
        #     print('ConnectionError')
        #     continue
