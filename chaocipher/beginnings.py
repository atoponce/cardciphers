import chaocipher

c = chaocipher.Cipher()
passphrase = 'CARDCIPHERCARDCIPHER'
deck = [i for i in xrange(1,53)]
cards = (
    'AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC',
    'AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD',
    'AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH',
    'AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS'
    )

print "Default unkeyed deck:"
for card in deck:
    print cards[card-1],

print "\n"

c.prepare_deck(deck)

print "Unkeyed Chaocipher deck (left on-top-of right):"
for card in deck:
    print cards[card-1],

print "\n"

for char in passphrase:
    c.prng(deck, char)

print "Keyed Chaocipher deck (left on-top-of right):"
for card in deck:
    print cards[card-1],
