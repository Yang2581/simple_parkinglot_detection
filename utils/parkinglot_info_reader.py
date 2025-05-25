import csv

def parkinglot_info_reader(filename):
    data = []
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) == 0:
                continue
            for i in range(len(row)):
                row[i] = eval(row[i])
            data.append(row)
    return data

if __name__ == "__main__":
    data = parkinglot_info_reader('empty.csv')
    print(data)