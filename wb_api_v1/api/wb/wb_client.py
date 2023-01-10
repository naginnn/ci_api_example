import requests as requests
from requests import Session

from automodel import BaseChild
class CategoryInfo:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class WbClient:

    def create_params(self):
        params = {
            'appType': 1,
            'curr': 'rub',
            'emp': 0,
            'lang': 'ru',
            'locale': "ru",
            'reg': 0,
            'spp': 0
        }
        session = Session().post('https://www.wildberries.ru/webapi/api/home/banners')
        params['couponsGeo'] = session.cookies.get('__cpns').replace('_', ',')
        params['dest'] = session.cookies.get('__dst').replace('_', ',')
        params['pricemarginCoeff'] = session.cookies.get('__pricemargin').replace('_', ',').replace('-', '')
        params['regions'] = session.cookies.get('__region').replace('_', ',')
        return params


    def get_child(self, params, parent_name, childs, subcategory=[]):
        for child in childs:
            category_name = child.get('name')
            childs = child.get('childs')
            if childs:
                self.get_child(params, parent_name + '|' + category_name, childs, subcategory)
            else:
                url = self.create_category_url(child, params)
                if not url:
                    continue
                    # try:
                    #     resp = requests.get(url)
                    #     if resp.status_code == 200:
                    #         resp = resp.json()
                    #         subcategory += [{parent_name: child, 'url': url, 'total': resp.get('data').get('total')}]
                    #         # print(resp)
                    #         print({parent_name: child, 'url': url, 'total': resp.get('data').get('total')})
                    # except:
                    #     pass
                subcategory += [{parent_name: child, 'url': url}]
                print({parent_name: child, 'url': url})
        return subcategory


    def get_categories(self, params):
        categories = requests.get('https://www.wildberries.ru/webapi/menu/main-menu-ru-ru.json').json()
        for category in categories:
            if category.get('childs'):
                all_categories = wb_client.get_child(params, category.get('name'), category.get('childs'))
        return all_categories

    def get_category_info(self, categories):
        for category in categories:
            resp = requests.get(category.get('url'))
            print(resp.json())

    def create_category_url(self, child, params, filter=None, ):
        shard = child.get('shard')
        query = child.get('query')
        if query and shard:
            for param in query.split('&'):
                if 'kind' in param or 'subject' in param:
                    param = param.split('=')
                    params[param[0]] = param[1]
            url = f'https://catalog.wb.ru/catalog/{shard}/v4/filters' \
                   + f'?{"filters=" + filter + "&" if filter else ""}' \
                   + '&'.join(["{}={}".format(k, v) for k, v in params.items()])
            return url
        return None



    def get_similar_queries(self):
        response = requests.get('https://similar-queries.wildberries.ru/catalog?url=/catalog/muzhchinam/odezhda/bryuki-i-shorty')
        return response.json()

#https://basket-03.wb.ru/vol387/part38709/38709879/info/ru/card.json
# 387/38709/38709879 can get it
# 3/5/brand_id
#/vol387/part38709/38709879/info/ru/card.json
#params

if __name__ == '__main__':
    wb_client = WbClient()
    params = wb_client.create_params()
    categories = wb_client.get_categories(params)
    # wb_client.get_category_info(categories)

