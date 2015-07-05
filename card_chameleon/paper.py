import card_chameleon
import encoder

c = card_chameleon.Cipher()

deck = [i for i in xrange(1,53)]
c.prepare_deck(deck)

ct = ""

passphrase='EUKMKTRVKUMNCTHPIRUANUSDWZZXVDARQVQFQMJRLOFMMZFMXKAAUR'
iv='ESXLGXKILKWLEZIDGAMVIVPBRW'
pt = 'JELLYLIKEABOVETHEHIGHWIRESIXQUAKINGPACHYDERMSKEPTTHECLIMAXOFTHEEXTRAVAGANZAINADAZZLINGSTATEOFFLUXQQ'

for char in passphrase:
    c.prng(deck, char, iv=True)

for char in iv:
    c.prng(deck, char, iv=True)

for char in pt:
    ct += c.prng(deck, char)

print ct
