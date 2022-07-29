import scrapy


class DotabuffSpider(scrapy.Spider):
    name = 'dotabuff'
    allowed_domains = ['dotabuff.com']
    start_urls = ['https://www.dotabuff.com/heroes']

    def start_requests(self):
        pages = ['anti-mage', 'meepo', 'lone-druid', 'tiny', 'slardar', 'legion-commander', 'phantom-assassin', 'troll-warlord',
        'monkey-king', 'riki', 'templar-assassin', 'io', 'kunkka', 'huskar', 'axe', 'bloodseeker', 'earthshaker',
        'shadow-fiend', 'night-stalker', 'enchantress', 'drow-ranger', 'sven', 'terrorblade', 'hoodwink', 'puck',
        'dawnbreaker', 'elder-titan', 'lina', 'luna', 'spirit-breaker', 'ursa', 'naga-siren', 'disruptor', 'alchemist',
        'shadow-shaman', 'magnus', 'slark', 'earth-spirit', 'crystal-maiden', 'beastmaster', 'tusk', 'nyx-assassin',
        'snapfire', 'lycan', 'broodmother', 'ember-spirit', 'clinkz', 'viper', 'jakiro', 'chen', 'dazzle', 'natures-prophet',
        'outworld-destroyer', 'centaur-warrunner', 'grimstroke', 'silencer', 'lion', 'dragon-knight', 'invoker', 
        'keeper-of-the-light', 'mirana', 'weaver', 'bane', 'windranger', 'bounty-hunter', 'shadow-demon', 'warlock',
        'witch-doctor', 'doom', 'visage', 'pangolier', 'lifestealer', 'rubick', 'phoenix', 'vengeful-spirit', 'gyrocopter',
        'tidehunter', 'leshrac', 'chaos-knight', 'mars', 'faceless-void','timbersaw', 'dark-willow', 'treant-protector',
        'marci', 'pudge', 'dark-seer', 'queen-of-pain', 'sniper', 'venomancer', 'abaddon', 'enigma', 'omniknight',
        'void-spirit', 'phantom-lancer', 'batrider', 'lich', 'bristleback', 'arc-warden', 'undying', 'razor', 'oracle',
        'underlord', 'death-prophet', 'ogre-magi', 'juggernaut', 'techies', 'skywrath-mage', 'clockwerk', 'spectre',
        'wraith-king', 'winter-wyvern', 'brewmaster', 'tinker', 'sand-king', 'morphling', 'necrophos', 'ancient-apparition',
        'pugna', 'storm-spirit', 'zeus', 'medusa', 'primal-beast']

        for hero in pages:
            url = f'https://www.dotabuff.com/heroes/{hero}/counters'
            yield scrapy.Request(url)

    def parse(self, response):
        item = {}
        hero = response.url
        item['Hero'] = hero[hero.find('heroes')+7:hero.rfind('/')]
        for tr in range(1, 123):
            hero = response.xpath(f'/html/body/div[2]/div[2]/div[3]/div[4]/section[3]/article/table/tbody/tr[{tr}]/td[2]/a/text()').get()
            disadvantage = response.xpath(f'/html/body/div[2]/div[2]/div[3]/div[4]/section[3]/article/table/tbody/tr[{tr}]/td[3]/text()').get()[:-1]
            item[hero] = float(disadvantage)
        return item
