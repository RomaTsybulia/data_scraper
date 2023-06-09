import datetime
import time

import urllib3
from openpyxl.workbook import Workbook
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

urllib3.disable_warnings()


def scrape_data():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = 'https://www.oree.com.ua/index.php/pricectr'
    driver.get(url)
    div_element = driver.find_element(By.XPATH, "//div[@class='dataTables_scrollBody']")
    next_day_data = div_element.find_elements(By.TAG_NAME, "tr")[-1]
    fields = next_day_data.find_elements(By.TAG_NAME, "td")
    data = {}

    for index, field in enumerate(fields):
        if index == 0:
            data["Date"] = field.text
        else:
            data[str(index) + ":00"] = field.text

    driver.quit()

    return data


def save_data(data_dict: dict):
    workbook = Workbook()
    sheet = workbook.active
    headers = list(data_dict.keys())

    for col_num, header in enumerate(headers, 1):
        sheet.cell(row=1, column=col_num).value = header

    values = list(data_dict.values())

    for col_num, value in enumerate(values, 1):
        sheet.cell(row=2, column=col_num).value = value

    filename = "data.xlsx"
    workbook.save(filename)

if __name__ == "__main__":
    current_time = datetime.datetime.now().strftime("%H:%M")
    for i in range(100):
        if current_time >= "13:00":
            data = scrape_data()
            save_data(data)
            print("Data was gathered successfully!")
            break
        time.sleep(300)
