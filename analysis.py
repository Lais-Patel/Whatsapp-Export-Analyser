import matplotlib.pyplot as plt
from matplotlib.scale import LogScale
from datetime import datetime
import pandas as pd

def read_csv():
    chat_log = pd.read_csv("data/whatsapp_data.csv")
    chat_log["Datetime"] = pd.to_datetime(chat_log["Datetime"])
    chat_log = chat_log.set_index('Datetime')
    return chat_log
    
def print_leaderboard(chat_log):
    name_counts = chat_log.groupby("Name").size().reset_index(name='Total Messages')
    sorted_counts = name_counts.sort_values(by='Total Messages', ascending=False)
    print(sorted_counts)

def plot_messages(chat_log):
    chat_log["Message_Count"] = 1
    for name, group in chat_log.groupby("Name"):
        plt.plot(group.index, group["Message_Count"].cumsum(), label=name)
    plt.yscale("linear")
    plt.legend(title="Name", loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_time_freq(case, chat_log):
    frequency = ""

    match case.lower():
        case "hour":
            frequency = "H"
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


def main():
    chat_log = read_csv()
    chat_log["Message_Count"] = 1
    time = "week"

    fig, graph = plt.subplots(2,2)

    graph[0,0].plot((plot_time_freq(time, chat_log)), marker='.', linestyle='-')

    graph[1,0].plot((plot_time_period(time, chat_log)), marker='.', linestyle='-')

    plot_time_person(time, chat_log, graph, f_or_p="freq", axis="symlog", pos=[0,1])

    plot_time_person(time, chat_log, graph, f_or_p="period", axis="symlog", pos=[1,1])

    plt.show()

main()