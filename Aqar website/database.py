import mysql.connector
import json

with open("database.json", "r") as database_file:
    database_data = json.load(database_file)

# Connect to MySQL
connection = mysql.connector.connect(
    host=database_data.get("database").get("host"),
    user=database_data.get("database").get("user"),
    password=database_data.get("database").get("password"),
    database=database_data.get("database").get("database"),
)

# Create cursor
cursor = connection.cursor()

# Create table 'property_data'
create_property_table_query = """
CREATE TABLE IF NOT EXISTS property_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ad_id VARCHAR(255) UNIQUE NOT NULL,
    ad_url TEXT,
    title TEXT,
    category TEXT,
    price TEXT,
    description TEXT,
    city TEXT,
    district TEXT,
    images TEXT,
    user_id TEXT,
    latitude TEXT,
    longitude TEXT,
    street_width TEXT,
    street_direction TEXT,
    property_age TEXT,
    rent_period TEXT,
    area_square_meters TEXT,
    width TEXT,
    length TEXT,
    number_apts TEXT,
    number_stores TEXT,
    number_living_rooms TEXT,
    number_bathrooms TEXT,
    number_rooms TEXT,
    meter_price TEXT,
    wells TEXT,
    trees TEXT,
    pool TEXT,
    car_entrance TEXT,
    maid_room TEXT,
    air_conditioning TEXT,
    duplex TEXT,
    driver_room TEXT,
    ad_license_number TEXT,
    backyard TEXT,
    number_kitchens TEXT,
    extra_unit TEXT,
    elevator TEXT,
    family_section TEXT,
    football_stadium TEXT,
    playground TEXT,
    volleyball_stadium TEXT,
    basement TEXT,
    created_time  TEXT,
    last_update TEXT,
    insert_date TEXT,
    update_date TEXT,
    is_translated BOOLEAN DEFAULT FALSE
)
"""
cursor.execute(create_property_table_query)

# Create table 'translate'
create_translate_table_query = """
CREATE TABLE IF NOT EXISTS translate_property_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ad_id VARCHAR(255) UNIQUE NOT NULL,
    ad_url TEXT,
    title TEXT,
    category TEXT,
    price TEXT,
    description TEXT,
    city TEXT,
    district TEXT,
    images TEXT,
    user_id TEXT,
    latitude TEXT,
    longitude TEXT,
    street_width TEXT,
    street_direction TEXT,
    property_age TEXT,
    rent_period TEXT,
    area_square_meters TEXT,
    width TEXT,
    length TEXT,
    number_apts TEXT,
    number_stores TEXT,
    number_living_rooms TEXT,
    number_bathrooms TEXT,
    number_rooms TEXT,
    meter_price TEXT,
    wells TEXT,
    trees TEXT,
    pool TEXT,
    car_entrance TEXT,
    maid_room TEXT,
    air_conditioning TEXT,
    duplex TEXT,
    driver_room TEXT,
    ad_license_number TEXT,
    backyard TEXT,
    number_kitchens TEXT,
    extra_unit TEXT,
    elevator TEXT,
    family_section TEXT,
    football_stadium TEXT,
    playground TEXT,
    volleyball_stadium TEXT,
    basement TEXT,
    created_time  TEXT,
    last_update TEXT,
    insert_date TEXT,
    update_date TEXT
)
"""
cursor.execute(create_translate_table_query)


# Commit changes
connection.commit()

# Close cursor and connection
cursor.close()
connection.close()
print("Database setup completed.")
