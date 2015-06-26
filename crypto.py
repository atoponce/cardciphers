import talon
import encoder

def get_keystream(message):
    t = talon.Cipher()
    d = [i for i in xrange(1,53)]
    #d = [3, 44, 23, 42, 43, 22, 31, 25, 6, 7, 5, 32, 51, 28, 45, 40, 37, 16,
    #     17, 50, 19, 10, 0, 46, 47, 38, 21, 20, 34, 35, 1, 49, 18, 41, 11, 33,
    #     15, 2, 39, 26, 4, 36, 24, 8, 29, 30, 48, 13, 12, 27, 9, 14]
    outs = []

    for i in xrange(len(message)):
        outs.append(t.prng(d))
    
    return outs

plain = 'python crypto'
print(plain)
plain = plain.upper().replace(' ','')
pad = 5 - len(plain) % 5
plain = plain + 'X' * pad

outs = get_keystream(plain)
ct = encoder.encrypt(plain, 26, outs)

cipher = ''
for i, c in enumerate(ct):
    if i % 5 < 4:
        cipher += c
    else:
        cipher = cipher + c + ' '

print('Encrypted: {0}'.format(cipher))

cipher = cipher.upper().replace(' ','')

outs = get_keystream(cipher)
pt = encoder.decrypt(cipher, 26, outs)

plain = ''
for c in pt:
    plain += c
    
print('Decrypted: {0}'.format(plain))
