import csv

def read(filename, usa=False, country=None):
    f = open(filename)
    reader = csv.reader(f)
    fields = next(reader)
    ind = 11 if usa else 3 
    ys = [0 for _ in fields[ind:]]
    num = 0
    for row in reader:
        if country == None or usa or row[1].lower() == country.lower():
            l = row[ind:]
            num += 1
            for i in range(len(ys)):
                # print(i)
                ys[i] += float(l[i])
    f.close()
    return ys