import card_chameleon

c = card_chameleon.Cipher()
string = ""

def reset_deck():
    deck = [i for i in xrange(1,53)]
    c._prepare_deck(deck)
    return deck
    
def encrypt(deck, letter):
    return c.prng(deck, letter)

def decrypt(deck, letter):
    return c.prng(deck, letter)

deck = reset_deck()
for char in "AARON":
    string += encrypt(deck,char)
    print deck

print string

string = ""
print ""

deck = reset_deck()
for char in "AARNA":
    string += decrypt(deck,char)

print string
