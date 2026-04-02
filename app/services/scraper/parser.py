from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def parse_html(html: str):
    return BeautifulSoup(html, "html.parser")


def parse_xml(xml_text: str):
    return ET.fromstring(xml_text)