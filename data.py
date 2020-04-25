import csv
import numpy as np

global_files = [
    "./data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "./data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
    "./data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
]
global_names = [
    "cases",
    "death",
    "recovered"
]

us_files = [
    "./data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv",
    "./data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
]

us_names = [
    "cases",
    "death"
]

def get_structured_data():
    data = {}
    data["Global"] = {}
    for filename, name in zip(global_files, global_names):
        with open(filename) as f:
            reader = csv.reader(f)
            fields = next(reader)
            data["Global"][name] = np.zeroes(len(fields) - 4)
            for row in reader:
                if row[1] not in data:
                    data[row[1]] = {}
                if name not in data[row[1]]:
                    data[row[1]][name] = np.zeros(len(fields) - 4)
                data[row[1]][name] += [float(y) for y in row[4:]]
                data["Global"][name] += [float(y) for y in row[4:]]
    data["United States"] = {}
    for filename, name in zip(us_files, us_names):
        with open(filename) as f:
            reader = csv.reader(f)
            fields = next(reader)
            ind = 12 if filename == './data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv' else 11
            data["United States"][name] = np.zeros(len(fields) - ind)
            for row in reader:           
                data["United States"][name] += [float(y) for y in row[ind:]]
    return data

def get_raw_data():
    data = {
        "global": {},
        "usa": {}
    }

    for name in global_names:
        data["global"][name] = {}
    for filename, name in zip(global_files + us_files, global_names + us_names):
        with open(filename) as f:
            reader = csv.reader(f)
            fields = next(reader)
            t = "global" if filename in global_files else "usa"
            data[t][name]["fields"] = fields
            data[t][name]["values"] = []
            for row in reader:
                data[t][name]["values"].append(row)
    
    return data

def read(filename, usa=False, country=None):
    f = open(filename)
    reader = csv.reader(f)
    fields = next(reader)
    ind = 11 if usa else 4
    if filename == './data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv':
        ind += 1
    ys = [0 for _ in fields[ind:]]
    num = 0
    for row in reader:
        if country == None or usa or row[1].lower() == country.lower():
            l = row[ind:]
            num += 1
            for i in range(len(ys)):
                ys[i] += float(l[i])
    f.close()
    return ys

if __name__ == "__main__":
    data = get_structured_data()
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data["United States"])