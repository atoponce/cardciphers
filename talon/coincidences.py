import talon
import encoder

# setting up the ciphertext
ciphertext = ''
keyphrase = 'CARDCIPHERCARDCIPHER'
plaintext = "ABAB"*25
plaintext *= 5200
deck = [i for i in xrange(1,53)]

c = talon.Cipher()
#c.prepare_deck(deck)

for char in keyphrase:
    c.mix_deck(deck)
    deck = c.count_cut(deck, encoder.plist.index(char)+1)

ct_list = encoder.encrypt(plaintext, c, deck, 0)

for char in ct_list:
    ciphertext += char

# finding the index of coincidence
n = len(ciphertext)
freq = {}
alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
freqsum = 0.0
last = -1
count = 0

for char in ciphertext:
    if not char in freq:
        freq[char] = 1
    else:
        freq[char] += 1
    if char == last:
        count += 1
    last = char

for char in alphabet:
    freqsum += freq[char] * (freq[char] - 1)

ic = freqsum / (n * (n - 1))

ratio = float(count)/len(ciphertext)
print("Coincidences: {0}/{1}".format(count, len(ciphertext)))
print("Index: {0}".format(ic))
print("Hit Ratio: {0:.12f}".format(ratio))
print("Expected: {0:.12f}".format(1.0/len(alphabet)))
print("Bias: 1/{0:.12f}".format(1/ic))
