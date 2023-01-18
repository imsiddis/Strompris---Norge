# This will be a discord bot.
# The bot token is: MTA1NDA2MzU3MDIwNTI3ODMzOQ.Gqqlbu.jf5j5dPRfHr-pRenj5UsolqPcivVd0lZzAzLbA
# The bot id is: 1054063570205278339

import discord
import discord.ext.commands as commands
import requests
import bs4
import schedule
import time
import datetime
import urllib.request
import json
import os

# This will be the bot token. [THIS WILL NEED TO BE CHANGED TO THE BOT TOKEN]
bot_token = "<BOT TOKEN>"


# This will be the channel id. [THIS WILL NEED TO BE CHANGED TO THE CHANNEL ID]
channel_id = "<CHANNEL ID>"

# This will be the bot prefix.
bot_prefix = "!"

# This will be the bot master id. [THIS WILL NEED TO BE CHANGED TO THE MASTER ID]
master_id = "<MASTER ID>"

#==========================#
# JSON PROJECT STARTS HERE #
#==========================#

def read_json():
    """
    This function will read the power_price.json file.
    """
    with open("power_price.json", "r") as file:
        data = json.load(file)
    return data

# Class for the JSON data.
class PowerPrice:
    """
    The PowerPrice class will contain the data from the power_price.json file.
    The power_price.json file will contain the power price data from which the bot will get the data from.
    """
    def __init__(self, data):
        """
        The __init__ function will initialize the PowerPrice class.
        It will set the data from the power_price.json file to the data variable.
        It will set the price_today variable to the price_today variable.
        It will set the price_tomorrow variable to the price_tomorrow variable.
        It will set the areas variable to the areas variable.

        Args:
            data (dict): The data from the power_price.json file.

        Returns:
            None
        """

        self.data = data
        self.price_today = data["price_today"]
        try:
            self.price_tomorrow = data["price_tomorrow"]
        except:
            self.price_tomorrow = "No data"
        self.areas = data["areas"]

    def get_price_today(self):
        # Return the price today.
        return self.price_today

    def get_price_tomorrow(self):
        # Return the price tomorrow.
        return self.price_tomorrow

    def get_areas(self):
        # Return the areas.
        return self.areas

    def get_price_area(self, area):
        # Return the price of a specific area.
        index = self.areas["omraade"].index(area)
        return self.areas["snitt"][index], self.areas["min"][index], self.areas["max"][index]
    
    # Get the price of electricity in a specific area.
    def get_price_now(self):
        return self.price_today["now"]
    def get_price_avg(self):
        return self.price_today["avg"]
    def get_price_min(self):
        return self.price_today["min"]
    def get_price_max(self):
        return self.price_today["max"]


#================#
# GET AREA PRICE #
#================#
def get_table():
    """
    get_table will scrape the minspotpris.no website and return the table as a list of lists.
    """
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



#  Extract the four lists from the table.
def get_lists():
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
    return omraade, snitt, min, max

# Get the price of electricity in a specific area.
def get_price_area(area):
    # Get the lists from the table.
    omraade, snitt, min, max = get_lists()
    # Get the index of the area.
    index = omraade.index(area)
    # Return the price of the area.
    return snitt[index], min[index], max[index]


# Get the price of electricity for all areas.
def get_price_country():
    data = read_json()
    # Call the PowerPrice class to get the data.
    power_price = PowerPrice(data)
    sør = power_price.get_price_area("SØR")
    nord = power_price.get_price_area("NORD")
    øst = power_price.get_price_area("ØST")
    vest = power_price.get_price_area("VEST")
    # Return the price of electricity for all areas.
    return (f"```=========================\nOmrådet: Vestlandet\nSnittpris: {vest[0]}\nMinimumspris: {vest[1]}\nMaksimumspris: {vest[2]}\n=========================\n\n=========================\nOmrådet: Østlandet\nSnittpris: {øst[0]}\nMinimumspris: {øst[1]}\nMaksimumspris: {øst[2]}\n\n=========================\nOmrådet: Sørlandet\nSnittpris: {sør[0]}\nMinimumspris: {sør[1]}\nMaksimumspris: {sør[2]}\n\n=========================\nOmrådet: Nordlandet\nSnittpris: {nord[0]}\nMinimumspris: {nord[1]}\nMaksimumspris: {nord[2]}\n=========================```")




