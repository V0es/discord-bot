import unittest
import string
import random
from src.bot import DiscordBot
from config.config import Config as cfg

test_method = DiscordBot._parse_news_args


class ParseNewsTest(unittest.TestCase):
       
    def test_parse(self):
        for _ in range(100):
            test_str = ''
            category = random.choice(list(cfg.news_categories.keys()))
            keyword = ''.join(random.choice(string.ascii_uppercase) + random.choice(string.digits) for _ in range(8))
            number = str(random.randint(0, 100))
            test_str += category + ':' + keyword + ':' + number
            self.assertEqual(test_method(test_str), {'category': cfg.news_categories[category], 'keyword': keyword,  'amount': number})

    def test_parse_nocategory(self):
        for _ in range(100):
            test_str = ''
            keyword = ''.join(random.choice(string.ascii_uppercase) + random.choice(string.digits) for _ in range(8))
            number = str(random.randint(0, 100))
            test_str += keyword + ':' + number
            self.assertEqual(test_method(test_str), {'category': None, 'keyword': keyword, 'amount': number})

    def test_parse_nokeyword(self):
        for _ in range(1000):
            test_str = ''
            category = random.choice(list(cfg.news_categories.keys()))
            number = str(random.randint(0, 100))
            test_str += category + ':' + number
            self.assertEqual(test_method(test_str), {'category': cfg.news_categories[category], 'keyword': None, 'amount': number})

    def test_parse_nonumber(self):
        for _ in range(1000):
            test_str = ''
            category = random.choice(list(cfg.news_categories.keys()))
            keyword = ''.join(random.choice(string.ascii_uppercase) + random.choice(string.digits) for _ in range(8))
            test_str += category + ':' + keyword
            self.assertEqual(test_method(test_str), {'category': cfg.news_categories[category], 'keyword': keyword, 'amount': None})

    def test_parse_only_category(self):
        for _ in range(1000):
            test_str = ''
            category = random.choice(list(cfg.news_categories.keys()))
            test_str += category
            self.assertEqual(test_method(test_str), {'category': cfg.news_categories[category], 'keyword': None, 'amount': None})

    def test_parse_only_keyword(self):
        for _ in range(1000):
            test_str = ''
            keyword = ''.join(random.choice(string.ascii_uppercase) + random.choice(string.digits) for _ in range(8))
            test_str += keyword
            self.assertEqual(test_method(test_str), {'category': None, 'keyword': keyword, 'amount': None})

    def test_parse_only_number(self):
        for _ in range(1000):
            test_str = ''
            number = str(random.randint(0, 100))
            test_str += number
            self.assertEqual(test_method(test_str), {'category': None, 'keyword': None, 'amount': number})

    def test_parse_wrong_order(self):
        for _ in range(1000):
            test_str = ''
            category = random.choice(list(cfg.news_categories.keys()))
            keyword = ''.join(random.choice(string.ascii_uppercase) + random.choice(string.digits) for _ in range(8))
            number = str(random.randint(0, 100))
            
            lst = [category, keyword, number]
            random.shuffle(lst)

            test_str = ':'.join(lst)
            self.assertEqual(test_method(test_str), {'category': cfg.news_categories[category], 'keyword': keyword, 'amount': number})
    

if __name__ == '__main__':
    unittest.main()
