import card_chameleon
import encoder

pt = "JELLYLIKEABOVETHEHIGHWIRE"*26000
ct = ""

c = card_chameleon.Cipher()

deck = [i for i in xrange(1,53)]
c.prepare_deck(deck)

for char in pt:
    ct += c.prng(deck, char)

print ct
