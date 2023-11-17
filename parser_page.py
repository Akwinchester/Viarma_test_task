from bs4 import BeautifulSoup
import requests
from config import domain, request_params
from random import randint


class PageParser:
    """
    Класс для парсинга страницы
    """
    def load_page(self, url):
        """
        Метод для загрузки страницы по указанному url
        """
        params = request_params[randint(0,2)]
        response = requests.get(url, headers=params['headers'], cookies=params['cookies'] )
        return response.text

    def parse_page(self, page):
        """
        Метод для парсинга страницы с помощью BeautifulSoup
        """
        return BeautifulSoup(page, 'html.parser')

    def get_characteristics_link(self, url):
        """
        Метод для получения ссылки на страницу характеристик
        """
        page = self.load_page(url)
        soup = self.parse_page(page)

        link = soup.find('a', string='Все характеристики')
        if link:
            self.new_url = link
            self.characteristics_url = domain + link['href']
            return self.characteristics_url

    def load_characteristics_page(self, url):
        """
        Метод для загрузки страницы характеристик
        """
        characteristics_url = self.get_characteristics_link(url)
        if characteristics_url:
            return self.load_page(characteristics_url)

    def parse_characteristics(self, url):
        """
        Метод для парсинга характеристик со страницы
        """
        page = self.load_characteristics_page(url)
        if page:
            soup = self.parse_page(page)
            specs_block = soup.find('div', id='product-specs')
            specs = specs_block.find_all('dl', class_='sZB0N')

            return self.get_specs_dict(specs)

    def get_specs_dict(self, specs):
        """
        Метод для получения словаря характеристик
        """
        specs_dict = {'Страница с характеристиками':f'=HYPERLINK("{self.characteristics_url}","ссылка на характеристики")'}
        for spec in specs:
            key = spec.dt.text
            value = spec.dd.text
            specs_dict[key] = value

        return specs_dict
