import re
from datetime import datetime
import pandas as pd
import random

# Whatsapp Export path without file extenstion
file_names = [
    ]
             

exclude_people = True # Set to False to exclude names in excluded from dataset
exclude_metaAI = True # Set to False to exclude Meta AI from dataset
after_date = datetime(2023, 2, 14) # Choose when to start collecting data from (yyyy,mm,dd)
before_date = datetime(2027, 11, 14) # Choose when to stop collecting data from (yyyy,mm,dd)

chat_log = []

def add_log(timestamp, msg, chat_log, file_name):
    data = [datetime.strptime(timestamp[1:], "%d/%m/%Y, %H:%M - ")]
    data.append(file_name[5:])
    data.append(msg[0])
    data.append(msg[1][1:])
    data.append(count_word(msg[1]))
    for i in range(3):
        data.append(0)

    if msg[1][1:] == "<Media omitted>":
        data[3] = " "
        data[4] = 0
        data[5] = 1
    elif msg[1][-26:] == " <This message was edited>":
        data[3] = msg[1][1:-26]
        data[6] = 1
    elif msg[1][1:] == "This message was deleted":
        data[3] = " "
        data[7] = 1
        
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
    if check_data == False and after_date <= (datetime.strptime(timestamp[1:], "%d/%m/%Y, %H:%M - ")) <= before_date:
        print(f'{datetime.strptime(timestamp[1:], "%d/%m/%Y, %H:%M - ")} >= {after_date}')
        print((datetime.strptime(timestamp[1:], "%d/%m/%Y, %H:%M - ") >= after_date))
        check_data = True
        print("in range")
    elif check_data == True and (datetime.strptime(timestamp[1:], "%d/%m/%Y, %H:%M - ") >= before_date):
        print(f'{datetime.strptime(timestamp[1:], "%d/%m/%Y, %H:%M - ")} <= {before_date}')
        print((datetime.strptime(timestamp[1:], "%d/%m/%Y, %H:%M - ") >= before_date))
        check_data = False
        print("out range")
    return check_data

def save_to_csv(chat_log):
    df = pd.DataFrame(chat_log, columns=["Datetime","Chat","Name","Message","Word_Count","Media","Edit","Delete"])
    df = df.set_index("Datetime")
    df = df.sort_values("Datetime")
    df.to_csv("data/whatsapp_data.csv")

def cent_done(current, total, count):
    if current//(total*0.1) == count:
        print(str(round((current/total)*100))+"%")
        '''
        for i in range(2):
            count_word(chat_log[random.randint(1,100)*-1][2], False)
            '''
        return 1
    return 0

def count_word(message, debug=False):
    if debug:
        print(message.strip())
        print(message.split())
        print(len(message.split()))
    words = re.findall("[\w'’:,-]+", message)
    word_count = len(words)
    if debug:
        print(words)
        print(word_count)
    return(word_count)

def file_processor(check_data, file_name):
    finding_joins = []
    print("Parsing file - ", file_name)
    with open(file_name+".txt", encoding="utf8") as f:
        log = f.read()
        timestamps = re.findall(r"\n\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ", log)
        messages = re.split(r"\n\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ", log)[1:]
        count = 1
        for i,timestamp in enumerate(timestamps):
            count += cent_done(i,len(timestamps), count)
            if messages[i].find(":",3,15)>-1:
                msg = messages[i].replace("\n"," ")
                msg = msg.split(":",1)
                check_data = check_data_range(timestamp,check_data)
                if (check_data == True):
                    if exclude_people:
                        if check_excldues(msg[0]):
                            if msg[1][:6] != " POLL:" and len(msg[1][1:]) != 0:
                                add_log(timestamp, msg, chat_log, file_name)
                    else:
                        if msg[1][:6] != " POLL:" and len(msg[1][1:]) != 0:
                                add_log(timestamp, msg, chat_log, file_name)
            else:
                if (messages[i].find("added") > 0) or (messages[i].find("left") > 0) or (messages[i].find("joined") > 0):
                    finding_joins.append((timestamp, messages[i]))
    print("Finished Parsing file -",file_name)
    print()
    for join in finding_joins:
        print(join)

def main():
    check_data = False
    for file_to_process in file_names:
        file_processor(check_data, "data/"+file_to_process)

    #save_to_csv(chat_log)

    print("Finished Parsing")

main()