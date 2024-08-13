import mysql.connector
import json
from googletrans import Translator

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


def translate_text(text, target_language="en"):
    translator = Translator()
    try:
        translated_text = translator.translate(text, dest=target_language)
        return translated_text.text
    except Exception as e:
        print("Translation error:", e)
        return None


# Create cursor
cursor = connection.cursor()

if cursor:
    try:
        # Create cursor
        cursor = connection.cursor()
        # Get records from property_data table where translation is required
        cursor.execute("SELECT * FROM property_data WHERE is_translated = 0")
        records = cursor.fetchall()

        # Translate and insert records into translated_property_data table
        for record in records:
            (
                id,
                ad_id,
                ad_url,
                title,
                category,
                price,
                description,
                city,
                district,
                images,
                user_id,
                latitude,
                longitude,
                street_width,
                street_direction,
                property_age,
                rent_period,
                area_square_meters,
                width,
                length,
                number_apts,
                number_stores,
                number_living_rooms,
                number_bathrooms,
                number_rooms,
                meter_price,
                wells,
                trees,
                pool,
                car_entrance,
                maid_room,
                air_conditioning,
                duplex,
                driver_room,
                ad_license_number,
                backyard,
                number_kitchens,
                extra_unit,
                elevator,
                family_section,
                football_stadium,
                playground,
                volleyball_stadium,
                basement,
                created_time,
                last_update,
                insert_date,
                update_date,
                is_translated,
            ) = record
            translated_title = translate_text(title)
            translated_description = translate_text(description)
            translated_city = translate_text(city)
            translated_district = translate_text(district)
            translated_price = translate_text(price)
            translated_user_id = translate_text(user_id)
            translated_last_update = translate_text(last_update)
            translated_rent_period = translate_text(rent_period)
            translated_area_square_meters = translate_text(area_square_meters)
            if (
                translated_title
                and translated_description
                and translated_city
                and translated_district
                and translated_user_id
                and translated_last_update
                and translated_rent_period
                and translated_area_square_meters
                and translated_price
            ):
                insert_query = """INSERT INTO translate_property_data (
              ad_id, ad_url, title, category, price, description, city, district, images,user_id, latitude, longitude,
                  street_width, street_direction, property_age, rent_period, area_square_meters,
    width, length, number_apts, number_stores, number_living_rooms, number_bathrooms,
    number_rooms, meter_price, wells, trees, pool, car_entrance, maid_room,
     air_conditioning, duplex, driver_room, ad_license_number, backyard,
    number_kitchens, extra_unit, elevator, family_section, football_stadium,
    playground, volleyball_stadium,basement, created_time, last_update, insert_date, update_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s)"""

                # Insert translated data into translated_property_data table
                cursor.execute(
                    insert_query,
                    (
                        ad_id,
                        ad_url,
                        translated_title,
                        category,
                        translated_price,
                        translated_description,
                        translated_city,
                        translated_district,
                        images,
                        translated_user_id,
                        latitude,
                        longitude,
                        street_width,
                        street_direction,
                        property_age,
                        translated_rent_period,
                        translated_area_square_meters,
                        width,
                        length,
                        number_apts,
                        number_stores,
                        number_living_rooms,
                        number_bathrooms,
                        number_rooms,
                        meter_price,
                        wells,
                        trees,
                        pool,
                        car_entrance,
                        maid_room,
                        air_conditioning,
                        duplex,
                        driver_room,
                        ad_license_number,
                        backyard,
                        number_kitchens,
                        extra_unit,
                        elevator,
                        family_section,
                        football_stadium,
                        playground,
                        volleyball_stadium,
                        basement,
                        created_time,
                        translated_last_update,
                        insert_date,
                        update_date,
                    ),
                )

                # Update isTranslated flag for the current record
                update_query = (
                    "UPDATE property_data SET is_translated = 1 WHERE id = %s"
                )
                cursor.execute(update_query, (id,))

                # Commit changes to the database
                connection.commit()
                print("Record with ID:", ad_id, "translated successfully.")
            else:
                print("Translation failed for record with ID:", id)

    except mysql.connector.Error as error:
        print("Error executing MySQL query:", error)
    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
else:
    print("Database connection failed.")
