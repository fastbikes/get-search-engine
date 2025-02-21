import datetime
from selenium import webdriver as webd
from utils.time_cost import TimeCost
from utils.log_utils import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class StockInfo:
    def __init__(self, stock_id, stock_name, driver):
        self.__driver = driver
        self.__id = stock_id
        self.__name = stock_name
        self.total_shares = ''
        self.circulating_shares = ''
        self.concept = ''
        self.price = 0
        self.PB = 0
        self.PE = 0
        self.zone = ''
        self.ipo_time = ''
        self.total_market_value = ''
        self.circulation_market_value = ''
        self.init_stock_info()

    def init_stock_info(self):
        try:
            self.__driver.get(f'http://stockpage.10jqka.com.cn/{self.__id}/')
            self.__driver.implicitly_wait(2)
            time_cost = TimeCost('采集总股本')
            time_cost.start()
            self.total_shares = self.get_total_shares()
            time_cost.end()

            time_cost = TimeCost('采集流通股本')
            time_cost.start()
            self.circulating_shares = self.get_circulating_shares()
            time_cost.end()

            time_cost = TimeCost('采集概念信息')
            time_cost.start()
            self.concept = self.get_concept()
            time_cost.end()

            time_cost = TimeCost('采集区域信息')
            time_cost.start()
            self.zone = self.get_zone()
            time_cost.end()

            time_cost = TimeCost('采集上市时间')
            time_cost.start()
            self.ipo_time = self.get_ipo_time()
            time_cost.end()

            time_cost = TimeCost('切换ifm')
            time_cost.start()
            self.__driver.switch_to.frame("ifm")
            time_cost.end()

            time_cost = TimeCost('采集当前价格')
            time_cost.start()
            self.price = self.get_current_price()
            time_cost.end()

            time_cost = TimeCost('采集PB')
            time_cost.start()
            self.PB = self.get_PB()
            time_cost.end()

            time_cost = TimeCost('采集PE')
            time_cost.start()
            self.PE = self.get_PE()
            time_cost.end()

            time_cost = TimeCost('采集总市值')
            time_cost.start()
            self.total_market_value = self.get_total_market_value()
            time_cost.end()

            time_cost = TimeCost('采集流通市值')
            time_cost.start()
            self.circulation_market_value = self.get_circulation_market_value()
            time_cost.end()
            self.__driver.switch_to.default_content()
        except Exception as e:
            logging.error(f'init stock info:{e}')

    # def save(self):
    #     try:
    #         stock_basic_info_list = []
    #         current_datetime = datetime.datetime.now()
    #         date_string = current_datetime.strftime("%Y-%m-%d")
    #         stock_info = get_stock_basic_info(self.__id)
    #         if len(stock_info) == 0:
    #             stock_basic_info_list.append(
    #                 (self.__id, date_string, self.PE, self.PB, self.total_market_value,
    #                  self.circulation_market_value, self.total_shares, self.circulating_shares,
    #                  self.concept, '', '', 0.0, 0.0, self.zone, self.ipo_time))
    #             add_stock_basic_info(stock_basic_info_list)
    #         else:
    #             if self.concept == '-' or len(self.zone) == 0 or len(self.concept) == 0 or len(self.ipo_time) == 0:
    #                 return
    #             logging.info(f'update {self.__id}: concept: {self.concept} zone: {self.zone} ipo_time:{self.ipo_time}')
    #             stock_basic_info_list.append((self.__id, self.concept, self.zone, self.ipo_time))
    #             update_stock_concept_zone(stock_basic_info_list)
    #
    #     except Exception as e:
    #         logging.error(f'stock_info save:{self.__id}:{e}')

    def get_PE(self):
        pe_path = '//*[@id="fvaluep"]'
        pe = 0
        try:
            pe_nodes = self.__driver.find_elements_by_xpath(pe_path)
            if len(pe_nodes) > 0 and pe_nodes[0].text != '亏损' and pe_nodes[0].text != '--':
                pe = float(pe_nodes[0].text)
        except Exception as e:
            logging.error(f'get_PE:{self.__id}:{e}')
            pe = 0
        return pe

    def get_PB(self):
        pb_path = '//*[@id="tvaluep"]'
        pb = 0
        try:
            pb_nodes = self.__driver.find_elements_by_xpath(pb_path)
            if len(pb_nodes) > 0 and pb_nodes[0].text != '--':
                pb = float(pb_nodes[0].text)
        except Exception as e:
            logging.error(f'get_PB:{self.__id}:{e}')
            pb = 0
        return pb

    def get_zone(self):
        zone_path = '/html/body/div[9]/div[2]/div[3]/dl/dd[1]'
        zone = ''
        try:
            zone_nodes = self.__driver.find_elements_by_xpath(zone_path)
            if len(zone_nodes) > 0:
                zone = zone_nodes[0].text
        except Exception as e:
            logging.error(f'get_zone:{self.__id}:{e}')
            zone = ''
        return zone

    def get_ipo_time(self):
        ipo_time_path = '/html/body/div[9]/div[2]/div[3]/dl/dd[5]'
        ipo_time = ''
        try:
            ipo_times_nodes = self.__driver.find_elements_by_xpath(ipo_time_path)
            if len(ipo_times_nodes) > 0:
                ipo_time = ipo_times_nodes[0].text
        except Exception as e:
            logging.error(f'get_ipo_time:{self.__id}:{e}')
            ipo_time = ''
        return ipo_time

    def get_current_price(self):
        price_path = '//*[@id="quote_header"]/span'
        price = 0
        try:
            price_nodes = self.__driver.find_elements_by_xpath(price_path)
            if len(price_nodes) > 0 and price_nodes[0].text != '--':
                price = float(price_nodes[0].text)
        except Exception as e:
            logging.error(f'get_current_price:{self.__id}:{e}')
        return price

    def get_total_shares(self):
        total_shares_path = '/html/body/div[9]/div[2]/div[3]/dl/dd[14]'
        total_shares = '-'
        try:
            total_shares_nodes = self.__driver.find_elements_by_xpath(total_shares_path)
            if len(total_shares_nodes) > 0:
                total_shares = total_shares_nodes[0].text
            # logging.debug(f'total_shares:{total_shares}')
        except Exception as e:
            logging.error(f'get_total_shares:{self.__id}:{e}')
        return total_shares

    def get_circulating_shares(self):
        circulating_shares_path = '/html/body/div[9]/div[2]/div[3]/dl/dd[15]'
        circulating_shares = '-'
        try:
            circulating_shares_nodes = self.__driver.find_elements_by_xpath(circulating_shares_path)
            if len(circulating_shares_nodes) > 0:
                circulating_shares = circulating_shares_nodes[0].text
            # logging.debug(f'circulating_shares:{circulating_shares}')
        except Exception as e:
            logging.error(f'get_circulating_shares:{self.__id}:{e}')
        return circulating_shares

    def get_concept(self):
        concept_path = '/html/body/div[9]/div[2]/div[3]/dl/dd[2]'
        concept_value = '-'
        try:
            concept_nodes = self.__driver.find_elements_by_xpath(concept_path)
            if len(concept_nodes):
                concept_value = concept_nodes[0].get_attribute('title')
            # logging.debug(f'concept:{concept_value}')
        except Exception as e:
            logging.error(f'get_concept:{self.__id}:{e}')
        return concept_value

    def get_total_market_value(self):
        total_market_value_path = '//*[@id="tvalue"]'
        total_market_value = '-'
        try:
            total_market_value_nodes = self.__driver.find_elements_by_xpath(total_market_value_path)
            if len(total_market_value_nodes) > 0:
                total_market_value = total_market_value_nodes[0].text
            # logging.debug(f'total_market_value:{total_market_value}')
        except Exception as e:
            logging.error(f'get_total_market_value:{self.__id}:{e}')
        return total_market_value

    def get_circulation_market_value(self):
        circulation_market_value_path = '//*[@id="flowvalue"]'
        circulation_market_value = '-'
        try:
            circulation_market_value_nodes = self.__driver.find_elements_by_xpath(circulation_market_value_path)
            if len(circulation_market_value_nodes) > 0:
                circulation_market_value = circulation_market_value_nodes[0].text
            # logging.debug(f'circulation_market_value:{circulation_market_value}')
        except Exception as e:
            logging.error(f'get_circulation_market_value:{self.__id}:{e}')
        return circulation_market_value

if __name__ == '__main__':
    options = webd.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('log-level=3')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--shm-size=1g")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.3325.181 Safari/537.36")

    driver_path = ChromeDriverManager().install()
    # driver_path="C:\\Users\\Administrator\\.wdm\\drivers\\chromedriver\\win64\\128.0.6613.86\\chromedriver-win32\\chromedriver.exe"
    driver = webd.Chrome(executable_path=driver_path, options=options)
    stock_info = StockInfo("000001", "平安银行", driver)
    print('get_stock_info')