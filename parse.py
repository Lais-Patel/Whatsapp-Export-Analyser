import re
from datetime import datetime
import pandas as pd

# Whatsapp Export path without file extenstion
file_name = "data\whatsapp_data"

exclude_people = True # Set to False to exclude names in excluded from dataset
exclude_metaAI = True # Set to False to exclude Meta AI from dataset
after_date = "14/11/2024" # Choose when to start collecting data from dd/mm/yyyy
before_date = "15/12/2026" # Choose when to stop collecting data from dd/mm/yyyy

chat_log = []

def add_log(timestamp, msg, chat_log):
    data = [datetime.strptime(timestamp[1:], "%d/%m/%Y, %H:%M - ")]
    data.append(msg[0])
    data.append(msg[1][1:])
    chat_log.append(data)

def check_excldues(name):
    with open("excluded.txt") as excludes:
        add_to_log = True

        for exclude_name in excludes.read().split():
            if exclude_name == name:
                add_to_log = False
        
        if name == "Meta AI" and exclude_metaAI:
            add_to_log = False

    return add_to_log

def check_data_range(timestamp, check_data):
    if check_data == False and (timestamp[1:11] == after_date):
        check_data = True
    elif check_data == True and (timestamp[1:11] == before_date):
        check_data = False
    return check_data

def save_to_csv(chat_log):
    df = pd.DataFrame(chat_log, columns=["Datetime","Name","Message"])
    df = df.set_index("Datetime")
    df = df.sort_values("Datetime")
    df.to_csv(file_name+".csv")

def main():
    check_data = False
    with open(file_name+".txt", encoding="utf8") as f:
        log = f.read()
        timestamps = re.findall(r"\n\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ", log)
        messages = re.split(r"\n\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ", log)[1:]

        for i,timestamp in enumerate(timestamps):
            if messages[i].find(":",3,15)>-1:
                msg = messages[i].replace("\n"," ")
                msg = msg.split(":",1)
                check_data = check_data_range(timestamp,check_data)
                if (check_data == True):
                    if exclude_people:
                        if check_excldues(msg[0]):
                            if msg[1][:6] != " POLL:":
                                add_log(timestamp, msg, chat_log)
                    else:
                        if msg[1][:6] != " POLL:":
                                add_log(timestamp, msg, chat_log)

    save_to_csv(chat_log)

    print("Finished Parsing")

main()