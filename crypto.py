#!/usr/bin/python

import talon
import encoder
import argparse

parser = argparse.ArgumentParser(description='Python implementation of Talon')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--decrypt', help='Decrypt a message')
group.add_argument('-e', '--encrypt', help='Encrypt a message')
parser.add_argument('-p', '--passphrase', help='Private passphrase to key deck')
args = parser.parse_args()

alg = talon.Cipher()
deck = [i for i in xrange(1,53)]

if args.passphrase:
    passphrase = args.passphrase.upper()
    for char in passphrase:
        alg.mix_deck(deck)
        deck = alg.count_cut(deck, encoder.clist.index(char)+1)

if args.encrypt:
    plaintext = args.encrypt.upper()
    encrypted = encoder.encrypt(plaintext, alg, deck)

    ciphertext = ''
    for index, char in enumerate(encrypted):
        if index % 5 < 4:
            ciphertext += char
        else:
            ciphertext += char + ' '
    print(ciphertext)

elif args.decrypt:
    ciphertext = args.decrypt.replace(' ','')
    decrypted = encoder.decrypt(ciphertext, alg, deck)

    plaintext = ''
    for char in decrypted:
        plaintext += char
    print(plaintext)

else:
    print('-e|--encrypt or -d|--decrypt is required')
