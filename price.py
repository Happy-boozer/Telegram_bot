import json
with open('base.json') as base:
    p_b = json.load(base)
val = []
for i in p_b:
    val.append(i)

def price(update, context):
    price = 0
    posns = update.message.text.split(', ')
    for k in posns:
        if k.lower().find("п") != -1:
            i = k.lower().find("п")
            r = k[i+1::]
            print(r)
    for j in val:
        if r == j:
            price += p_b[j]