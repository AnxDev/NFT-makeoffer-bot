from concurrent.futures import thread
from multiprocessing.connection import wait
from py import process

from seleniumwire import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys as key
import sys
from colorama import Fore, Style, init, Back
# import chrome settings from selenium.webdriver.chrome.options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from threading import Thread
def wait_for_element(driver, by, value, timeout=10):
       WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (by, value)
            )
        )

def open_metamask(driver, numberofwindows,index= 0):
    global hasToContinue
    wait_for_element(driver, By.CLASS_NAME, "elements__StyledListItem-sc-197zmwo-0")
    metamasklist = driver.find_elements_by_class_name("elements__StyledListItem-sc-197zmwo-0")[index]
    metamasklist.click()
    time.sleep(3)
    while True:
        try:
            driver.switch_to.window(driver.window_handles[2])
            break
        except:
            pass
    if "https://opensea.io/login?" in driver.current_url:
        driver.get("https://opensea.io/login?referrer=%2Faccount")
        open_metamask(driver, numberofwindows, index= 0)        
    else:
        wait_for_element(driver, By.ID, "password")



def makeoffer(driver):
    global offer_value, expiration_date, hasToContinue
    time.sleep(1)
    wait_for_element(driver, By.CLASS_NAME, "dpXlkZ")
    if driver.find_elements_by_class_name("dpXlkZ")[0].text.split("\n")[1].lower() == "Buy now".lower():
        offerbutton = driver.find_elements_by_class_name("InlineFlexreact__InlineFlex-sc-9jbsog-0")[1]
    else:
        if driver.find_elements_by_class_name("InlineFlexreact__InlineFlex-sc-9jbsog-0")[0].text.split("\n")[1].lower() == "Place Bid".lower():
            hasToContinue = True
            return
        offerbutton = driver.find_element_by_class_name("dpXlkZ")
    offerbutton.click()
    wait_for_element(driver, By.CLASS_NAME, "Input--input")
    offerinput = driver.find_element_by_class_name("Input--input")
    offerinput.send_keys(offer_value)
    time.sleep(1)
    print("-" * 50 + "\n" + element for element in driver.find_elements_by_class_name("Inputreact__StyledContainer-sc-3dr67n-0"))
    driver.find_element_by_xpath("//div[@class='Blockreact__Block-sc-1xf18x6-0 jqNBiE']").click()
    wait_for_element(driver, By.CLASS_NAME, "Inputreact__StyledContainer-sc-3dr67n-0")
    
    driver.find_element_by_class_name("elements__StyledListItem-sc-197zmwo-0").click()
    wait_for_element(driver, By.CLASS_NAME, "cTtDsd")
    time_input = driver.find_element_by_xpath("//input[@type='time']")
    time_input.send_keys(expiration_date)
    wait_for_element(driver, By.CLASS_NAME, "jwQUoq")
    
    makeofferButton = driver.find_element_by_class_name("jwQUoq")
    makeofferButton.click()
    time.sleep(2)
    while True:
        try:
            driver.switch_to.window(driver.window_handles[2])
            break
        except:
            time.sleep(1)
    wait_for_element(driver, By.CLASS_NAME, "signature-request-message__scroll-button")
    driver.find_element_by_class_name("signature-request-message__scroll-button").click()
    wait_for_element(driver, By.CLASS_NAME, "btn-primary")
    driver.find_element_by_class_name("btn-primary").click()

def doCollection(site):
    global Options
    options = Options()
    options.add_extension("MetaMask.crx")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome("chromedriver.exe", options=options, service_log_path='NUL')

    a = input("Quando hai fatto l'accesso a MetaMask e lo hai collegato a opensea, premi invio")
    print("Se vuoi ARRESTARE il programma, premi CTRL+C.\nSe escono scritte che non sono errori, non preoccuparti. In caso contrario, contatta il dev.")
    
    #log_in(driver, site)

    driver.get(site + "?search[sortAscending]=true&search[sortBy]=CREATED_DATE")

    items = driver.find_element_by_class_name("kejuyj").text
    items = int(items.replace(".", "").replace(" ", "").replace("items", ""))

    col_input = driver.find_element_by_xpath("//input[@placeholder='Search by name or trait']")
    #Assetreact__AssetCard-sc-bnjqwy-2
    hasToContinue = False
    print(len(driver.find_elements_by_class_name("fXFHnS")))
    for i in range(items):
        if i == 0:
            item = driver.find_elements_by_class_name("Assetreact__AssetCard-sc-bnjqwy-2")[0]
            item.click()
            time.sleep(4)
            url = driver.current_url
            makeoffer(driver)
            if hasToContinue:
                hasToContinue = False
                continue
        else:
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url + f"{i}")
            makeoffer(driver)
            if hasToContinue:
                continue

    
init()
def main():
    
    global password, secret_phrase, offer_value, expiration_date, hasToContinue
    print(Back.WHITE + Fore.BLACK)
    sites = []
    number_of_threads = int(input("Quante collezioni vuoi fare contemporaneamente?: "))
    for i in range(0,number_of_threads):
        site = input("Inserisci i link delle collezioni di opensea da visitare (es. https://opensea.io/collection/the-lunartics): ")
        sites.append(site)
    sites = [site.replace("http://", "https://").replace(" ", "").replace("www.", "") for site in sites]
    for site in sites:
        if "https://opensea.io/collection/" not in site.lower():
            print(Back.WHITE + Fore.RED + "I link che hai scritto non sono validi, riprova.")
            main()
    print(sites)
    print(Back.WHITE + Fore.BLACK)
    if input("Hai scritto i link correttamente? [SI / NO]: ").lower() == "si":
        pass
    else:
        main()
    offer_value = input("Inserisci il valore dell'offerta (es. 0.000000000000000001): ")
    print( Back.BLACK + Fore.RED)
    if input( "! ATTENZIONE ! Sicuro di aver scritto il prezzo corretto? [SI / NO]: ").lower() == "si":
        pass
    else:
        offer_value = input("Inserisci il valore dell'offerta (es. 0.000000000000000001): ")
    print(Back.WHITE + Fore.BLACK)
    
    expiration_date = input("Inserisci l'ora di scadenza con i minuti dell'offerta (es. 16:04): ")
    expiration_date = expiration_date.split(":")
    
    print("Fai l'accesso a MetaMask e collegalo con opensea.")
    threads = []
    thread1 = Thread(target=doCollection, args=(sites[0],))
    thread2 = Thread(target=doCollection, args=(sites[1],))
    thread1.start()
    thread2.start()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nArresto...")
        sys.exit()
        