from talon import Talon

t = Talon()
d = [i for i in xrange(52)]

rounds = 50

for n in xrange(rounds):
    print t.algorithm(d),

print "\n{0}".format(d)
