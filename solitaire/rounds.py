import encoder
import solitaire

c = solitaire.Cipher()
d = [i for i in xrange(1,55)] # must fill with values 1-54
#c.shuffle_deck(d)

faces = [None] * 54
cards = (
    'AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC',
    'AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD',
    'AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH',
    'AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS',
    'JA','JB',
    )
outs = []

rounds = 50

print "Starting deck:"
for index, value in enumerate(d):
    faces[index] = cards[value-1]

for face in faces:
    print face,
print ""

print "Deck rounds:"
for i in xrange(rounds):
    outs.append(c.prng(d))

    for index, value in enumerate(d):
        faces[index] = cards[value-1]

    for face in faces:
        print face,
    print ""

print "Keystream:"
for out in outs:
    print out,
print ""
