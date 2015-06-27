import talon
import encoder

def get_keystream(message):
    t = talon.Cipher()
    d = [i for i in xrange(1,53)]
    outs = []

    for i in xrange(len(message)):
        outs.append(t.prng(d))
    
    return outs

plain = 'Apache/2.2.22 (Debian) Server at ae7.st Port 80'
print(plain)
plain = plain.upper()
pad = 5 - len(plain) % 5
plain = plain + 'X' * pad

outs = get_keystream(plain)
ct = encoder.encrypt(plain, outs)

cipher = ''
for i, c in enumerate(ct):
    if i % 5 < 4:
        cipher += c
    else:
        cipher = cipher + c + ' '

print('Encrypted: {0}'.format(cipher))

cipher = cipher.replace(' ','')

outs = get_keystream(cipher)
pt = encoder.decrypt(cipher, outs)

plain = ''
for c in pt:
    plain += c
    
print('Decrypted: {0}'.format(plain))
