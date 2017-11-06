mem_depth = 3
bs = '000000'

pairs = ['11', '10', '01', '00']

vals = []
for c1,c2 in zip(bs[0::2], bs[1::2]):
    if c1 == '1':
        if c2 == '1':
            vals.append(0)
        else:
            vals.append(1)
    else:
        if c2 == '1':
            vals.append(2)
        elif c2 == '0':
            vals.append(3)

i = 0
ith = 0

while i < mem_depth:
    ith += vals[i] * 4**(mem_depth-(i+1))
    i += 1

print(ith)
