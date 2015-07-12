#!/usr/bin/python

import solitaire
import encoder
import argparse

parser = argparse.ArgumentParser(description='Python implementation of Solitaire')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--decrypt', help='Decrypt a message')
group.add_argument('-e', '--encrypt', help='Encrypt a message')
parser.add_argument('-p', '--passphrase', help='Private passphrase to key deck')
parser.add_argument('-k', '--key', help='Private comma-separated deck order.')
args = parser.parse_args()

last = -1
coincidences = 0
alg = solitaire.Cipher()

deck = [i for i in xrange(1,55)]
#alg.shuffle_deck(deck)
#alg.prepare_deck(deck)

if args.key:
    deck = []
    cards = args.key.split(',')

    if not ',' in args.key:
        parser.error('All 54 cards must be comma-separated.')

    if not args.key.replace(' ','').replace(',','').isdigit():
        parser.error('The deck must uniquely comprise of digits 1-54.')

    # bulid deck
    for card in cards:
        deck.append(int(card))

    # more tests
    if len(deck) != 54:
        parser.error('The deck must be exactly 54 cards in total.')

    if sorted(deck)[0] < 1 or sorted(deck)[53] > 54:
        parser.error('The deck must use uniquely the values 1-54 inclusively.')

    for card in deck:
        out = card
        if out == last:
            coincidences += 1
        last = out

    if coincidences:
        parser.error('The deck must contain all unique values of 1-54.')

if args.passphrase:
    passphrase = args.passphrase.upper().replace(' ','')
    for char in passphrase:
        alg.mix_deck(deck, encoder.clist.index(char)+1)

if args.encrypt:
    plaintext = args.encrypt.upper()
    encrypted = encoder.encrypt(plaintext, alg, deck, 5)

    ciphertext = ''
    for index, char in enumerate(encrypted):
        if index % 5 < 4:
            ciphertext += char
        else:
            ciphertext += char + ' '
    print(ciphertext)

elif args.decrypt:
    ciphertext = args.decrypt.replace(' ','')
    decrypted = encoder.decrypt(ciphertext, alg, deck, 5)

    plaintext = ''
    for char in decrypted:
        plaintext += char
    print(plaintext)

else:
    print('-e|--encrypt or -d|--decrypt is required')
