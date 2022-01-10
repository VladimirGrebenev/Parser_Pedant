# попытка номер три
from selenium import webdriver
from bs4 import BeautifulSoup
import lxml

def get_data_BS():
    # инициализация работы браузера
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    # выбираем город Москва
    driver.get('https://pedant.ru/?townid=1')
    # переходим на страницу с прайсом определённой модели айфона
    driver.get('https://pedant.ru/remont-apple/iphone/pr-razbilos-ili-potsarapolos-steklo?object=' + model)
    # парсинг страницы
    pageSource = driver.page_source
    bsObj = BeautifulSoup(pageSource, 'lxml')

    return bsObj



# функция сбора моделей телефона
def parse_phone_models():

    # инициализация работы браузера
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    # выбираем город Москва
    driver.get('https://pedant.ru/?townid=1')
    # переходим на страницу с прайсом определённой модели айфона
    driver.get('https://pedant.ru/remont-apple/iphone/pr-razbilos-ili-potsarapolos-steklo?object=x')
    # парсинг страницы
    pageSource = driver.page_source
    bsObjModels = BeautifulSoup(pageSource, 'lxml')

    models_items = bsObjModels.find_all('ul', class_='hide-unactive-items-mobile')[1]

    models = []

    for model in models_items:
        models.append(
            model.text.replace(' ', '').casefold().strip().replace('iphone', '')
        )

    for model in models:
        print(model)

    return models

# фукция парсинга прайса со страницы определённой модели айфона
def parse_price():

    price = [] # создаём наш главный словарь price

    models = parse_phone_models()

    #перебираем модели и парсим их страницы
    for model in models:

        # инициализация работы браузера
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        # выбираем город Москва
        driver.get('https://pedant.ru/?townid=1')
        # переходим на страницу с прайсом определённой модели айфона
        driver.get('https://pedant.ru/remont-apple/iphone/pr-razbilos-ili-potsarapolos-steklo?object=' + model)
        # парсинг страницы
        pageSource = driver.page_source
        bsObjPrice = BeautifulSoup(pageSource, 'lxml')
        table = bsObjPrice.find('div', class_='tab-content').find('tbody')

        for row in table.find_all('tr'):
            cols = row.find_all('td')
            price.append({
                'service': cols[0].text.replace('\n                    \n\n                + ', ' +').replace(
                    '\n                    \nNEW', '').strip(),
                'gadjet': cols[1].text.strip(),
                'fix_time': cols[2].text.strip(),
                'price_key': int(cols[3].text.replace(' акция до 17 января', '').replace('р.', '').replace(' ','')
                                 .replace('от', '').replace('Бесплатно', '0').replace('Звоните,пишите.Скажемценуза'
                                                                                      '3мин.', '0').strip())/2,
                })

    for service in price:
        print(service)

def main():
    parse_price()
    # parse_phone_models()

if __name__ == '__main__':
    main()