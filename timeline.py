# -*- coding: utf-8 -*-
from datetime import datetime
from lxml.html import fromstring, tostring
from subprocess import check_output

URL = 'https://wiki.spodeli.org/%D0%92%D0%B0%D0%B6%D0%BD%D0%B8_%D0%BD%D0%B0%D1%81%D1%82%D0%B0%D0%BD%D0%B8_%D0%B7%D0%B0_%D1%81%D0%BB%D0%BE%D0%B1%D0%BE%D0%B4%D0%BD%D0%B8%D0%BE%D1%82_%D1%81%D0%BE%D1%84%D1%82%D0%B2%D0%B5%D1%80_%D0%B2%D0%BE_%D0%A0%D0%B5%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0_%D0%9C%D0%B0%D0%BA%D0%B5%D0%B4%D0%BE%D0%BD%D0%B8%D1%98%D0%B0'

MONTHS = [u'јануари', u'февруари', u'март', u'април', u'мај', u'јуни', u'јули',
          u'август', u'септември', u'октомври', u'ноември', u'декември']

def crawl():
    """Crawl the wiki-timeline page and parse data"""
    content = check_output(['curl', URL])

    doc = fromstring(content.decode('utf-8'))
    content = doc.cssselect("div#mw-content-text")[0]
    del doc

    content.remove(content.cssselect("table#toc")[0])
    for el in content.cssselect("h2"):
        content.remove(el)

    # parse data
    cur_date = ''

    skip = True # skip until you get time header

    for el in content:
        if not skip and el.tag=='p':
            yield cur_date, el

        elif el.tag=='h3':
            skip = False
            el_span = el.cssselect('span[id]')[0]
            cur_date = el_span.text.strip()

def process_date(data):
    """Process human dates to machine readable dates"""
    for date, el in data:
        if date.endswith(u'година'):
            date = date[:-6].strip()
        date = date.lower()
        display_date = date
        for i, month in enumerate(MONTHS):
            if month in date:
                date = date.replace(month, str(i))
                break
        try:
            date = datetime.strptime(date, '%d %m %Y').strftime('%Y-%m-%d')
        except Exception:
            try:
                date = datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')
            except Exception:
                date = ''

        yield date, display_date, el

def output(data, keep_empty_date=False):
    """Write output to csv,
       set keep_empty_date to include the invalid date entries"""
    with open('timeline.csv', 'w') as f:
        f.write('date,display_date,description,link,series,html\n')
        for date, display_date, el in data:
            if keep_empty_date or date!='':
                #text = el.text_content().replace('"', u'“').replace('\n',' ').strip()
                html = tostring(el).replace('\n',' ').replace('"','""').strip()
                #if text=='': continue
                line = '"%s",%s,,,,"%s"\n' % (date,
                                              display_date.encode('ascii', 'xmlcharrefreplace'),
                                              html.encode('utf-8'))
                f.write(line)

def main():
    data = crawl()
    data = process_date(data)
    output(data, keep_empty_date=False)

main()
