import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def validate_elements(driver):
    elements = driver.find_elements(By.TAG_NAME, 'a')
    output = []
    for elem in elements:
        href = elem.get_attribute('href')
        if href and href.startswith("http"):
            output.append(href)
    return output

def crawl(url, method, options):

    driver = webdriver.Firefox(options=options)
    driver.get(url)

    time.sleep(3)

    myarray = validate_elements(driver)
    

    if(method == 1):
        # Method 1 (fastest)
        x=1;
        for href in myarray:
            driver.execute_script("window.open('"+href+"', '_blank');")
            driver.switch_to.window(driver.window_handles[x]) 
            time.sleep(1)
            x=x+1
    elif(method == 2):
        # Method 2 (best)
        for href in myarray:
            driver.execute_script("window.open('about:blank','"+href+"');")
            driver.switch_to.window(str(href)) 
            driver.get(href)

def main():
    #  Set browser options
    options = Options()
    options.set_preference("dom.disable_open_during_load", False)
    options.set_preference('dom.popup_maximum', -1)

    #  Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", default="https://alfiemills.co.uk", help="Desired URL to connect to the browser")
    parser.add_argument("-m", "--method", default=1, help="Method of crawling the site. [Default is 1 | 1 = fastest, 2 = best]", type=int)
    #  Validate arguments
    args = parser.parse_args()
    if (args.method > 2 or args.method < 1):
        raise ValueError("Invalid method")
    if(args.url.startswith("http") != True):
        raise ValueError("Invalid URL (Doesn't start with https)")


    crawl(args.url, args.method, options)

main()