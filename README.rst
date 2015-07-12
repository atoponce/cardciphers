Playing Card Ciphers
====================

This repository accompanies my wiki on known playing card ciphers. The
repository can be found at http://aarontoponce.org/wiki/card-ciphers.

Each cipher is implemented in Python, and can encrypt and decrypt text via the
``crypto.py`` script. For example:

    $ ./crypto.py --encrypt 'Hello, world.'          
    XZDiO RISzb PvDmB ZPdHe

    $ ./crypto.py --decrypt 'XZDiO RISzb PvDmB ZPdHe'
    HELLO, WORLD.

Each card cipher requires a very specific deck ordering before encrypting and
decrypting text. See each specific cipher's README or on the wiki for more
information. For example, some ciphers follow the Bridge ordering of suits,
while others do not.
