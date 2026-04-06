file_name = "data"
start = 179726
end = 181137

def main():
    with open(file_name+".txt", encoding="utf8") as f:
        log = f.readlines()
        print(log[start])
        print(log[end])
    
    with open(file_name+"_remove.txt", "w", encoding="utf8") as f:
        for line in log[start:end]:
            f.write(line)

main()