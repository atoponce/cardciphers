Pocket-RC4
==========

Pocket-RC4 is a pseudorandom number generator. That is, after each round of the
algorithm, a number is generated. This nuber is added or subtracted from the
plaintext to produce either the ciphertext or the plaintext.

Although Pocket-RC4 uses the same deck arrangement of strictly alternating
red/black pairs like Card-Chameleon, and the ordering of suits still the same,
the assignment to each card in numerical rather than a lookup table. As such,
the tables are broken down by suit below:

+---+---+---+---+---+---+---+---+---+----+----+----+----+
| Hearts                                                |
+---+---+---+---+---+---+---+---+---+----+----+----+----+
| A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | T  | J  | Q  | K  |
+---+---+---+---+---+---+---+---+---+----+----+----+----+
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
+---+---+---+---+---+---+---+---+---+----+----+----+----+

+----+----+----+----+----+----+----+----+----+----+----+----+----+
| Diamonds                                                       |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| A  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | T  | J  | Q  | K  |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
+----+----+----+----+----+----+----+----+----+----+----+----+----+

+----+----+----+----+----+----+----+----+----+----+----+----+----+
| Spades                                                         |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| A  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | T  | J  | Q  | K  |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 |
+----+----+----+----+----+----+----+----+----+----+----+----+----+

+----+----+----+----+----+----+----+----+----+----+----+----+----+
| Clubs                                                          |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| A  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | T  | J  | Q  | K  |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 |
+----+----+----+----+----+----+----+----+----+----+----+----+----+

So, technically, Hearts and Spades are still paired together like in
Card-Chameleon due to modulo 26. The same for the pairing of Diamonds and
Clubs. This is seen more clearly when permuting the deck while processing the
initialization vector, which will require either converting the Latin
characters to their numerical value, or using a lookup table.

+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| Spades                                            | Clubs                                             |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | T | J | Q | K | A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | T | J | Q | K |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

The plaintext and the ciphertext must be converted to a numerical value. Thus:

    A = 1
    B = 2
    C = 3
    ...
    X = 24
    Y = 25
    Z = 26

Pocket-RC4 requires an initialization vector as part of the algorithm. The
algorithm can either use the Jokers or not. This implementation does not use
the Jokers. As such, everything is done modulo 26, and the initialization
vector must be 26 unique characters in length.
