# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from tqdm import tqdm
import csv
import os

def fetch_lowest_aud_sell_rate(url: list):
    
    response = requests.get(url[-1])
    soup = BeautifulSoup(response.content, 'html.parser')
    target_tr = soup.find(lambda tag: tag.name == "td" and "澳大利亚元" in tag.text).find_parent("tr")

    for i, row in enumerate(target_tr):
        # print(i, row.text)
        if i == 7:
            # print(row.text)
            
            return float(row.text.strip())/url[0]  # Ensure to strip whitespace for accurate comparison

def sleep_with_progress(sleep_time):
    intervals = int(sleep_time / 0.1)
    for _ in tqdm(range(intervals), desc="Sleeping"):
        time.sleep(0.1)

def log_to_csv(rate, time_str, date_str, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Price', 'Time', 'Date'])  # Write the header if the file doesn't exist
        writer.writerow([rate, time_str, date_str])

last_printed_rate = None  # Initialize variable to store the last printed rate

# Generate the filename based on the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"log_{current_datetime}.csv"

kylc_url = "https://www.kylc.com/bank/rmbfx/b-boc.html"
boc_url = "https://www.boc.cn/sourcedb/whpj/"

url_dict = dict()
url_dict["kylc"] = [1,kylc_url] # 1 is the multiplier for kylc result

url_dict["boc"] = [100,boc_url] # 100 is the multiplier for boc result

while True:
    boc_aud_rate = fetch_lowest_aud_sell_rate(url_dict["boc"])
    
    now_date = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")

    if boc_aud_rate != last_printed_rate:  # Check if the fetched rate is different from the last printed rate
        print(f'Price: {boc_aud_rate}, Time: {now_time}, Date: {now_date}')
        log_to_csv(boc_aud_rate, now_time, now_date, filename)  # Log the information to the CSV file
        last_printed_rate = boc_aud_rate  # Update the last printed rate

    sleep_time = random.uniform(60, 90)
    time.sleep(sleep_time)  # Wait before fetching the next rate 
