def encrypt(message, base, keystream):
    if base == 26:
        s = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    if base == 52:
        s = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&()-=+:,./?')

    ct = []

    for n, c in zip(keystream, message):
        ct.append((n + s.index(c)) % base)

    for i, v in enumerate(ct):
        ct[i] = s[v]

    return ct

def decrypt(message, base, keystream):
    if base == 26:
        s = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    if base == 52:
        s = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&()-=+:,./?')

    pt = []
    for n, c in zip(keystream, message):
        pt.append((s.index(c) - n) % base)

    for i, v in enumerate(pt):
        pt[i] = s[v]

    return pt
