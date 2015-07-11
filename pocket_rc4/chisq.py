import pocket_rc4
import scipy, scipy.stats

t = pocket_rc4.Cipher()
s = scipy.stats

d = [i for i in xrange(1,53)]
t.prepare_deck(d)
t.shuffle_deck(d)

counts = {}
observed = []
expected = 10000
rounds = len(d)*expected

for i in xrange(rounds):
    n = t.prng(d)
    if n not in counts:
        counts[n] = 1
    else:
        counts[n] += 1

for key in sorted(counts):
    observed.append(counts[key])

o_values = scipy.array(observed)
chi = s.chisquare(o_values)

print("{0:.4f}, {1:.4f}".format(chi[0], chi[1]))
