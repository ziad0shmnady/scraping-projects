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
import sqlite3

import mysql.connector

## import database.json to get the database configuration
with open("database.json", "r") as database_file:
    database_data = json.load(database_file)

# Connect to MySQL
## print the database_data dictionary to see the keys
# print()
connection = mysql.connector.connect(
    host=database_data.get("database").get("host"),
    user=database_data.get("database").get("user"),
    password=database_data.get("database").get("password"),
    database=database_data.get("database").get("database"),
)

# Create cursor
cursor = connection.cursor()
# c = conn.cursor()
driver = webdriver.Chrome()
## function


## translatetion mapping dictionary
translation_mapping = {
    "عرض الشارع": "street_width",
    "الواجهة": "street_direction",
    "عمر العقار": "property_age",
    "مدة الإيجار": "rent_period",
    "المساحة": "area_square_meters",
    "العرض": "width",
    "الطول": "length",
    "عدد الشقق": "number_apts",
    "عدد المحلات": "number_stores",
    "غرف النوم": "number_bedrooms",
    "الصالات": "number_living_rooms",
    "عدد دورات المياة": "number_bathrooms",
    "عدد الغرف": "number_rooms",
    "سعر المتر": "meter_price",
    "عدد الآبار": "wells",
    "عدد الأشجار": "trees",
    " مسبح": "pool",
    " مدخل سيارة": "car_entrance",
    "غرفة خادمة": "maid_room",
    "مكيف": "air_conditioning",
    "دوبلكس": "duplex",
    "غرفة سائق": "driver_room",
    "رخصة الإعلان": "ad_license_number",
    "رقم الإعلان": "ad_id",
    "حوش": "backyard",
    "مطبخ": "number_kitchens",
    "ملحق": "extra_unit",
    "مصعد": "elevator",
    "قسم عوائل": "family_section",
    "ملعب كرة قدم": "football_stadium",
    "ملاهي": "playground",
    "ملعب كرة طائرة": "volleyball_stadium",
    "تاريخ الاضافة": "created_time",
    "اخر تحديث": "last_update",
    "توفر صرف صحي": "basement",
}


def translate_text(text, target_language="en"):
    translator = Translator()
    try:
        translated_text = translator.translate(text, dest=target_language)
        return translated_text.text
    except Exception as e:
        print("Translation error:", e)
        return None


def user_id(driver=driver):
    try:
        user_id = driver.find_element(By.CSS_SELECTOR, "h2._name__Xc3Tb").text
    except:
        user_id = None
    return user_id


def find_name(driver=driver):
    try:
        name = driver.find_element(By.CSS_SELECTOR, "._title__eliuu h1").text
    except:
        name = None
    return name


def find_price(driver=driver):
    try:
        price = driver.find_element(By.CSS_SELECTOR, "._price__EH7rC").text
    except:
        price = None
    return price


def find_content(driver=driver):
    try:
        content = driver.find_element(By.CSS_SELECTOR, "p._content__om2Q_").text
    except:
        content = None
    return content


def find_city(driver=driver):
    try:
        ul = driver.find_element(By.CSS_SELECTOR, "._breadcrumb__4vZNW")
        li = ul.find_elements(By.CSS_SELECTOR, "li")
        city = li[2].text
    except:
        city = None
    return city


def find_latitude_longitude(driver=driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "img[alt='Marker']").click()
        a = driver.find_element(By.CSS_SELECTOR, "a.leaflet-link").get_attribute("href")

        query_string = a.split("?")[1]
        q_value = query_string.split("=")[-1]
        latitude, longitude = q_value.split(",")
        return latitude, longitude
    except:
        latitude = None
        longitude = None
    return latitude, longitude


def find_district(driver=driver):
    try:
        ul = driver.find_element(By.CSS_SELECTOR, "._breadcrumb__4vZNW")
        li = ul.find_elements(By.CSS_SELECTOR, "li")
        district = li[-1].text
    except:
        district = None
    return district


