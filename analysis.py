import matplotlib.pyplot as plt
from matplotlib.scale import LogScale
from datetime import datetime
import pandas as pd
import numpy as np
import emoji
import random

def read_csv():
    chat_log = pd.read_csv("data/whatsapp_data.csv")
    chat_log["Datetime"] = pd.to_datetime(chat_log["Datetime"])
    chat_log = chat_log.set_index('Datetime')
    return chat_log
    
def print_leaderboard(chat_log, word=False, letter=False, media=False, edit=False, delete=False):
    name_counts = chat_log[(chat_log['Delete'] != 1) & (chat_log['Media'] != 1)].groupby("Name").agg(Total_Messages=('Name', 'size'), Total_Words=('Word_Count', 'sum'), Total_Letters=('Letter_Count', 'sum')).reset_index()
    name_counts["Media"] = chat_log[chat_log['Media'] == 1].groupby("Name").agg(Media=('Name', 'size')).reset_index()['Media']
    name_counts["Delete"] = chat_log[chat_log['Delete'] == 1].groupby("Name").agg(Delete=('Name', 'size')).reset_index()['Delete'].map('{:.0f}'.format)
    name_counts["Edit"] = chat_log[chat_log['Edit'] == 1].groupby("Name").agg(Edit=('Name', 'size')).reset_index()['Edit'].map('{:.0f}'.format)
    name_counts["Avg_Words_per_Msg"] = (name_counts["Total_Words"]/name_counts["Total_Messages"]).round(4)
    name_counts["Avg_Letters_per_Word"] = (name_counts["Total_Letters"]/name_counts["Total_Words"]).round(4)

    columns = ['Name', 'Total_Messages']
    if word:
        columns.extend(['Total_Words', 'Avg_Words_per_Msg'])
    if letter:
        columns.extend(['Total_Letters', 'Avg_Letters_per_Word'])
    if media:
        columns.append('Media')
    if edit:
        columns.append('Edit')
    if delete:
        columns.append('Delete')
    
    sorted_counts = name_counts[columns].sort_values(by="Total_Messages", ascending=False).fillna(0)
    print(sorted_counts.to_string(index=False))

