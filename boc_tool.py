# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from tqdm import tqdm

def fetch_lowest_boc_sell_rate():
    boc_url = "https://www.kylc.com/bank/rmbfx/b-boc.html"
    response = requests.get(boc_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    target_tr = soup.find(lambda tag: tag.name=="td" and "澳大利亚元" in tag.text).find_parent("tr")

    for i, row in enumerate(target_tr):
        if i == 7:
            return row.text.strip()  # Ensure to strip whitespace for accurate comparison
            
def sleep_with_progress(sleep_time):
    intervals = int(sleep_time / 0.1)
    for _ in tqdm(range(intervals), desc="Sleeping"):
        time.sleep(0.1)

last_printed_rate = None  # Initialize variable to store the last printed rate

while True:
    boc_aud_rate = fetch_lowest_boc_sell_rate()
    now_date = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")
    
    if boc_aud_rate != last_printed_rate:  # Check if the fetched rate is different from the last printed rate
        print(f'Rate：{boc_aud_rate}, Time：{now_time}, Date：{now_date}')
        last_printed_rate = boc_aud_rate  # Update the last printed rate
    
    sleep_time = random.uniform(60, 90)
    time.sleep(sleep_time)  # Wait before fetching the next rate
