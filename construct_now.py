# This program will scrape a URL and add the data to a JSON file.
#

import requests
import bs4
import json
import urllib.request
import time
import datetime
import os


# This function will get the price of electricity.
def get_price(t1, t2):
    # First, we will get the HTML of the page.
    page = requests.get(f"https://minspotpris.no/")
    # Then we will parse the HTML using beautifulsoup.
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    # Now we will find the price of electricity.
    element = soup.find(t1, class_=t2)
    price = element.get_text()    
    return price

# This program will scrape a URL and add the data to a JSON file.
def get_table():
    url = "https://minspotpris.no/"
    tables = []
    features = "html.parser"
    html = urllib.request.urlopen(url).read()
    bs = bs4.BeautifulSoup(html, features)
    table = bs.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="dagenspris") 
    rows = table.findAll(lambda tag: tag.name=='tr')
    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip() for ele in cols]
        # Return the table as a list of lists so that it can be sorted.
        tables.append([ele for ele in cols if ele])
    return tables

def time_function():
    time_now = datetime.datetime.now()
    return str(time_now)

#  Extract the four lists from the table.
def get_lists():
    time_now = datetime.datetime.now()
    table = get_table()
    omraade = []
    snitt = []
    min = []
    max = []
    for row in table:
        omraade.append(row[0])
        snitt.append(row[1])
        min.append(row[2])
        max.append(row[3])
    return omraade, snitt, min, max, time_now

def get_cheapest_time():
    page = requests.get(f"https://minspotpris.no/")
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    try:
        element = soup.find("span", class_="green b")
        cheapest_time = element.get_text()
        return cheapest_time
    except AttributeError as e:
        log_error(e)
        element = soup.find_all("div", class_="goleftafter")
        find_br = element[0].find("br")
        cheapest_time = find_br.get_text()
        if cheapest_time == "":
            cheapest_time = "Billigste tid kunne ikke bli funnet."
        return cheapest_time

# export the data to a JSON file.
# The lists should be sorted by area.
def export_json():
    omraade, snitt, min, max, = get_lists()
    with open("power_price.json", "w") as file:
        # Create the JSON object.
        try:
            json_object = {
                "time": time_function(),
                "price_today": {
                    "now": get_price("span","em24 i"),
                    "avg": get_price("span","em24"),
                    "min": get_price("span","em18"),
                    "max": get_price("td","r red")
                },
                "price_tomorrow": {
                    "avg": get_price("span","em24 c"),
                    "min": get_price("span","em24 c green"),
                    "max": get_price("span","em24 c red")
                },
                "areas": {
                    "omraade": omraade,
                    "snitt": snitt,
                    "min": min,
                    "max": max
                },
                "cheapest_time": get_cheapest_time()
            }
            # Write the JSON object to the file.
            json.dump(json_object, file, indent=4)
        except:
            json_object = {
                "price_today": {
                    "now": get_price("span","em24 i"),
                    "avg": get_price("span","em24"),
                    "min": get_price("span","em18"),
                    "max": get_price("td","r red")
                },
                "areas": {
                    "omraade": omraade,
                    "snitt": snitt,
                    "min": min,
                    "max": max
                },
                "cheapest_time": get_cheapest_time()
            }
            # Write the JSON object to the file.
            json.dump(json_object, file, indent=4)

def waiting_animation(duration):
    animation = "|/-\\"
    idx = 0
    start_time = time.time()
    print('Henter strømdata fra nettsiden...', end="\r")
    for i in range(duration):
        print(f'Henter strømdata fra nettsiden... {animation[idx % len(animation)]}', end="\r")
        idx += 1
        time.sleep(0.1)
    end_time = time.time()
    print(f'Strømdata hentet fra nettsiden. Lagrer i power_price.json. Tid brukt: {end_time - start_time:.2f} sekunder')

def create_logs():
    if not os.path.exists("logs.txt"):
        with open("logs.txt", "w") as file:
            file.write("")
    else:
        pass

# Log the errors and successes on a new line.
def log_success():
    with open("logs.txt", "a") as file:
        file.write(f"\n{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Success - JSON file updated.")

def log_error(e=None):
    with open("logs.txt", "a") as file:
        file.write(f"\n{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Error - JSON file could not be updated.")


if __name__ == "__main__":
    create_logs()
    try:
        export_json()
        log_success()
    except Exception as e:
        log_error(e)
    waiting_animation(20)