def plot_messages(chat_log, Name="", word=False):
    if word:
        messageOrWord = "Word_Count"
    else:
        chat_log["Message_Count"] = 1
        messageOrWord = "Message_Count"

    for name, group in chat_log.groupby("Name"):
        if Name == "" or name in Name:
            plt.plot(group.index, group[messageOrWord].cumsum(), label=name)
    
    plt.yscale("linear")
    plt.legend(title="Name", loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_time_freq(case, chat_log):
    frequency = ""

    match case.lower():
        case "hour":
            frequency = "h"
        case "day":
            frequency = "D"
        case "week":
            frequency = "W"
        case "month":
            frequency = "M"
        case "year":
            frequency = "Y"

    grouped_data = chat_log.groupby(pd.Grouper(freq=frequency))["Message_Count"].sum()

    return grouped_data

def plot_time_period(case, chat_log):
    chat_log = chat_log.drop("Message", axis='columns')
    chat_log = chat_log.drop("Name", axis='columns')

    match case.lower():
        case "hour":
            grouped_data = chat_log.groupby([chat_log.index.hour]).sum()
        case "day":
            grouped_data = chat_log.groupby([chat_log.index.day]).sum()
        case "week":
            grouped_data = chat_log.groupby([chat_log.index.weekday]).sum()
        case "month":
            grouped_data = chat_log.groupby([chat_log.index.month]).sum()
        case "year":
            grouped_data = chat_log.groupby([chat_log.index.year]).sum()

    return grouped_data

def plot_time_person(case, chat_log, graph, f_or_p="period", axis="linear", pos=[0,0]):

    for name, group in chat_log.groupby("Name"):
        if f_or_p == "period":
            grouped_data =  plot_time_period(case,group)
        elif f_or_p == "freq":
            grouped_data =  plot_time_freq(case,group)
        print(grouped_data)
        graph[pos[0],pos[1]].plot(grouped_data.index, grouped_data, marker='.', linestyle='-', label=name)

    graph[pos[0],pos[1]].set_yscale(axis)
    box = graph[pos[0],pos[1]].get_position()
    graph[pos[0],pos[1]].set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    graph[pos[0],pos[1]].legend(title="Name", loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=6)

def four_graphs(chat_log, time):
    fig, graph = plt.subplots(2,2)

    graph[0,0].plot((plot_time_freq(time, chat_log)), marker='.', linestyle='-')

    graph[1,0].plot((plot_time_period(time, chat_log)), marker='.', linestyle='-')

    plot_time_person(time, chat_log, graph, f_or_p="freq", axis="symlog", pos=[0,1])

    plot_time_person(time, chat_log, graph, f_or_p="period", axis="symlog", pos=[1,1])

    plt.show()

def percentage_total(chat_log, Name):
    messages_sent = chat_log.groupby('Name')['Message_Count'].sum()[Name]
    total_messages_sent = len(chat_log)
    percentage_sent = (messages_sent/total_messages_sent) * 100
    return round(percentage_sent, 3)

def peak_time(name_log, name, time):
    name_log = name_log.drop("Message", axis='columns').drop("Name", axis='columns')

    match time.lower():
        case "hour":
            data = name_log.groupby([name_log.index.hour]).sum()
            return data
        case "day":
            data = name_log.groupby(pd.Grouper(freq='D'))["Message_Count"].sum()
        case "week":
            data = name_log.groupby(pd.Grouper(freq='W'))["Message_Count"].sum()

    message_time = []
    for index, item in data.items():
        message_time.append((item, index))
    message_time.sort(reverse=True)

    top_time = []
    for i in range(3):
        top_time.append({ message_time[i][1] : message_time[i][0] })
        
    return top_time
    
def streak_finder(chat_log, Name):
    streak_dict = {}
    for name,log in chat_log.groupby("Name"):
        streak = 0
        max_streak = 0
        prior_date = log.index[0]
        # print(name)

        for time in log.index:
            difference = (time - prior_date).days

            if difference == 0:
                continue
            elif difference == 1:
                streak += 1
                # print(difference,"diff", streak, "s", max_streak, "ms", time)
            elif difference > 1:
                streak = 1
                # print(difference,"diff", streak, "s", max_streak, "ms", time)
            
            if max_streak < streak:
                max_streak = streak
                max_streak_date = time
            
            prior_date = time
            
        streak_dict[name]= (max_streak, max_streak_date)

    lazy = []

    for data in streak_dict:
        lazy.append([streak_dict[data],data])
    lazy.sort()
    for data in lazy:
        print(data)

def colour_calendar(chat_log, Name):
    for name,log in chat_log.groupby("Name"):
        if name == Name:
            grouped_data = log.groupby(pd.Grouper(freq="D"))["Message_Count"].sum()
            grouped_data = grouped_data.reset_index()
            grouped_data["Datetime"] = pd.to_datetime(grouped_data["Datetime"])

            grouped_data["year"] = grouped_data["Datetime"].dt.year
            grouped_data["month"] = grouped_data["Datetime"].dt.month
            grouped_data["week"] = grouped_data["Datetime"].dt.strftime('%W').astype(int)
            grouped_data["day_name"] = grouped_data["Datetime"].dt.dayofweek
            grouped_data["day"] = grouped_data["Datetime"].dt.day

            fig, axes = plt.subplots(grouped_data["year"].nunique(), 1, figsize=(12,10))

            for i,year in enumerate(grouped_data["year"].unique()):
                heatmap_data = grouped_data[grouped_data["year"]==year].pivot_table(index="day_name",columns="week",values="Message_Count")
                heatmap_data = heatmap_data.reindex(index=list(range(7)), columns=list(range(54)), fill_value=np.nan).replace(0, np.nan)
                if grouped_data["year"].nunique() == 1:
                    g = axes.imshow(heatmap_data, cmap='Greens')
                else:
                    g = axes[i].imshow(heatmap_data, cmap='Greens')

            fig.colorbar(g, ax=axes, label='Messages Sent that Day')
            plt.show()


            ''' Will leave this as an idea for later
                max = grouped_data.quantile(0.9)
                print("max",max)
                for x in grouped_data.nlargest(10):
                print(name,x,(x*1/max).round())'''

def emoji_count(chat_log):
    people_dict = {}
    for name,log in chat_log.groupby("Name"):
        emoji_count_dict = {}
        for message in log["Message"]:
            try:
                for emojis in emoji.emoji_list(message):
                    char = emoji.emojize(emojis["emoji"])
                    if char not in ["🟩","⬛","🟨","⬜","🟪","🟦","🟡","🔵"]:
                        if char in emoji_count_dict:
                            emoji_count_dict[char] += 1
                        else:
                            emoji_count_dict[char] = 1
            except:
                pass
        people_dict[name] = dict(sorted(emoji_count_dict.items(), key=lambda x: x[1], reverse=True)[:5])
    for name, items in people_dict.items():
        print(name,items)

def main():
    chat_log = read_csv()
    chat_log["Message_Count"] = 1
    
    colour_calendar(chat_log, "Lais Patel")

    #print_leaderboard(chat_log, True)
    #plot_messages(chat_log)
    #streak_finder(chat_log, "Lais Patel")
    

main()

'''
done - percentage of total messages being yours
- most common emojis you sent
- most common stickers you sent (ext)
done - peak time you messaged at + graph
done - peak day and week you messaged + how many
done your longest message you sent
- average messages per day
done average message length by words
- longest concurrent time spent in chat
- how many minutes spent in chat
done longest streak of days messaging
done avg word length
''' 