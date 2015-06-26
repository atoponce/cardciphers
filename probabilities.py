import talon

t = talon.Cipher()
d = [i for i in xrange(1,53)]
#t.shuffle_deck(d)

counts = {}
rounds = 1612000

for i in xrange(rounds):
    n = t.prng(d)
    if n not in counts:
        counts[n] = 1
    else:
        counts[n] += 1

expected = rounds / 52.0

for key in sorted(counts):
    count = counts[key]
    #print("{0}: {1} ({2:.12f})".format(key, count, float(count/expected - 1)))
    print("{0},{1}".format(key, count))
