import sys
import time
import requests
from urllib.parse import urlencode,parse_qs,urlparse
import lxml.html
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

if __name__ == "__main__":
    target = "Fuji_list.txt"
    dist = target.split("_")[0]
    with open(target, "r") as f:
        order = f.readlines()
    s_order = set(order)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="./chromedriver",
                              options=options
                              )

    N=len(s_order)
    for k,l in enumerate(s_order,1):
        post_url = l[:-1]
        print(post_url,"({}/{})".format(k,N))

        post = driver.get(post_url)
        
        time.sleep(5)
        try:
            img_root = driver.find_element_by_id("react-root")
        except NoSuchElementException:
            print("*** oops! ***")
            continue
        
        imgs = img_root.find_elements_by_tag_name("img")

        i=1
        for img in imgs:
            try:
                s = img.get_attribute("srcset")
            except StaleElementReferenceException:
                print("*** oops! ***")
                continue
                
            if not s: continue

            img_url = s.split(",")[-1].split()[0]
            print("{: <4}{}".format(i,img_url))
##            print(img_url.split("/"))
            savename = img_url.split("/")[-1].split("?")[0]

            res = requests.get(img_url)
            with open("/".join((dist,savename)), "wb") as fout:
                fout.write(res.content)
            
            i += 1
##            time.sleep(1)
            

##        break
