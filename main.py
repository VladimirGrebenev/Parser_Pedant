from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
import csv

brand = 'iPhone'
reduce = 2 # показатель на который уменьшаем прайс

def get_data_BS():
    # # инициализация работы браузера
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # driver = webdriver.Chrome(options=options)
    # # выбираем город Москва
    # driver.get('https://pedant.ru/?townid=1')
    # # переходим на страницу с прайсом определённой модели айфона
    # driver.get('https://pedant.ru/remont-apple/iphone/pr-razbilos-ili-potsarapolos-steklo?object=' + model)
    # # парсинг страницы
    # pageSource = driver.page_source
    # bsObj = BeautifulSoup(pageSource, 'lxml')
    #
    # return bsObj
    pass



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

    print('Модельный ряд для парсинга: ')
    for model in models:
        print(model)

    # # для текстирования функций создал короткий список моделей
    # models = {
    #     'x',
    #
    # }

    return models

# функция парсинга прайса со страницы определённой модели
def parse_price():

    price = [] # создаём наш главный словарь price

    models = parse_phone_models()

    #перебираем модели и парсим их страницы
    for model in models:

        print('парсим модель: ' + model)

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

            # добавляем услуги в прайс и делим цену на значение reduce
            try:
                price.append({
                    'brand': brand,
                    'service': cols[0].text.replace('\n                    \n\n                + ', ' +').replace(
                        '\n                    \nNEW', '').strip(),
                    'gadjet': (brand + ' ' + model),
                    'fix_time': cols[2].text.strip(),
                    'price_key': int(int(cols[3].text.replace(' ', '').replace('р.', '').replace('от', '').strip(

                    ))/reduce),
                })
            # на случай если значение не число, а строка
            except Exception:
                price.append({
                    'brand': brand,
                    'service': cols[0].text.replace('\n                    \n\n                + ', ' +').replace(
                        '\n                    \nNEW', '').strip(),
                    'gadjet': (brand + ' ' + model),
                    'fix_time': cols[2].text.strip(),
                    'price_key': cols[3].text.strip(),
                })

        print(model + ' в базе')

    # избавляемся от лишних цен по акции
    for servise in price:
        if 'акция' in str(servise['price_key']):
            value = str(servise['price_key'])
            value = value.split(' р.')
            new_value = value[0].replace(' ', '').replace('от', '')
            servise['price_key'] = int(int(new_value)/reduce)


    return price

def save(price, path):
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Брэнд', 'Услуга', 'Модель', 'Время ремонта', 'Цена под ключ'))
        writer.writerows(
            (service['brand'], service['service'], service['gadjet'], service['fix_time'],
                          service['price_key']) for service in price)

def main():

    price = []
    price.extend(parse_price())
    save(price, 'price_iphone.csv')
    print('прайс сохранён')

if __name__ == '__main__':
    main()