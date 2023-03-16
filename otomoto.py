import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import re


class Otomoto:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.page_num = None
        self.xpath_dict = self.XPathDict()
        self.xpath_dict_highlighted = self.XPathDictH()
        self.data_columns = ['name', 'price', 'year', 'mileage', 'localization', 'engine_capacity']
        self.df = pd.DataFrame(columns=self.data_columns, index=[])

    def getDriver(self, page_num):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url.format(page_num=page_num))

    def getIds(self):
        ids_list = []
        ids = self.driver.find_elements("xpath", '//*[@id]')
        for ii in ids:
            if ii.tag_name == 'article' and len(re.findall(r'\d{10}', ii.get_attribute('id'))) > 0:
                if ii.get_attribute('data-highlight') == "true":
                    data_highlight = True
                else:
                    data_highlight = False
                try:
                    ids_list.append((int(ii.get_attribute('id')), data_highlight))
                except:
                    None
        print(ids_list)
        return ids_list

    def XPathDict(self):
        xpathdict = {'name': '//*[@id="{i_d}"]/div[1]/h2/a'
            , 'price': '//*[@id="{i_d}"]/div[3]/div/span'
            , 'year': '//*[@id="{i_d}"]/div[1]/div/ul/li[1]'
            , 'mileage': '//*[@id="{i_d}"]/div[1]/div/ul/li[2]'
            , 'localization': '//*[@id="{i_d}"]/div[1]/ul/li[1]/span/span'
            , 'engine_capacity': '//*[@id="{i_d}"]/div[1]/div/ul/li[3]'
                     }
        return xpathdict

    def XPathDictH(self):
        xpathdict = {'name': '//*[@id="{i_d}"]/div[1]/h2/a'
            , 'price': '//*[@id="{i_d}"]/div[4]/div/span'
            , 'year': '//*[@id="{i_d}"]/div[1]/div/ul/li[1]'
            , 'mileage': '//*[@id="{i_d}"]/div[1]/div/ul/li[2]'
            , 'localization': '//*[@id="{i_d}"]/div[1]/ul/li[1]/span/span'
            , 'engine_capacity': '//*[@id="{i_d}"]/div[1]/div/ul/li[3]'
                     }
        return xpathdict

    def getXPathData(self, xpath, i_d):
        try:
            return self.driver.find_element("xpath", xpath.format(i_d=i_d)).text
        except:
            return None

    def getAllData(self):
        for i_d, data_highlight in self.getIds():
            data = []
            if data_highlight:
                for xpath in self.xpath_dict_highlighted:
                    data.append(self.getXPathData(xpath=self.xpath_dict_highlighted[xpath], i_d=i_d))
            else:
                for xpath in self.xpath_dict:
                    data.append(self.getXPathData(xpath=self.xpath_dict[xpath], i_d=i_d))

            if any(data):  # checks to see if the list data has all 'None' values
                self.df = self.df.append(pd.Series(data, index=self.data_columns), ignore_index=True)

    def getAllPagesData(self, max_page, delay=20):
        for page_num in range(1, max_page):
            print(f"page number = {page_num}")
            self.getDriver(page_num=page_num)
            self.getAllData()
            WebDriverWait(self.driver, delay)
            self.driver.close()
