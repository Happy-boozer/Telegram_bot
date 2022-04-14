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
        T = []
        for i in ['о', 'к', 'р', 'а', 'с']:
            if i in list(k.lower()):
                T.append(True)
            else:
                T.append(False)
        if k.lower().find("п") != -1 and all(T):
            i = k.lower().find("п")
            k = k[i+1::]
        for j in val:
            if j.lower() == k.lower():
                price += p_b[j]
    if price == 0:
        update.message.reply_text("")
    else:
        update.message.reply_text(price)
