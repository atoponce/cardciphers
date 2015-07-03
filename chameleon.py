import card_chameleon

c = card_chameleon.Cipher()
deck = [i for i in xrange(1,53)]
c._prepare_deck(deck)

def encrypt(deck, letter):
    return c.prng(deck, letter)

def decrypt(deck, letter):
    return c.prng(deck, letter)

print decrypt(deck,'A')
