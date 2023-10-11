import os
import xml.etree.ElementTree as ET


file_path = "./list.xml"
if os.path.exists(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
else:
    print(f"The file {file_path} does not exist.")
