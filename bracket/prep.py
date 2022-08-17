with open('./draw.txt', 'r') as f:
    with open('./oop.csv', 'w') as d:
        for l in f.readlines():
            line = l.split()
            print(line)
            
            ol = [t for t in line if '(' not in t]
            out = ' '.join(ol) + '\n'

            d.write(out)