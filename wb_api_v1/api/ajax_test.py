
class Params:

    filters = 'filters='
    fsupplierAll = filters + 'fsupplier'
    fbrandAll = filters + 'fbrand'

    sort = 'sort='
    popular = sort + 'popular'
    rate = sort +'rate'
    priceup = sort + 'priceup'
    pricedown = sort + 'pricedown'
    newly = sort + 'newly'
    benefit = sort + 'benefit'

    fbrand = 'fbrand'
    fsupplier = 'fsupplier'
    xsubject = 'xsubject'
    fdlvr = 'fdlvr'
    discount = 'discount'
    priceU = 'priceU'
    fcolor = 'fcolor'
    fsize = 'fsize'

    def setfbrand(self, *brandId):
        for arg in brandId:
            self.fbrand += arg + ';'
        self.fbrand = self.fbrand[:len(self.fbrand) - 1]

    def setfsupplier(self, *supplierId):
        for arg in supplierId:
            self.fsupplier += arg + ';'
        self.fsupplier = self.fsupplier[:len(self.fsupplier) - 1]

    #any param
    def setFilter(self, param, *args):
        param += '='
        for arg in args:
            param += f'{arg};'
        param = param[:len(param) - 1]
        return param

if __name__ == '__main__':
    params = Params()
    # print(params.setFilter('sort', 'rate'))
    params.setfbrand('101907', '199400')
    # print(params.fbrand)

    # Фильтры на странице с категорией!
    # Верхняя колонка! можно передать только по одному типу каждого параметра + фильтры слева
    # filters=fsupplier (показать всех продавцов)
    # filters=fbrand (показать все бренды)
    # sort=popular (по популярности)
    # sort=rate (по рейтингу)
    # sort=priceup (по цене - сначала дешевые)
    # sort=pricedown (по цене - сначала дорогие)
    # sort=newly (по обновлению)
    # sort=benefit (сначала выгодные)

    # Колонка слева!
    # fbrand=101907 id бренда несколько через ;
    # fsupplier=-100 id продавца несколько через ;
    # xsubject=41;184 id подкатегории несколько через ;
    # fdlvr=25 (срок доставки 25 - 1 день/ 49 - 2 дня / 73 - до 3х дней / 121 - до 5 дней) только одно
    # discount=10 (скидка 10 - от 10 процентов 30;50) - только одно
    # priceU=199400;219400 по цене от и до 1994 до 2194
    # fcolor=16761035 id цвета несколько через ;
    # fsize=35440 id размера несколько через ;

    # Верхняя колонка! можно передать только по одному типу каждого параметра
    params = {'filters=': '',
              'fbrand': '',
              'fsupplier': '',
              'xsubject': '',
              'fdlvr': '',
              'discount': '',
              'priceU': '',
              'fcolor': '',
              'fsize': ''}

if __name__ == '__main__':

    print()