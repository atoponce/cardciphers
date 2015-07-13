import random
import string

clist = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

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

def _create_iv(n):
    """ Create a random initialization vector.

    Prepend a plaintext message with 5 random characters in the same ciphertext
    character base as the rest of the ciphertext.

    Args:
        n (int): The number of initialization vector characters to generate.

    Returns:
        str: An initialization vector string.

    """

    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    r = random.SystemRandom()
    return ''.join(r.sample(chars, n))

def encrypt(message, alg, deck, n=26):
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
        if not char in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            message = message.replace(char, '')

    for char in iv:
        c_loc = alg.find_black_card(deck, char)
        alg.mix_deck(deck, c_loc-1, iv=True)

    msg = iv + message
    message = _pad_message(msg)
    message = message[n:] # strip iv for encryption
    keystream = _get_keystream(message, alg, deck)

    for num, char in zip(keystream, message):
        ct.append((num + clist.index(char)) % 26)

    for index, value in enumerate(ct):
        ct[index] = clist[value]

    return list(iv) + ct

def decrypt(message, alg, deck, n=26):
    """ Decrypt a ciphertext message.

    Args:
        message (str): The ciphertext message.
        alg (object): The specific cipher object.
        deck (list): A full 52-card deck. State is maintained.
        n (int): The number of initialization vector characters to generate.

    Returns:
        str: An decrypted message without the initialization vector.

    """
    pt = []
    iv = message[:n]
    message = message[n:]

    for char in iv:
        c_loc = alg.find_black_card(deck, char)
        alg.mix_deck(deck, c_loc-1, iv=True)

    keystream = _get_keystream(message, alg, deck)

    for num, char in zip(keystream, message):
        pt.append(((clist.index(char)) - num) % 26)

    for index, value in enumerate(pt):
        pt[index] = clist[value]

    return _unpad_message(pt)
