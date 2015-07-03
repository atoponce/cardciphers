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

def _unpad_message(message):
    """ Remove the padding off a decrypted ciphertext message.

    Args:
        message (str): The full decrypted ciphertext message.

    Returns:
        str: The decrypted message without PKCS#7 padding.

    """

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

def _create_iv(n):
    """ Create a random initialization vector.

    Prepend a plaintext message with 5 random characters in the same ciphertext
    character base as the rest of the ciphertext.

    Args:
        n (int): The number of random characters to generate.

    Returns:
        str: An initialization vector string.

    """

    r = random.SystemRandom()
    return "".join(r.choice(string.ascii_letters) for i in xrange(n))

def encrypt(message, alg, deck, n):
    """ Encrypt a plaintext message.

    Args:
        message (str): The plaintext message.
        alg (object): The specific cipher object.
        deck (list): A full 52-card deck. State is maintained.
        n (int): The number of initialization vector characters to generate.

    Returns:
        str: An encrypted message prepended with an initialization vector.

    """

    ct = []
    iv = _create_iv(n)
    
    for char in message:
        if not char in plist:
            message = message.replace(char, '')
    
    for char in iv:
        alg.mix_deck(deck)
        deck = alg.count_cut(deck, clist.index(char) + 1)

    message = _pad_message(message)
    keystream = _get_keystream(message, alg, deck)

    for num, char in zip(keystream, message):
        ct.append((num + plist.index(char)) % 52)

    for index, value in enumerate(ct):
        ct[index] = clist[value]

    return list(iv) + ct

def decrypt(message, alg, deck, n):
    """ Decrypt a ciphertext message.

    Args:
        message (str): The ciphertext message.
        alg (object): The specific cipher object.
        deck (list): A full 52-card deck. State is maintained.
        n (int): The number of characters of the initialization vector.

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
        pt.append(((clist.index(char)) - num) % 52)

    for index, value in enumerate(pt):
        pt[index] = plist[value]

    return _unpad_message(pt)
