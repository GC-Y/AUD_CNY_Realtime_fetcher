from flask import Flask, render_template, jsonify
import threading
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import csv
import os
import json

app = Flask(__name__)

# Global variable to store the latest data
latest_data = {
    "price": None,
    "time": None,
    "date": None,
    "history": []
}

# Load existing data from all log files
def load_latest_logs():
    folder = "log_history"
    if not os.path.exists(folder):
        os.makedirs(folder)
        return
    
    # Find all log files
    log_files = [f for f in os.listdir(folder) if f.startswith("log_") and f.endswith(".csv")]
    if not log_files:
        return
    
    # Sort files by their creation date (most recent first)
    log_files.sort(reverse=True)
    
    # Collect all historical data
    all_entries = []
    
    # Process each log file
    for log_file in log_files:
        file_path = os.path.join(folder, log_file)
        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header
                if not header:
                    continue  # Skip empty files
                
                for row in reader:
                    if len(row) >= 3:  # Ensure row has expected data
                        try:
                            entry = {
                                "price": float(row[0]),
                                "time": row[1],
                                "date": row[2]
                            }
                            # Add only if not duplicate (same date+time)
                            if not any(e["date"] == entry["date"] and e["time"] == entry["time"] for e in all_entries):
                                all_entries.append(entry)
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing row in {log_file}: {row}, Error: {e}")
        except Exception as e:
            print(f"Error reading file {log_file}: {e}")
    
    if all_entries:
        # Sort all entries by date and time
        all_entries.sort(key=lambda x: (x["date"], x["time"]))
        
        # Set the latest data
        latest_entry = all_entries[-1]
        latest_data["price"] = latest_entry["price"]
        latest_data["time"] = latest_entry["time"]
        latest_data["date"] = latest_entry["date"]
        
        # Get historical data (last 100 entries)
        latest_data["history"] = all_entries[-100:]
        
        print(f"Loaded {len(all_entries)} historical entries from {len(log_files)} log files")

# Function to fetch the AUD sell rate
def fetch_lowest_aud_sell_rate(url_info):
    try:
        response = requests.get(url_info[1])
        soup = BeautifulSoup(response.content, 'html.parser')
        target_tr = soup.find(lambda tag: tag.name == "td" and "澳大利亚元" in tag.text).find_parent("tr")

        for i, row in enumerate(target_tr):
            if i == 7:
                return float(row.text.strip())/url_info[0]  # Ensure to strip whitespace for accurate comparison
    except Exception as e:
        print(f"Error fetching rate: {e}")
        return None

def log_to_csv(rate, time_str, date_str, filename):
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Price', 'Time', 'Date'])  # Write the header if the file doesn't exist
        writer.writerow([rate, time_str, date_str])

# Background task to fetch rates
def background_fetcher():
    # Check if there is a folder called "log_history" in the current dir, will create one if not.
    folder = "log_history"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate the filename based on the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(folder, f"log_{current_datetime}.csv")

    url_dict = dict()
    url_dict["boc"] = [100, "https://www.boc.cn/sourcedb/whpj/"]  # 100 is the multiplier for boc result

    last_printed_rate = None

    while True:
        boc_aud_rate = fetch_lowest_aud_sell_rate(url_dict["boc"])
        
        if boc_aud_rate is not None:
            now_date = datetime.now().strftime("%Y-%m-%d")
            now_time = datetime.now().strftime("%H:%M:%S")

            if boc_aud_rate != last_printed_rate:  # Check if the fetched rate is different from the last printed rate
                print(f'Price: {boc_aud_rate}, Time: {now_time}, Date: {now_date}')
                log_to_csv(boc_aud_rate, now_time, now_date, filename)  # Log the information to the CSV file
                
                # Update the global variable
                latest_data["price"] = boc_aud_rate
                latest_data["time"] = now_time
                latest_data["date"] = now_date
                
                # Update history (keep last 30 entries)
                latest_data["history"].append({"price": boc_aud_rate, "time": now_time, "date": now_date})
                if len(latest_data["history"]) > 30:
                    latest_data["history"] = latest_data["history"][-30:]
                
                last_printed_rate = boc_aud_rate  # Update the last printed rate

        sleep_time = random.uniform(60, 90)
        time.sleep(sleep_time)  # Wait before fetching the next rate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/latest')
def get_latest_data():
    return jsonify(latest_data)

if __name__ == '__main__':
    # Load existing data if available
    load_latest_logs()
    
    # Start the background fetcher in a separate thread
    fetcher_thread = threading.Thread(target=background_fetcher, daemon=True)
    fetcher_thread.start()
    
    # Get local IP address
    import socket
    def get_local_ip():
        try:
            # Create a socket connection to an external server
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Doesn't need to be reachable
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
    
    local_ip = get_local_ip()
    port = int(os.environ.get('PORT', 5000))
    url = f"http://{local_ip}:{port}"
    
    # Open browser automatically
    import webbrowser
    print(f"Opening browser to {url}")
    print(f"You can also access this page from other devices on your network at: {url}")
    webbrowser.open(f"http://localhost:{port}")
    
    # Start the Flask app - host='0.0.0.0' ensures it's accessible from other devices
    app.run(host='0.0.0.0', port=port, debug=False)