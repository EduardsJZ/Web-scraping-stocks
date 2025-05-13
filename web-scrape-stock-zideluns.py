from selenium import webdriver
import yfinance as yf
import matplotlib.pyplot as plt
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
class HashTable:
    def __init__(self, capacity):   
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity
    
    def insert(self, key, value): 
        index = self._hash(key) 
    
        if self.table[index] is None: 
            self.table[index] = Node(key, value) 
            self.size += 1
        else: 
            current = self.table[index] 
            while current: 
                if current.key == key: 
                    current.value = value 
                    return
                current = current.next
            new_node = Node(key, value) 
            new_node.next = self.table[index] 
            self.table[index] = new_node 
            self.size += 1

    def __iter__(self):
        for current in self.table:
            if current is not None:
                yield(current.key, current.value)

class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price = None
        self.news = None
        self.currency = None

def get_news(symbol):
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--lang=en-US")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    url = f"https://finance.yahoo.com/quote/{symbol}/news"
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Noraidīt visu")]'))
            )
            cookie_button.click()
            # print("Cookies accepted.")
        except Exception:
            # print("No cookie popup found.")
            return None

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//ul/li/section/div/a/h3'))
        )

        news_elements = driver.find_elements(By.XPATH, '//ul/li/section/div/a/h3')
        news = []
        for element in news_elements:
            title = element.text
            link = element.find_element(By.XPATH, './..').get_attribute('href')  
            news.append({'title': title, 'link': link})

        news = news[:5]

        if not news:
            # print("Nav atrastas jaunākās ziņas.")
            return None
        # print("Jaunākās ziņas atrastas.")
        return news

    except Exception as e:
        # print(f"Kļūda, iegūstot jaunākās ziņas: {e}")
        return None

    finally:
        driver.quit()

def get_price(symbol):
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--lang=en-US")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Noraidīt visu")]'))
            )
            cookie_button.click()
            # print("Cookies accepted.")
        except Exception:
            # print("No cookie popup found.")
            return None

        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/div[1]/span'))
        )

        current_price = round(float(price_element.text.replace(',', '')), 2)
        currency_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[1]/span/span[3]'))
        )
        currency = currency_element.text.strip()
        # print(f"Atrasta cena: {current_price} {currency}")
        return current_price, currency

    except Exception as e:
        # print(f"Kļūda, iegūstot akcijas cenu: {e}")
        return None

    finally:
        driver.quit()
    
def convert_price(price):
    try:
        price = float(price)
        return round(price * USD_TO_EUR_RATE, 2)
    except ValueError:
        # print("Kļūda, konvertējot cenu:", price)
        return None
    
def get_usd_to_eur_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        response.raise_for_status()
        data = response.json()
        # print("Iegūts valūtas maiņas kurss:", data["rates"]["EUR"])
        return data["rates"]["EUR"]
    except Exception as e:
        # print("Kļūda, iegūstot valūtas maiņas kursu:", e)
        return 0

USD_TO_EUR_RATE = get_usd_to_eur_rate()    

def get_chart_eur(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d", interval="5m")  
        data['Close'] = data['Close'].apply(convert_price) 

        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label='Cena EUR')
        plt.title(f"{symbol} akciju cena pēdējās 24 stundās (EUR)")
        plt.xlabel("Laiks")
        plt.ylabel("Cena EUR")
        plt.legend()
        plt.grid()

        chart_filename = f"{symbol}_24h_chart.png"
        plt.savefig(chart_filename)
        plt.close()
        print(f"Akciju diagramma pēdējām 24 stundām saglabāta kā {chart_filename}")
    except Exception as e:
        print(f"Kļūda, iegūstot akciju diagrammu: {e}")

def check_if_exists(symbol):
    try:
        ticker = yf.Ticker(symbol)
        if 'symbol' in ticker.info and ticker.info['symbol'] == symbol:
            return True
        else:
            return False
    except Exception as e:
        # print(f"Kļūda, pārbaudot simbolu {symbol}: {e}")
        return False

Stocks = HashTable(100)
while True:
    print("\nIzvēlne:")
    print("1 - Ievadīt akciju")
    print("2 - Izvadīt")
    print("3 - Beigt")
    choice = input("Izvēlieties opciju: ")
    if choice == '1':
        symbol = input("Ievadiet akcijas simbolu: ").upper()
        if check_if_exists(symbol):
            current_stock = Stock(symbol)
            while True:
                print("\nIzvēlne:")
                print("1 - Cena")
                print("2 - Jaunākās ziņas")
                print("3 - Grafiks")
                print("4 - Saglabāt un Atgriezties")
                print("5 - Atcelt")
                sub_choice = input("Izvēlieties darbību: ").strip()
                match sub_choice:
                    case '1':
                        price, currency = get_price(symbol)
                        current_stock.price = price
                        current_stock.currency = currency
                        print("\nCena saglabāta")
                    case '2':
                        news = get_news(symbol)
                        current_stock.news = news
                        print("\nJaunākās ziņas saglabātas")
                    case '3':
                        get_chart_eur(symbol)
                    case '4':
                        Stocks.insert(symbol, current_stock)
                        print(f"\nAkcijas {symbol} dati saglabāti.")
                        break
                    case '5':
                        print("\nAtceltas darbības.")
                        break
                    case _:
                        print("\nNederīga izvēle.")
        else:
            print(f"Akcija {symbol} netika atrasta.")
    elif choice == '2':
        for stock in Stocks:
            print(f"\nAkcija: {stock[0]}")
            if stock[1].price is not None and stock[1].currency is not None:
                print(f"Cena: {stock[1].price} {stock[1].currency}")
            if stock[1].news: 
                print("Jaunākās ziņas:")
                for i, news_item in enumerate(stock[1].news, start=1):
                    print(f"  {i}. {news_item['title']}")
                    print(f"     Saite: {news_item['link']}")
    
    elif choice == '3':
        break

    else:
        print("\nNederīga izvēle")


