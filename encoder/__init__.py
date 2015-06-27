def encrypt(message, keystream):
    plist = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&()-=+:,./? ')
    clist = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    
    for char in message:
        if not char in plist:
            message = message.replace(char, '')

    ct = []

    for num, char in zip(keystream, message):
        ct.append((num + plist.index(char)) % 52)

    for index, value in enumerate(ct):
        ct[index] = clist[value]

    return ct

def decrypt(message, keystream):
    clist = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    plist = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&()-=+:,./? ')

    pt = []

    for num, char in zip(keystream, message):
        pt.append((clist.index(char) - num) % 52)

    for index, value in enumerate(pt):
        pt[index] = plist[value]

    return pt
