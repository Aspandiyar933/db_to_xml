import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import Error
from config import *
import logging 

logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s)')

try:
    conn = mysql.connector.connect(
        host=HOST,
        user=USER, 
        password=PASSWORD,
        database=DATABASE
    )
except Error as err:
    logging.error("Error while connecting to MySQL", err)

cursor = conn.cursor()

try:
    with open('query.sql', 'r', encoding='utf-8') as file:
        query = file.read()
except FileNotFoundError as err:
    logging.INFO("File not found", err)

cursor.execute(query)

data = cursor.fetchall()

#tree = ET.parse('newlist.xml')
#root = tree.getroot()

root = ET.Element("yml_catalog")
shop = ET.SubElement(root, "shop")
categories = ET.SubElement(shop, "categories")
offers = ET.SubElement(shop, "offers")


result = {}
data_about_goods = {}
counter = 0
for row in data:
    if not result.get(row[4]) and row[4] != None:
        result[row[4]] = row[5]
        category = ET.SubElement(categories, "category")
        category.set("id", str(row[4]))
        category.set('type', 'new')
        category.text = str(row[5])
        #categories_element = root.find('.//categories')
        #categories_element.append(category)
    data_about_goods[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
    counter += 1
    offer = ET.SubElement(offers, "offer")    
    offer.set("id", str(row[0]))
    offer.set("type", "vendor.model")
    #offers_element = root.find('.//offers')
    #offers_element.append(offer)
    typePrefix = ET.SubElement(offer, "typePrefix")
    typePrefix.text = "Товар"
    vendor = ET.SubElement(offer, "vendor")
    vendor.text = "BOSCH"
    model = ET.SubElement(offer, "model")
    model.text = str(row[1])
    name = ET.SubElement(offer, "name")
    name.text = str(row[2])
    currencyId = ET.SubElement(offer, "currencyId")
    currencyId.text = "KZT"
    categoryId = ET.SubElement(offer, "categoryId")
    categoryId.text = str(row[4])
    picture = ET.SubElement(offer, "picture")
    picture.text = str(row[3])
    url = ET.SubElement(offer, "url")
    url.text = str(row[7])
    shortDescription = ET.SubElement(offer, "shortDescription")
    shortDescription.text = str(row[6])
    # offer.append(typePrefix)
    # offer.append(vendor)
    # offer.append(model)
    # offer.append(name)
    # offer.append(currencyId)
    # offer.append(categoryId)
    # offer.append(picture)
    # offer.append(url)
    # offer.append(shortDescription)

tree = ET.ElementTree(root)

try:
    tree.write('your_modified_xml_file.xml', encoding='utf-8', xml_declaration=True)
    print(f"New category added successfully. And has adding {counter} goods")
    logging.info(f"New category added successfully. And has adding {counter} goods")
except:
    logging.error("Error while writing to file")

#print(data_about_goods)

cursor.close()
conn.close()

