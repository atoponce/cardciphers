import talon
import scipy, scipy.stats

t = talon.Cipher()
s = scipy.stats

d = [i for i in xrange(1,53)]
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
e_values = scipy.array([expected]*52)
chi = s.chisquare(o_values, f_exp=e_values)

print("Chi-square: {0:.4f}, p-value: {1:.4f}".format(chi[0], chi[1]))