def find_feature(driver=driver):
    try:
        feature = {}
        div = driver.find_element(By.CSS_SELECTOR, "div._specs__Ag0l9")
        divs = div.find_elements(By.CSS_SELECTOR, "div._item___4Sv8")

        for i in divs:
            key = i.find_element(By.CSS_SELECTOR, "div._label___qjLO").text
            ## check if the key is in the translation_mapping dictionary
            if key in translation_mapping:
                key = str(translation_mapping[key])
            else:
                continue
            try:

                value = i.find_element(By.CSS_SELECTOR, "p._label___qjLO").text
                feature[key] = value
            except:
                try:
                    value = i.find_element(
                        By.CSS_SELECTOR, 'img[alt="Available-colored"]'
                    ).text
                    feature[key] = 1
                except:
                    value = None
    except:

        ## return only the keys that are in the translation_mapping dictionary
        feature = feature
    return feature


def find_images(driver=driver):
    try:

        images = []
        list_images = driver.find_elements(
            By.CSS_SELECTOR, "div._listingImages__tKNxb img"
        )

        for i in list_images:
            ## get firts link from srcset
            image = i.get_attribute("srcset").split(",")[0].split(" ")[0]
            images.append(image)
    except:
        images = modified_images
    modified_images = [url.replace("350x0", "1080x0") for url in images]
    return modified_images


# Load the configuration from the JSON file
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)


data = []
nameWithDate = (
    "data" + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S" + ".json")
)
##Enter the number of pages you want to scrape
for item in config_data["Aqar_website"]:
    # Iterate over each key in the inner dictionary
    for key in item:
        # Print the URL
        value = item[key]["url"]
        driver.delete_all_cookies()
        driver.get(value + "/" + str(5000))
        page = driver.find_elements(By.CSS_SELECTOR, "._pagination__Fz1t6  span")[
            -1
        ].text
        item[key]["all_pages"] = page

with open("config.json", "w") as config_file:
    json.dump(config_data, config_file, indent=4)

