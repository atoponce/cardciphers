import random
import string

plist = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&()-=+:,./? ')
clist = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

def get_keystream(message, alg, deck):
    outs = []
    for i in xrange(len(message)):
        outs.append(alg.prng(deck))
    return outs
    
def pad_message(message):
    pad = len(message) % 5
    if pad is 0:
        message += '55555'
    elif pad is 1:
        message += '4444'
    elif pad is 2:
        message += '333'
    elif pad is 3:
        message += '22'
    else:
        message += '1'
    return message

def unpad_message(message):
    pad = message[-1:]
    if '1' in pad:
        message = message[:-1]
    elif '2' in pad:
        message = message[:-2]
    elif '3' in pad:
        message = message[:-3]
    elif '4' in pad:
        message = message[:-4]
    else:
        message = message[:-5]
    return message

def create_iv():
    r = random.SystemRandom()
    return "".join(r.choice(string.ascii_letters) for i in xrange(5))

def encrypt(message, alg, deck):
    ct = []
    iv = create_iv()
    
    for char in message:
        if not char in plist:
            message = message.replace(char, '')
    
    for char in iv:
        alg.mix_deck(deck)
        deck = alg.count_cut(deck, clist.index(char) + 1)

    message = pad_message(message)
    keystream = get_keystream(message, alg, deck)

    for num, char in zip(keystream, message):
        ct.append((num + plist.index(char)) % 52)

    for index, value in enumerate(ct):
        ct[index] = clist[value]

    return list(iv) + ct

def decrypt(message, alg, deck):
    pt = []
    iv = message[:5]
    message = message[5:]

    for char in iv:
        alg.mix_deck(deck)
        deck = alg.count_cut(deck, clist.index(char) + 1)

    keystream = get_keystream(message, alg, deck)

    for num, char in zip(keystream, message):
        pt.append(((clist.index(char)) - num) % 52)

    for index, value in enumerate(pt):
        pt[index] = plist[value]

    return unpad_message(pt)
