import random
import string

plist = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#$%&()-=+:,./? ')
clist = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

def _get_keystream(message, alg, deck):
    """ Generate a pseudorandom keystream of integers

    Args:
        message (str): The full plaintext or ciphertext message.
        alg (object): The specific cipher object.
        deck (list): A full 52-card deck. State is maintained.

    Returns:
        list: A list pseudorandom numbers

    """

    outs = []
    for i in xrange(len(message)):
        outs.append(alg.prng(deck))
    return outs
    
def _pad_message(message):
    """ A PKCS#7 padding implementation for the end of the plaintext message.

    Args:
        message (str): The full plaintext message.

    Returns:
        str: A PKCS#7 padded message.

    """

    pad = len(message) % 5
    if pad is 0:
        message += 'ZZZZZ'
    elif pad is 1:
        message += 'YYYY'
    elif pad is 2:
        message += 'XXX'
    elif pad is 3:
        message += 'WW'
    else:
        message += 'V'
    return message

def _unpad_message(message):
    """ Remove the padding off a decrypted ciphertext message.

    Args:
        message (str): The full decrypted ciphertext message.

    Returns:
        str: The decrypted message without PKCS#7 padding.

    """

    pad = message[-1:]
    if 'V' in pad:
        message = message[:-1]
    elif 'W' in pad:
        message = message[:-2]
    elif 'X' in pad:
        message = message[:-3]
    elif 'Y' in pad:
        message = message[:-4]
    elif 'Z' in pad:
        message = message[:-5]
    return message

def _create_iv(n, base):
    """ Create a random initialization vector.

    Prepend a plaintext message with 5 random characters in the same ciphertext
    character base as the rest of the ciphertext.

    Args:
        n (int): The number of random characters to generate.
        base (int): The input/output base of the plaintext/ciphertext.

    Returns:
        str: An initialization vector string.

    """

    r = random.SystemRandom()
    if base is 26:
        return "".join(r.choice(string.uppercase) for i in xrange(n))
    else:
        return "".join(r.choice(string.ascii_letters) for i in xrange(n))

def encrypt(message, alg, deck, n, base):
    """ Encrypt a plaintext message.

    Args:
        message (str): The plaintext message.
        alg (object): The specific cipher object.
        deck (list): A full 52-card deck. State is maintained.
        n (int): The number of initialization vector characters to generate.
        base (int): The input/output base of the plaintext/ciphertext.

    Returns:
        str: An encrypted message prepended with an initialization vector.

    """

    ct = []
    iv = _create_iv(n, base)
    
    for char in message:
        if not char in plist[:base]:
            message = message.replace(char, '')
    
    for char in iv:
        alg.mix_deck(deck)
        deck = alg.count_cut(deck, clist.index(char) + 1)

    message = _pad_message(message)
    keystream = _get_keystream(message, alg, deck)

    for num, char in zip(keystream, message):
        ct.append((num + plist.index(char)) % base)

    for index, value in enumerate(ct):
        ct[index] = clist[value]

    return list(iv) + ct

def decrypt(message, alg, deck, n, base):
    """ Decrypt a ciphertext message.

    Args:
        message (str): The ciphertext message.
        alg (object): The specific cipher object.
        deck (list): A full 52-card deck. State is maintained.
        n (int): The number of characters of the initialization vector.
        base (int): The input/output base of the plaintext/ciphertext.

    Returns:
        str: An decrypted message without the initialization vector.

    """
    pt = []
    iv = message[:n]
    message = message[n:]

    for char in iv:
        alg.mix_deck(deck)
        deck = alg.count_cut(deck, clist.index(char) + 1)

    keystream = _get_keystream(message, alg, deck)

    for num, char in zip(keystream, message):
        pt.append(((clist.index(char)) - num) % base)

    for index, value in enumerate(pt):
        pt[index] = plist[value]

    return _unpad_message(pt)
