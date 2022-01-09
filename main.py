# попытка номер три
from selenium import webdriver
from bs4 import BeautifulSoup
import lxml

models = {
    '8',
    'x',
}

def parse_price():
    price = []

    for model in models:

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get('https://pedant.ru/?townid=1')
        driver.get('https://pedant.ru/remont-apple/iphone/pr-razbilos-ili-potsarapolos-steklo?object=' + model)

        pageSource = driver.page_source
        bsObj = BeautifulSoup(pageSource, 'lxml')
        table =bsObj.find('div', class_='tab-content').find('tbody')



        for row in table.find_all('tr'):
            cols = row.find_all('td')

            # print(cols[0].text.strip())


            price.append({
                'service': cols[0].text.strip(),
                'gadjet': cols[1].text.strip(),
                'fix_time': cols[2].text.strip(),
                'price_key': cols[3].text.strip(),
                })

    for service in price:
        print(service)

def main():
    parse_price()

if __name__ == '__main__':
    main()