import re
from datetime import datetime
import pandas as pd

# Whatsapp Export file name
file_name = ""

exclude_people = False # Set to False to exclude names in excluded from dataset
exclude_metaAI = False # Set to False to exclude Meta AI from dataset
after_date = "14/11/2024" # Choose when to start collecting data from dd/mm/yyyy
before_date = "15/12/2026" # Choose when to stop collecting data from dd/mm/yyyy


chat_log = []
check_data = False

with open(file_name, encoding="utf8") as f:
    log = f.read()
    timestamps = re.findall(r"\n\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ", log)
    messages = re.split(r"\n\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ", log)[1:]
    for i,timestamp in enumerate(timestamps):
        if messages[i].find(":",3,15)>-1:
            msg = messages[i].replace("\n"," ")
            msg = msg.split(":",1)
            if check_data == False and (timestamp[1:11] == after_date):
                check_data = True
                print("true")
            elif check_data == True and (timestamp[1:11] == before_date):
                check_data = False
                print("false")
            if (check_data == True):
                if (msg[0] == "Meta AI" and exclude_metaAI == False) or msg[0] != "Meta AI": 
                    if msg[1][:6] != " POLL:":
                        data = [datetime.strptime(timestamp[1:], "%d/%m/%Y, %H:%M - ")]
                        data.append(msg[0])
                        data.append(msg[1][1:])
                        chat_log.append(data)

df = pd.DataFrame(chat_log, columns=["Datetime","Name","Message"])
df = df.set_index("Datetime")
df = df.sort_values("Datetime")
df["Message_Count"] = 1
df["Cum_Messages_Overall"] = df["Message_Count"].cumsum()
df["Cum_Messages"] = df.groupby("Name")["Message_Count"].cumsum()
df.to_csv("data.csv")