# This will get the time when electricity is cheapest.
def get_cheapest_time():
    page = requests.get(f"https://minspotpris.no/")
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    element = soup.find("span", class_="green b")
    cheapest_time = element.get_text()
    return cheapest_time


# This will be the function to get the price of electricity.
def get_price(t1, t2):
    # First, we will get the HTML of the page.
    page = requests.get(f"https://minspotpris.no/")
    # Then we will parse the HTML using beautifulsoup.
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    # Now we will find the price of electricity.
    element = soup.find(t1, class_=t2)
    price = element.get_text()    
    return price

# This will be the function to get the price of electricity for tomorrow.
def get_tomorrow_price():
        tomorrow_avg = get_price("span","em24 c")
        tomorrow_min = get_price("span","em24 c green")
        tomorrow_max = get_price("span","em24 c red")
        return f'```=================================\n\t ~ Oversikt for imorgen ~\n=================================\nSnittpris: {tomorrow_avg} øre/kWh\nMinimumspris: {tomorrow_min} øre/kWh\nMaksimumspris: {tomorrow_max} øre/kWh\n=================================```'

# This function will error handle the get_tomorrow_price function.
def get_tomorrow_price_error():
    data = read_json()
    tomorrow = PowerPrice(data).get_price_tomorrow()
    try:
        return f'```=================================\n\t ~ Oversikt for imorgen ~\n=================================\nSnittpris: {tomorrow["avg"]} øre/kWh\nMinimumspris: {tomorrow["min"]} øre/kWh\nMaksimumspris: {tomorrow["max"]} øre/kWh\n=================================```'
    except:
        return "```#===============================================================#\n# Oops, det ser ut til at morgendagens priser enda ikke er ute!\n # Prisene for imorgen blir klare klokken 14:00 hver dag.\n# Ha en fin dag!\n#===============================================================#```"


def get_today_price():
    # get_now = get_price("span","em24 i")
    # get_avg = get_price("span","em24")
    # get_min = get_price("span","em18")
    # get_max = get_price("td","r red")
    data = read_json()
    today = PowerPrice(data).get_price_today()
    return f'```=================================\n\t ~ Oversikt for i dag ~\n=================================\nNå: {today["now"]}\nSnittpris: {today["avg"]} øre/kWh\nMinimumspris: {today["min"]} øre/kWh\nMaksimumspris: {today["max"]} øre/kWh\n=================================\nKlokken {get_cheapest_time()} er det billigst å bruke strøm.```'


# This function should check the time the JSON file was last updated.
def check_file_time_update():
    # Check the time the file was last updated.
    file_time = os.path.getmtime("power_price.json")
    # Convert the time to a readable format.
    file_time = time.ctime(file_time)
    # Return the time.
    return file_time


intents = discord.Intents.default()
intents.message_content = True

# Client
client = discord.Client(intents=intents)

# Commands
@client.event
async def on_ready():
    print("Bot is ready!")

# Function to print to console when a command is used.
def print_command(message):
    print(f"{message.author} used the command {message.content} in the channel {message.channel}")

