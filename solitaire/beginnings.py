import pocket_rc4

c = pocket_rc4.Cipher()
passphrase = 'CARDCIPHERCARDCIPHER'
deck = [i for i in xrange(1,53)]
cards = (
    'AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH',
    'AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD',
    'AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS',
    'AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC'
    )

print "Default unkeyed deck:"
for card in deck:
    print cards[card-1],

print "\n"

c.prepare_deck(deck)

print "Unkeyed Pocket-RC4 deck:"
for card in deck:
    print cards[card-1],

print "\n"

for char in passphrase:
    c_loc = c.find_black_card(deck, char)
    c.mix_deck(deck, c_loc-1, iv=True)

print "Keyed Pocket-RC4 deck:"
for card in deck:
    print cards[card-1],
