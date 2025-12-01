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

def plot_time_period(case, chat_log):
    chat_log["Message_Count"] = 1
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

    grouped_data.plot(marker='o', linestyle='-')
    plt.tight_layout()


def plot_time(case, chat_log):
    chat_log["Message_Count"] = 1
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


    grouped_data.plot(marker='o', linestyle='-')
    plt.tight_layout()


def plot_period(case, chat_log):
    tally = {}
    match case:
        case "week":
            for time in chat_log.index:
                print(time.weekday())
                try:
                    tally[time.weekday()] += 1
                except:
                    tally[time.weekday()] = 1
            print(tally)
        case "hour":
            for time in chat_log["Datetime"]:
                try:
                    tally[time.hour] += 1
                except:
                    tally[time.hour] = 1
            print(tally)


def main():
    chat_log = read_csv()
    plot_time_period("HOUR",chat_log)
    plot_time("HOUR",chat_log)
    plt.show()

main()