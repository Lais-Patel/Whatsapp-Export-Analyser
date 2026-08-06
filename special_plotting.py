import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def read_csv():
    data = pd.read_csv("data/joining_data.csv")
    data["Datetime"] = pd.to_datetime(data["Datetime"])
    data = data.set_index('Datetime')
    return data

def plot_joins(data):
    plt.step(data.index,data["group_size"], where="post")
    plt.show()

def main():
    data = read_csv()
    plot_joins(data)

main()