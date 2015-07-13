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

Also, this implementation uses PKCS#7 padding as follows:

* If one padding character is required, append "V".
* If two padding characters are required, append "WW".
* If three padding characters are required, append "XXX".
* If four padding characters are required, append "YYYY".
* If no padding characters are required, append "ZZZZZ".

In this manner, it is unambiguously clear exactly what is padding and what is
plaintext. Unfortunately, this increases the message by 1-5 characters in
length. However, this also allows software algorithms to make a deterministic
choice on exactly which characters to remove from the decrypted ciphertext
without affecting the intended message.

Encryption/Decryption Algorithm
-------------------------------

1. Key the deck, either by random shuffle, or deterministic algorithm.
2. Deal out two face-up piles- a red pile and a black pile, card-for-card,
   preserving deck order. Do not place down color groups.
3. Make a new face-up pile, by interleaving the two piles, starting with the
   black pile, then the red pile. When finished, the new pile should strictly
   alternate red and black cards every card, starting with red on the top, and
   black on the bottom.
4. Create a 26-unique character initialization vector. Every letter in the
   26-character Latin alphabet must be represented exactly once. For each
   character in the IV with the following steps:

   a) Find the black card corresponding to the IV character. Identify this as
      the letter "t".
   b) Exchange the red card above this black card with the top red card.
   c) Move the black card corresponding to "t" and the red card above to the
      bottom of the deck.
   d) Move the top two cards (one red, one black) to the bottom of the deck.

5. Pad the IV + plaintext message with PKCS#7 padding as described above.
6. Set "j" to the value of the bottom red card.
7. Encrypt each letter in the plaintext with the following steps:

    a) Add the value of the top red card to "j" mod 26.
    b) Find the black card corresponding to the new "j" value.
    c) Identify the red card above this plaintext black card as "t".
    d) Add the red "t" card to the top card card mod 26.
    
       i) If encrypting, add this value to the plaintext charcter, mod 26.
       ii) If decrypting, subtract this value from the ciphertext character,
           mod 26.

    e) Exchange the red "t" card with the top red card.
    f) Move the top two cards (one red, one black) to the bottom of the deck.
