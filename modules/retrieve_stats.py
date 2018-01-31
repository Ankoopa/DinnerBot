import discord
import requests
from bs4 import BeautifulSoup

try:
    def get_data(handle):
        page = requests.get("https://masterpubg.com/profile/pc/"+handle)
        soup = BeautifulSoup(page.content, 'html.parser')
        p_data = soup.find("div", {"class": "data-lifetime-stats widget widget-table"})
        p_datatable = p_data.find("div", {"class": "table-body"})
        p_labels = p_datatable.findAll("div", {"class": "table-column-left table-label col-xs-6"})
        p_labels_txt = []
        for i in p_labels:
            p_labels_txt.append(i.get_text(strip=True))
        p_vals = p_datatable.findAll("div", {"class": "table-column-left table-value col-xs-6"})
        p_vals_txt = []
        for i in p_vals:
            p_vals_txt.append(i.get_text(strip=True))
        return p_labels_txt, p_vals_txt
except Exception as e:
    print(e)