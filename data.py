def read(filename, country=None):
    f = open(filename)
    lines = f.readlines()
    ys = [0 for _ in lines[0].split(',')[3:]]
    for line in lines[1:]:
        l = line.split(',')
        if country == None or l[1].lower() == country.lower():
            l = l[3:]
            for i in range(len(ys)):
                ys[i] += float(l[i])
    f.close()