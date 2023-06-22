from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

class Siteuri(ABC):
    def __init__(self, url):
        self.url = url
        self.titlu = ""
        self.magazin = ""
        self.pret = 0.0
        self.set_titlu_pret()

    def get_url(self):
        return self.url

    def get_titlu(self):
        return self.titlu

    def get_pret(self):
        return self.pret

    def get_magazin(self):
        return self.magazin
    @abstractmethod
    def set_titlu_pret(self):
        pass


class Emag(Siteuri):
    def __init__(self, url):
        super().__init__(url)
        self.magazin = "Emag"

    def set_titlu_pret(self):
        page = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        title_element = soup.find(class_="page-title")
        if title_element:
            self.titlu = title_element.get_text().strip()
        else:
            print("Nu s-a putut găsi titlul produsului.")

        price_element = soup.find(class_="product-new-price has-deal")
        if price_element == None:
            price_element = soup.find(class_="product-new-price")
        if price_element:
            self.pret = price_element.get_text()
            self.pret = float(self.pret[0:5].replace(".", ""))
        else:
            print("Nu s-a putut găsi prețul produsului.")


class Altex(Siteuri):
    def __init__(self, url):
        super().__init__(url)
        self.magazin = "Altex"

    def set_titlu_pret(self):
        page = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        title_elements = soup.find_all(class_="jsx-8f410c0b503f5d3f")
        if len(title_elements) >= 2:
            self.titlu = title_elements[2].get_text().strip()
        else:
            print("Nu s-a putut găsi titlul produsului.")

        price_element = soup.find(class_="Price-int leading-none")
        if price_element:
            self.pret = price_element.get_text()
            self.pret = float(self.pret[0:5].replace(".", ""))
        else:
            print("Nu s-a putut găsi prețul produsului.")