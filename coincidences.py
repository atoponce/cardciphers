import talon

t = talon.Cipher()

last = -1
count = 0
rounds = 1612000
d = [i for i in xrange(1,53)]
t.shuffle_deck(d)

for i in xrange(rounds):
    out = t.prng(d)
    if out == last:
        count += 1
    last = out

ratio = float(count)/rounds
print("Coincidencs: {0}/{1}".format(count, rounds))
print("Hit Ratio: {0:.12f}".format(ratio))
print("Expected: {0:.12f}".format(1.0/52))
print("Bias: 1/{0:.12f}".format(1/ratio))
