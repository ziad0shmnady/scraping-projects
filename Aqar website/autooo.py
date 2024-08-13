from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
import random
import datetime
from googletrans import Translator
import json
driver = webdriver.Chrome()
## function

def translate_text(text, target_language='en'):
    translator = Translator()
    try:
        translated_text = translator.translate(text, dest=target_language)
        return translated_text.text
    except Exception as e:
        print("Translation error:", e)
        return None
    
def find_name(driver=driver):
    try:
        name=driver.find_element(By.CSS_SELECTOR, '._title__eliuu h1').text
    except:
        name = None
    return name

def find_price(driver=driver):
    try:
        price=driver.find_element(By.CSS_SELECTOR, '._price__EH7rC').text
    except:
        price = None
    return price

def find_content(driver=driver):
    try:
        content=driver.find_element(By.CSS_SELECTOR, 'p._content__om2Q_').text
    except:
        content = None
    return content

def find_feature(driver=driver):
    try:
        feature={}
        div=driver.find_element(By.CSS_SELECTOR, 'div._specs__Ag0l9')
        divs=div.find_elements(By.CSS_SELECTOR, 'div._item___4Sv8')

        for i in divs:
            key=i.find_element(By.CSS_SELECTOR, 'div._label___qjLO').text
            # translate the key to english
            # key=translate_text(key)

            try:
                   
                value=i.find_element(By.CSS_SELECTOR, 'p._label___qjLO').text
                feature[key]=value
            except:
                try:
                    value=i.find_element(By.CSS_SELECTOR, 'img[alt="Available-colored"]').text
                    feature[key]="مـتـاح"
                except:
                    value=None
    except:
        feature = feature
    return feature
    
def find_images(driver=driver):
    try:

        images=[]
        list_images=driver.find_elements(By.CSS_SELECTOR, 'div._listingImages__tKNxb img')

        for i in list_images:
            ## get firts link from srcset
            image=i.get_attribute('srcset').split(",")[0].split(" ")[0]
            images.append(image)
    except:
        images = modified_images
    modified_images = [url.replace('350x0', '1080x0') for url in images]
    return modified_images



# Load the configuration from the JSON file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)





## Loop through the number of pages to get links
data=[]
##Enter the number of pages you want to scrape
for item in config_data['Aqar_website']:
    # Iterate over each key in the inner dictionary
    for key in item:
        # Print the URL
        value=item[key]['url']
        driver.delete_all_cookies()
        driver.get(value+"/"+str(5000))
        page=driver.find_elements(By.CSS_SELECTOR,"._pagination__Fz1t6  span")[-1].text
        item[key]['all_pages']=page

with open('config.json', 'w') as config_file:
    json.dump(config_data, config_file, indent=4)

for item in config_data['Aqar_website']:
    # Iterate over each key in the inner dictionary
    for key in item:
        # Print the URL
        category=key
        value=item[key]['url']
        page=item[key]['all_pages']
        page_scraped=item[key]['page_scraped']
      
        driver.delete_all_cookies()
        for i in range(1, int(3)):
            driver.delete_all_cookies()
            driver.get(value+"/"+str(i))
            link=driver.find_elements(By.CSS_SELECTOR, '._list__Ka30R a ')
            links=[]
            for j in range(0,len(link)):

                linkk=link[j].get_attribute("href")
                links.append(
                    {
                        "page_num":i,
                        "url":linkk,
                        "item_number":j+1,
                        "category": category
                    }
                )

                with open('links.json', 'w') as links_file:
                    json.dump(links, links_file, indent=4)
                driver.delete_all_cookies()                  
            for item in range(0,len(links)-17):
                # i=start
                driver.delete_all_cookies()

                driver.get(links[item]["url"])
                counter=item+1

                try:
                    ## wait for the page to load using driver.implicitly_wait
                    # driver.implicitly_wait(5)
                    name= find_name()
                except:
                    name = None
                try:
                    price= find_price()
                except:
                    price = None
                try:
                    content= find_content()
                except:
                    content = None
                try:
                    feature= find_feature()
                except:
                    feature = None
                try:
                    images= find_images()
                except:
                    images = None
                data.append({"url":links[item]["url"],"name":name,"category":links[item]["category"] ,"price":price, "content":content, "feature":feature, "images":images,"insert_date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"update_date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                driver.delete_all_cookies()
                random_name="data.json"  ## +str(random.randint(10,1000))+".json"
                with open(random_name, 'w', encoding='utf-8') as all_data:
                    json.dump(data, all_data, ensure_ascii=False, indent=4)
                for itemm in config_data['Aqar_website']:
                # Iterate over each key in the inner dictionary
                    for key in itemm:
                        # Print the URL
                        
                        if(links[item]["category"]==key):
                            itemm[key]['item_scraped']+=1
                        
                        with open('config.json', 'w') as config_file:
                            json.dump(config_data, config_file, indent=4)
            ##update page_scraped

            for category_item in config_data['Aqar_website']:
                category_key = list(category_item.keys())[0]
                if category_key == links[item]["category"]:
                    category_item[category_key]['page_scraped'] += 1

                    with open('config.json', 'w') as config_file:
                        json.dump(config_data, config_file, indent=4)










