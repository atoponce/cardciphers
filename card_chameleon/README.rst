Card-Chameleon
==============

Card-Chameleon is a "lookup cipher". That is, each card in the deck is assigned
to an English Latin character, and the sender looks up the plaintext character
in the deck, to find its paired ciphertext character. The reverse is true for
the recipient who wishes to decrypt a message, by looking up the ciphertext
character in the deck, to find its paired plaintext character.

Chard-Chameleon uses a special ordering of suits, which are in turn assigned to
the Latin characters:

+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| Hearts and Spades                                 | Diamonds and Clubs                                |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | T | J | Q | K | A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | T | J | Q | K |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

Black cards contain plaintext characters, while the red cards contain
ciphertext characters. This is made clear in the algorithm. As such, the
plaintext character "X" is assigned to the "Jack of Clubs", while the
ciphertext "H" is assigned to the "8 of Hearts".

Card-Chameleon requires an initialization vector as part of the algorithm. The
algorithm can either use the Jokers or not. This implementation does not use
the Jokers. As such, everything is done modulo 26, and the initialization
vector must be 26 unique characters in length.
