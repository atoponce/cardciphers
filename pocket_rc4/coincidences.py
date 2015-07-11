import pocket_rc4

c = pocket_rc4.Cipher()

last = -1
count = 0
rounds = 52*10000
d = [i for i in xrange(1,53)]
c.prepare_deck(d)
for i in xrange(13):
    c.shuffle_deck(d)

for i in xrange(rounds):
    out = c.prng(d)
    if out == last:
        count += 1
    last = out

ratio = float(count)/rounds
print("Coincidencs: {0}/{1}".format(count, rounds))
print("Hit Ratio: {0:.12f}".format(ratio))
print("Expected: {0:.12f}".format(1.0/26))
print("Bias: 1/{0:.12f}".format(1/ratio))
