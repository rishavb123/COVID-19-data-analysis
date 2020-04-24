def read(filename, usa=False, country=None):
    f = open(filename)
    lines = f.readlines()
    ind = 13 if usa else 3 
    ys = [0 for _ in lines[0].split(',')[ind:]]
    if usa: ys += [0]
    for line in lines[1:]:
        l = line.split(',')
        if country == None or l[1].lower() == country.lower():
            l = l[ind:]
            for i in range(len(ys)):
                if not l[i].isdigit(): l[i] = '1'
                ys[i] += float(l[i])
    f.close()
    return ys