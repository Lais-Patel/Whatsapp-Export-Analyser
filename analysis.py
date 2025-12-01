import matplotlib.pyplot as plt
from matplotlib.scale import LogScale
from datetime import datetime
import pandas as pd

def read_csv():
    chat_log = pd.read_csv("data\whatsapp_data.csv")
    chat_log["Datetime"] = pd.to_datetime(chat_log["Datetime"])
    chat_log = chat_log.set_index("Datetime")
    return chat_log
    
def print_leaderboard(chat_log):
    name_counts = chat_log.groupby("Name").size().reset_index(name='Total Messages')
    sorted_counts = name_counts.sort_values(by='Total Messages', ascending=False)
    print(sorted_counts)

def plot_messages(chat_log):
    chat_log["Message_Count"] = 1
    chat_log["Cum_Messages"] = chat_log.groupby("Name")["Message_Count"].cumsum()
    for name, group in chat_log.groupby("Name"):
        plt.plot(group.index, group["Message_Count"].cumsum(), label=name)
    plt.yscale("log")
    plt.legend(title="Name", loc='upper left')
    plt.show()

def main():
    chat_log = read_csv()
    plot_messages(chat_log)

main()