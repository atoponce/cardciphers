#!/usr/bin/python

import pocket_rc4
import encoder
import argparse

parser = argparse.ArgumentParser(description='Python implementation of Pocket-RC4')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--decrypt', help='Decrypt a message')
group.add_argument('-e', '--encrypt', help='Encrypt a message')
parser.add_argument('-p', '--passphrase', help='Private passphrase to key deck')
parser.add_argument('-k', '--key', help='Private comma-separated deck order.')
args = parser.parse_args()

last = -1
coincidences = 0
alg = pocket_rc4.Cipher()

deck = [i for i in xrange(1,53)]
#alg.shuffle_deck(deck)
alg.prepare_deck(deck)

if args.key:
    deck = []
    cards = args.key.split(',')

    if not ',' in args.key:
        parser.error('All 52 cards must be comma-separated.')

    if not args.key.replace(' ','').replace(',','').isdigit():
        parser.error('The deck must uniquely comprise of digits 1-52.')

    # bulid deck
    for card in cards:
        deck.append(int(card))

    # more tests
    if len(deck) != 52:
        parser.error('The deck must be exactly 52 cards in total.')

    if sorted(deck)[0] < 1 or sorted(deck)[51] > 52:
        parser.error('The deck must use uniquely the values 1-52 inclusively.')

    for card in deck:
        out = card
        if out == last:
            coincidences += 1
        last = out

    if coincidences:
        parser.error('The deck must contain all unique values of 1-52.')

if args.passphrase:
    passphrase = args.passphrase.upper().replace(' ','')
    for char in passphrase:
        c_loc = alg.find_black_card(deck, char)
        alg.mix_deck(deck, c_loc-1, iv=True)

if args.encrypt:
    plaintext = args.encrypt.upper()
    encrypted = encoder.encrypt(plaintext, alg, deck, n=26)

    ciphertext = ''
    for index, char in enumerate(encrypted):
        if index % 5 < 4:
            ciphertext += char
        else:
            ciphertext += char + ' '
    print(ciphertext)

elif args.decrypt:
    ciphertext = args.decrypt.replace(' ','')
    decrypted = encoder.decrypt(ciphertext, alg, deck, n=26)

    plaintext = ''
    for char in decrypted:
        plaintext += char
    print(plaintext)

else:
    print('-e|--encrypt or -d|--decrypt is required')
