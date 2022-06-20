from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import concurrent.futures
import multiprocessing
import keyboard

class Product():
    products = {}
    products_prices = {}


def init():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(r'C:\chromedriver.exe', options=options)
    driver.get('https://orteil.dashnet.org/cookieclicker/')

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'cc_btn.cc_btn_accept_all'))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'langSelect-ES'))).click()

    sleep(2)

    with open('cookiegame.txt', 'r') as f:
        save = f.read()
        keyboard.press_and_release('control+o')
        sleep(1)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'textareaPrompt'))).send_keys(save)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'promptOption0'))).click()
        
    return driver

def click_cookie(driver):
    cookie = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'bigCookie')))
    while True: 
        if not keyboard.is_pressed('s'): cookie.click()
        else: break

def buy(driver):

    Product.products.update({'product0':WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'product0')))})
    Product.products.update({'product1':WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'product1')))})

    while True:
        if not keyboard.is_pressed('s'):
            try:
                cookies_amount = float(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cookies'))).text.replace(',','').replace('\ngalletas\npor', '').replace('\nmillion', '').split(' ')[0])
                print(cookies_amount)
                Product.products_prices.update({'product0':float(driver.find_element(By.ID, 'productPrice0').text.replace('million', '').replace(',',''))})
                Product.products_prices.update({'product1':float(driver.find_element(By.ID, 'productPrice1').text.replace('million', '').replace(',',''))})
            except Exception as e: print(e)

            try:
                for i in range(len(Product.products_prices)):

                    product = f'product{i}'
                    Product.products.get(product).click()
            except Exception as e: print()
            try:
                for i in range(2,19): 
                    product = driver.find_element(By.ID, f'product{i}')
                    Product.products.update({f'product{i}':product})
                    product_price = driver.find_element(By.ID, f'productPrice{i}').text.replace(',','')
                    if product_price.find('million') is not -1:
                        product_price = float(product_price.replace('million','')) * 10**6
                    elif product_price.find('billion') is not -1:
                        product_price = float(product_price.replace('billion','')) * 10**9
                    elif product_price.find('trillion') is not -1:
                        product_price = float(product_price.replace('trillion','')) * 10**14
                    else:
                        product_price = float(product_price)
                    Product.products_prices.update({f'product{i}':product_price})
                    current_upgrade = driver.find_element(By.ID, 'upgrade0')
                    current_upgrade.click()
            except Exception as e: print()
        else: 
            sleep(20)
            break


if __name__ == '__main__':
    multiprocessing.freeze_support()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        driver = init()
        f1 = executor.submit(click_cookie, driver)
        f2 = executor.submit(buy, driver)

        #while True:
        #    if keyboard.is_pressed('esc'): driver.quit()
        #    else: continue



