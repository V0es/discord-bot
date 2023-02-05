import unittest
import string, random
from bot import DiscordBot

test_method = DiscordBot._parse_news_args


news_categories = {
    'business' : 'бизнес',
    'entertainment' : 'развлечения',
    'general' : 'общие',
    'health' : 'здоровье',
    'science' : 'наука',
    'sports' : 'спорт',
    'technology' : 'технологии',
}



def _parse_news_args(news_args : str):
        arg_list = news_args.split(':')
        news_args = {
            'category' : None,
            'keyword' : None,
            'num' : None
        }
        
        if not len(arg_list):
            return None
        for arg in arg_list:

            if arg in news_categories.keys():
                news_args['category'] = arg
                continue
            
            else:
                try:
                    arg = int(arg)
                    news_args['num'] = str(arg)
                    continue
                except ValueError:
                    news_args['keyword'] = arg
                    continue
        return news_args

class ParseNewsTest(unittest.TestCase):
       
    def test_parse(self):
        for i in range(100):
            test_str = ''
            category = random.choice(list(news_categories.keys()))
            keyword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            number = str(random.randint(0, 100))
            test_str += category + ':' + keyword + ':' + number
            self.assertEqual(test_method(test_str), {'category' : category, 'keyword' : keyword, 'num' : number})
    

    def test_parse_nocategory(self):
        for i in range(100):
            test_str = ''
            keyword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            number = str(random.randint(0, 100))
            test_str += keyword + ':' + number
            self.assertEqual(test_method(test_str), {'category' : None, 'keyword' : keyword, 'num' : number})


    def test_parse_nokeyword(self):
        for i in range(1000):
            test_str = ''
            category = random.choice(list(news_categories.keys()))
            number = str(random.randint(0, 100))
            test_str += category + ':' + number
            self.assertEqual(test_method(test_str), {'category' : category, 'keyword' : None, 'num' : number})


    def test_parse_nonumber(self):
        for i in range(1000):
            test_str = ''
            category = random.choice(list(news_categories.keys()))
            keyword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            test_str += category + ':' + keyword
            self.assertEqual(test_method(test_str), {'category' : category, 'keyword' : keyword, 'num' : None})


    def test_parse_only_category(self):
        for i in range(1000):
            test_str = ''
            category = random.choice(list(news_categories.keys()))
            test_str += category
            self.assertEqual(test_method(test_str), {'category' : category, 'keyword' : None, 'num' : None})


    def test_parse_only_keyword(self):
        for i in range(1000):
            test_str = ''
            keyword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            test_str += keyword
            self.assertEqual(test_method(test_str), {'category' : None, 'keyword' : keyword, 'num' : None})


    def test_parse_only_number(self):
        for i in range(1000):
            test_str = ''
            number = str(random.randint(0, 100))
            test_str += number
            self.assertEqual(test_method(test_str), {'category' : None, 'keyword' : None, 'num' : number})


    def test_parse_wrong_order(self):
        for i in range(1000):
            test_str = ''
            category = random.choice(list(news_categories.keys()))
            keyword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            number = str(random.randint(0, 100))
            
            lst = [category, keyword, number]
            random.shuffle(lst)

            test_str = ':'.join(lst)
            self.assertEqual(test_method(test_str), {'category' : category, 'keyword' : keyword, 'num' : number})
    

if __name__ == '__main__':
    unittest.main()



