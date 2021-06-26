import pickle
import os
import json
import pandas as pd

with open('./imgData/imgData.pickle', 'rb') as handle:
    b = pickle.load(handle)


x = b["img_datas"][0]


def find_total(x):

    lines = []
    for i, v in enumerate(x[1:]):
        if((v[0].lower()).find("total") != -1):
            avr = (v[1][0][1]+v[1][3][1])/2
            line = []
            for c in x[1:]:
                if((c[1][0][1] < int(avr) and c[1][3][1]) > int(avr)):
                    line.append((c[0], c[1][0][0]))
            lines.append(line)

    ttl = 0.00
    for i in lines:
        for l in i:
            if(l[0].find(".") != -1):
                price = ""
                for t in l[0]:
                    if t in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
                        price = price+t
                try:
                    p = float(price)
                    if (p > ttl):
                        ttl = p
                except:
                    pass
    return(ttl)


def find_total_lines(x):

    lines = []
    for i, v in enumerate(x[1:]):
        if((v[0].lower()).find("total") != -1):
            avr = (v[1][0][1]+v[1][3][1])/2
            line = []
            for c in x[1:]:
                if((c[1][0][1] < int(avr) and c[1][3][1]) > int(avr)):
                    line.append((c[0], c[1][0][0]))
            lines.append(line)

            for li in line:
                print(li[0])


entries = sorted(os.listdir('./data/img'))

ordered_data = []
for i in entries:
    ind = b["img_name"].index(i)
    ttl = find_total(b["img_datas"][ind])
    ordered_data.append((i, ttl))


file_names = []
totals = []

sum = 0
for d in ordered_data:
    file_names.append(d[0])
    totals.append(d[1])
    sum += d[1]
file_names.append("Grand Total")
totals.append(sum)

out = pd.DataFrame()
out['File Name'] = file_names
out['total'] = totals
print(out)
out.to_csv('OCR_output.csv', index=False)
