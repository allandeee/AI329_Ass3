mem_depth = 3
bs = '111101'

pairs = ['11', '10', '01', '00']

vals = []
for c1,c2 in zip(bs[0::2], bs[1::2]):
    pair = c1 + c2
    vals.append(pairs.index(pair))

i = 0
ith = 0

while i < mem_depth:
    ith += vals[i] * 4**(mem_depth-(i+1))
    i += 1

print(ith)
