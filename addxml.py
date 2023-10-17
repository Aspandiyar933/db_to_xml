import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import Error
from config import *
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO, filename=os.path.join(BASE_DIR, '.log'), filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

try:
    with open(os.path.join(BASE_DIR, 'query.sql'), 'r', encoding='utf-8') as file:
        query = file.read()
except FileNotFoundError as err:
    logging.INFO("File not found", err)


try:
    conn = mysql.connector.connect(
        host=HOST,
        user=USER, 
        password=PASSWORD,
        database=DATABASE
    )

    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
except Error as err:
    logging.error("Error while connecting to MySQL", str(err))


root = ET.Element("yml_catalog")
shop = ET.SubElement(root, "shop")
categories = ET.SubElement(shop, "categories")
offers = ET.SubElement(shop, "offers")

tree = ET.ElementTree(root)


result = {}
counter = 0
for row in data:
    if not result.get(row[4]) and row[4] != None:
        result[row[4]] = row[5]
        category = ET.SubElement(categories, "category")
        category.set("id", str(row[4]))
        category.set('type', 'new')
        category.text = str(row[5])

    counter += 1

    offer = ET.SubElement(offers, "offer")    
    offer.set("id", str(row[0]))
    offer.set("type", "vendor.model")

    typePrefix = ET.SubElement(offer, "typePrefix")
    typePrefix.text = "Товар"

    vendor = ET.SubElement(offer, "vendor")
    vendor.text = "BOSCH"

    model = ET.SubElement(offer, "model")
    model.text = str(row[1])

    name = ET.SubElement(offer, "name")
    name.text = str(row[2])

    price_or = row[9] or row[8] 
    price = ET.SubElement(offer, "price")
    price.text = str(int(price_or))

    currencyId = ET.SubElement(offer, "currencyId")
    currencyId.text = "KZT"

    categoryId = ET.SubElement(offer, "categoryId")
    categoryId.text = str(row[4])

    picture = ET.SubElement(offer, "picture")
    picture.text = 'https://boschcenter.kz/%s' % str(row[3])

    url = ET.SubElement(offer, "url")
    url.text = 'https://boschcenter.kz/%s' % str(row[7])

    shortDescription = ET.SubElement(offer, "shortDescription")
    shortDescription.text = str(row[6])[:-64] + '.'

try:
    tree.write(os.path.join(BASE_DIR, 'feed.xml'), encoding='utf-8', xml_declaration=True)
    print(f"New category added successfully. And has adding {counter} goods")
    logging.info(f"New category added successfully. And has adding {counter} goods")
except:
    logging.error("Error while writing to file")