from bs4 import BeautifulSoup
import requests
from config import domen, request_params
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
            self.characteristics_url = domen + link['href']
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
        specs_dict = {}
        for spec in specs:
            key = spec.dt.text
            value = spec.dd.text
            specs_dict[key] = value

        return specs_dict


# parser = PageParser()
# characteristics_soup = parser.parse_characteristics('https://market.yandex.ru/product--otparivatel-xiaomi-mijia-handheld-ironing-machine-mjgtj01lf/890989735?nid=82866&show-uid=17000598762990496268616017&context=search&text=%D0%B1%D1%8B%D1%82%D0%BE%D0%B2%D0%B0%D1%8F%20%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0&uniqueId=1241766&own-cards=1241766%3A102020884861&sku=102020884861&cpc=fCq2T0FnbyytR5wDkMsAjW2v9JqKTiGlICZ0CYydPLw83nLic_SUxTctG1qkmGHZKG1dPZjNJlExT0R3NoqwCNHWv3R-w_yLAD4P1uMxNvZamhn3GoRnWx3hSrh_cwlfhm7xZ9lNLHvDWYWPSzzpyqWAlh309GhSTMjBydtng--ay83UMpXXgjAY2ZmgYH6X5nbVI_lNze9nEMAgLt1brSCIsrxINNRQTTEM8N63sVeNSZ2NKN-Mco5rPL7f9nl7a1jX_3L7g97YZS89DHECCg%2C%2C&do-waremd5=9GMvrnbkcjWoX4wJQwodvw&sponsored=1&rs=eJw9jy1oQlEcxe_TNDCIoEtzNy4YhsGiz12LdYsWYWEzCesGeQwWxH2YZ3m4ZlJBmA_f8xb7fc22V4wDizbBd06w_Dgczj3_c4uj5IP1bV2ZadgPX01gZmYSfslYzsM345tf45nJ2hIyb8d8LIOqVIbu-eA1qC6q0Ef6H3TelzF1mv6mgoZb-ln29OEID3QHcEQOdMZke3nucZrIRIq3qqBs4YoO2JPgnjnzO1D9I6-eVujMIO8W6Pxww7MHvefbP-45LOBv4eg7Lumw0yZv6DvUl2DUpU7hrZ6y8553M9xpgzrP5TUmJbQoBPCH_G-D1z-ZrLNHMLNAT7Rmzwhaurz44p8AYvaY3g%2C%2C')
# #characteristics_soup = parser.parse_characteristics('https://market.yandex.ru/product--morozhenitsa-kitfort-kt-1809/675051003?nid=54939&show-uid=17000598762990496268616015&context=search&text=%D0%B1%D1%8B%D1%82%D0%BE%D0%B2%D0%B0%D1%8F%20%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0&uniqueId=920840&own-cards=920840%3A100972425731&sku=100972425731&cpc=fCq2T0Fnbyw5WrRkefyTll36j5E34kvphVmvNy3imciBiS31ENbUrv6OYh8glaAGT3l2hO2ducnYDHPtFw8LGnFYt4SuDozOE-NUmbhrPIRQZ2L_b2R9oEB8w7LH66ZCdt0ppsTkghb8vvAXVDnh67fAr7KkleMz-HFiNolq0f0ylgc13_HslxXi_PiUlFQGYHJfRZ4RuZVBKnfdl587OI-PT7chJwRObyT6oNjPUU3zDwDYTqlfirrQy69cSv2e6g4ukyKrputAQYrbPRbBRw%2C%2C&do-waremd5=qf44bI0W1n6_fY7cxblGDA&sponsored=1&rs=eJw9jy1oQlEcxe_TNDCIoEtzNy4YhsGiz12LdYsWYWEzCesGeQwWxH2YZ3m4ZlJBmA_f8xb7fc22V4wDizbBd06w_Dgczj3_c4uj5IP1bV2ZadgPX01gZmYSfslYzsM345tf45nJ2hIyb8d8LIOqVIbu-eA1qC6q0Ef6H3TelzF1mv6mgoZb-ln29OEID3QHcEQOdMZke3nucZrIRIq3qqBs4YoO2JPgnjnzO1D9I6-eVujMIO8W6Pxww7MHvefbP-45LOBv4eg7Lumw0yZv6DvUl2DUpU7hrZ6y8553M9xpgzrP5TUmJbQoBPCH_G-D1z-ZrLNHMLNAT7Rmzwhaurz44p8AYvaY3g%2C%2C')
#
# print(characteristics_soup)