for item in config_data["Aqar_website"]:
    # Iterate over each key in the inner dictionary
    for key in item:
        # Print the URL
        category = key
        value = item[key]["url"]
        all_page = item[key]["all_pages"]
        page_scraped = item[key]["page_scraped"]

        driver.delete_all_cookies()
        for i in range(page_scraped + 1, int(all_page)):
            driver.delete_all_cookies()
            ##scroll to the bottom of the page
            driver.get(value + "/" + str(i))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            link = driver.find_elements(By.CSS_SELECTOR, "._list__Ka30R a ")
            links = []
            for j in range(0, len(link)):

                linkk = link[j].get_attribute("href")
                links.append(
                    {
                        "page_num": i,
                        "url": linkk,
                        "item_number": j + 1,
                        "category": category,
                    }
                )

                with open("links.json", "w") as links_file:
                    json.dump(links, links_file, indent=4)
                driver.delete_all_cookies()
            for item in range(0, len(links) - 17):
                # i=start
                driver.delete_all_cookies()

                driver.get(links[item]["url"])
                counter = item + 1

                try:
                    ## wait for the page to load using driver.implicitly_wait
                    # driver.implicitly_wait(5)
                    name = find_name()
                except:
                    name = None
                try:
                    price = find_price()
                except:
                    price = None
                try:
                    content = find_content()
                except:
                    content = None
                try:
                    feature = find_feature()
                except:
                    feature = None
                try:
                    images = find_images()
                except:
                    images = None

                try:
                    city = find_city()
                except:
                    city = None

                try:
                    district = find_district()
                except:

                    district = None
                try:
                    userid = user_id()
                except:
                    userid = None
                try:
                    latitude, longitude = find_latitude_longitude()
                except:
                    latitude = None
                    longitude = None
                data.append(
                    {
                        "url": links[item]["url"],
                        "name": name,
                        "category": links[item]["category"],
                        "price": price,
                        "content": content,
                        "city": city,
                        "district": district,
                        "images": images,
                        "user_id": userid,
                        "latitude": latitude,
                        "longitude": longitude,
                        "insert_date": datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "update_date": datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                )
                ## extend the data dictionary with the feature dictionary
                data[-1].update(feature)
                try:
                    ## check if ad_id is already in the database
                    cursor.execute(
                        "SELECT ad_id FROM property_data WHERE ad_id = %s",
                        (feature.get("ad_id"),),
                    )
                    result = cursor.fetchone()
                    if result:
                        ##update the "updated_date" column in the database for the ad_id
                        print("Updating the ad_id:", feature.get("ad_id"))
                        sql = """UPDATE property_data SET update_date = %s WHERE ad_id = %s"""
                        val = (
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            feature.get("ad_id"),
                        )
                        cursor.execute(sql, val)
                        connection.commit()

                    sql = """INSERT INTO property_data (
              ad_id, ad_url, title, category, price, description, city, district, images,user_id, latitude, longitude,
                  street_width, street_direction, property_age, rent_period, area_square_meters,
    width, length, number_apts, number_stores, number_living_rooms, number_bathrooms,
    number_rooms, meter_price, wells, trees, pool, car_entrance, maid_room,
     air_conditioning, duplex, driver_room, ad_license_number, backyard,
    number_kitchens, extra_unit, elevator, family_section, football_stadium,
    playground, volleyball_stadium,basement, created_time, last_update, insert_date, update_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)"""
                    val = (
                        feature.get("ad_id") or None,
                        links[item]["url"],
                        name,
                        links[item]["category"],
                        price,
                        content,
                        city,
                        district,
                        json.dumps(images),
                        userid,
                        latitude,
                        longitude,
                        feature.get("street_width"),
                        feature.get("street_direction"),
                        feature.get("property_age"),
                        feature.get("rent_period"),
                        feature.get("area_square_meters"),
                        feature.get("width"),
                        feature.get("length"),
                        feature.get("number_apts"),
                        feature.get("number_stores"),
                        feature.get("number_living_rooms"),
                        feature.get("number_bathrooms"),
                        feature.get("number_rooms"),
                        feature.get("meter_price"),
                        feature.get("wells"),
                        feature.get("trees"),
                        feature.get("pool"),
                        feature.get("car_entrance"),
                        feature.get("maid_room"),
                        feature.get("air_conditioning"),
                        feature.get("duplex"),
                        feature.get("driver_room"),
                        feature.get("ad_license_number"),
                        feature.get("backyard"),
                        feature.get("number_kitchens"),
                        feature.get("extra_unit"),
                        feature.get("elevator"),
                        feature.get("family_section"),
                        feature.get("football_stadium"),
                        feature.get("playground"),
                        feature.get("volleyball_stadium"),
                        feature.get("basement"),
                        feature.get("created_time"),
                        feature.get("last_update"),
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    cursor.execute(sql, val)
                    connection.commit()

                except mysql.connector.Error as e:
                    print("Database error:", e)
                    continue

                driver.delete_all_cookies()
                with open(nameWithDate, "w", encoding="utf-8") as all_data:
                    json.dump(data, all_data, ensure_ascii=False, indent=4)
                for itemm in config_data["Aqar_website"]:
                    # Iterate over each key in the inner dictionary
                    for key in itemm:
                        # Print the URL

                        if links[item]["category"] == key:
                            itemm[key]["item_scraped"] += 1

                        with open("config.json", "w") as config_file:
                            json.dump(config_data, config_file, indent=4)
            ##update page_scraped

            # Update the page scraped for the right category
            ## read the links file
            with open("links.json", "r") as links_file:
                linkss = json.load(links_file)

                for category_item in config_data["Aqar_website"]:
                    category_key = list(category_item.keys())[0]
                    if category_key == linkss[item]["category"]:
                        category_item[category_key]["page_scraped"] += 1

                        with open("config.json", "w") as config_file:
                            json.dump(config_data, config_file, indent=4)
