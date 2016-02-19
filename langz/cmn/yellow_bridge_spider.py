from robobrowser import RoboBrowser

TABLE_TITLES = {
    'English': 'definition',
    'See': 'see_also',
    'Traditional': 'traditional',
    'Pinyin': 'pinyin',
    'Cantonese': 'jyutping',
    'Effective': 'tone_sandhi',
    'Measure': 'quantifier',
    'Part': 'category',
}

class YellowBridgeSpider(object):
    def __init__(self, browser, query={}):
        self.browser = browser
        self.query = query

    def url(self):
        w = self.query['simplified']
        return "http://www.yellowbridge.com/chinese/dictionary.php?word=%s" % w

    def crawl(self):
        data = {}
        self.browser.open(self.url())

        data['simplified'] = self.browser.select('.mainDictChar')[0].text

        table = self.browser.select('#mainData tr')
        for tr in table:
            title, content = [td.text for td in tr.select('td')]
            for t, c in TABLE_TITLES.items():
                if title.startswith(t):
                    data[c] = content
                    break

        if data['traditional'].startswith('Same'):
            data['traditional'] = data['simplified']

        if data['tone_sandhi'].startswith('Same'):
            data['tone_sandhi'] = data['pinyin']

        if data['category']:
            data['category'] = data['category'][1]

        if 'quantifier' in data:
            data['quantifier'] = data['quantifier'].split(', ')
        else:
            data['quantifier'] = ['个']

        return data
