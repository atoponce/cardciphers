import card_chameleon

deck = [i for i in xrange(1,53)]

c = card_chameleon.Cipher()

c.shuffle_deck(deck)

print deck