@client.event
async def on_message(message):
    """
    This function will be used to handle all the commands.
    It will also print to console when a command is used in a discord channel.
    """
    # Get the current hour and the next hour in two different variables.
    current_hour = datetime.datetime.now()
    next_hour = current_hour + datetime.timedelta(hours=1)
    next_hour = next_hour.strftime("%H" + ":00")
    current_hour = current_hour.strftime("%H" + ":00")
    if message.author == client.user:
        return
    elif message.content == "!updatelog" or message.content == "!lastupdate" or message.content == "!lu":
        await message.channel.send(f"```#===============================================================#\n# Siste gang filen ble oppdatert var {check_file_time_update()}\n#===============================================================#```")
    elif message.content == "!idag":
        await message.channel.send(get_today_price())
    elif message.content == "!nå":
        print_command(message)
        data = read_json()
        now = PowerPrice(data).get_price_now()
        # get_now = get_price("span","em24 i")
        await message.channel.send(f"```#===========================================================#\n# Prisen nå mellom klokken {current_hour} og {next_hour} er {now} øre/kWh #\n#===========================================================#```")
    elif message.content == "!snitt":
        print_command(message)
        data = read_json()
        avg = PowerPrice(data).get_price_avg()
        # get_avg = get_price("span","em24")
        await message.channel.send(f"```Snittprisen i dag er {avg} øre/kWh```")
    elif message.content == "!min":
        print_command(message)  
        data = read_json()
        min = PowerPrice(data).get_price_min()
        # get_min = get_price("span","em18")
        await message.channel.send(f'```Minimumsprisen i dag er {min} øre/kWh```')
    elif message.content == "!max":
        print_command(message)
        data = read_json()
        max = PowerPrice(data).get_price_max()
        # get_max = get_price("td","r red")
        await message.channel.send(f'```Maksimumsprisen i dag er {max} øre/kWh```')
    elif message.content == "!hjelp" or message.content == "!help":
        await message.channel.send(f'```!idag: Viser pris nå, snittpris, minimumspris og maksimumspris.\n!imorgen: Viser prisen for imorgen.\n!nå: Viser pris nå.\n!snitt: Viser snittprisen.\n!min: Viser minimumsprisen.\n!max: Viser maksimumsprisen.\n!vest: Viser pris for Vestlandet.\n!midt: Viser pris for Midt-Norge.\n!øst: Viser pris for Østlandet.\n!sør: Viser pris for Sør-Norge.\n!nord: Viser pris for Nord-Norge.```')
    elif message.content == "!imorgen":
        print_command(message)
        await message.channel.send(get_tomorrow_price_error())
    # Area commands
    elif message.content == "!vest":
        print_command(message)
        data = read_json()
        power_price = PowerPrice(data)
        price = power_price.get_price_area("VEST")
        await message.channel.send(f"```Området: Vestlandet\nSnittpris: {price[0]}\nMinimumspris: {price[1]}\nMaksimumspris: {price[2]}```")
    elif message.content == "!midt":
        print_command(message)
        data = read_json()
        power_price = PowerPrice(data)
        price = power_price.get_price_area("MIDT")
        await message.channel.send(f"```Området: Midt-Norge\nSnittpris: {price[0]}\nMinimumspris: {price[1]}\nMaksimumspris: {price[2]}```")
    elif message.content == "!øst":
        print_command(message)
        data = read_json()
        power_price = PowerPrice(data)
        price = power_price.get_price_area("ØST")
        await message.channel.send(f"```Området: Østlandet\nSnittpris: {price[0]}\nMinimumspris: {price[1]}\nMaksimumspris: {price[2]}```")
    elif message.content == "!sør":
        print_command(message)
        data = read_json()
        power_price = PowerPrice(data)
        price = power_price.get_price_area("SØR")
        await message.channel.send(f"```Området: Sørlandet\nSnittpris: {price[0]}\nMinimumspris: {price[1]}\nMaksimumspris: {price[2]}```")
    elif message.content == "!nord":
        print_command(message)
        data = read_json()
        power_price = PowerPrice(data)
        price = power_price.get_price_area("NORD")
        
        await message.channel.send(f"```Området: Nord-Norge\nSnittpris: {price[0]}\nMinimumspris: {price[1]}\nMaksimumpris: {price[2]}```")
    elif message.content == "!når":
        print_command(message)
        await message.channel.send(f"```{get_cheapest_time()}```")
    elif message.content == "!norge":
        print_command(message)
        await message.channel.send(get_price_country())
    else:
        pass

# Run the bot
client.run(bot_token)