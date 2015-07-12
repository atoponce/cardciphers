Solitaire
=========

Solitaire is a pseudorandom number generator. That is, after each round of the
algorithm, a number is generated. This nuber is added or subtracted from the
plaintext to produce either the ciphertext or the plaintext.

Solitaire uses the Bridge ordering of suits. In Contact Bridge, Clubs are
ranked lowest, followed by Diamonds, then Hearts, with Spades ranked highest.
As such, Solitaire uses the following card assignments:

    Clubs: Face value (Ace=1, King=13)
    Diamonds: Face value + 13
    Hearts: Face value + 26
    Spades: Face value + 39
    Jokers: Value of 53

Or, if you wanted to see them broken down into tables:

+---+---+---+---+---+---+---+---+---+----+----+----+----+
| Clubs                                                 |
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
| Hearts                                                         |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| A  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | T  | J  | Q  | K  |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 |
+----+----+----+----+----+----+----+----+----+----+----+----+----+

+----+----+----+----+----+----+----+----+----+----+----+----+----+
| Spades                                                         |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| A  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | T  | J  | Q  | K  |
+----+----+----+----+----+----+----+----+----+----+----+----+----+
| 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 |
+----+----+----+----+----+----+----+----+----+----+----+----+----+

+----+----+
| Jokers  |
+----+----+
| A  | B  |
+----+----+
| 53 | 53 |
+----+----+

Bruce Schneier did not mention anything of an initialization vector as part of
the algorithm. As such, this implementation uses a 5-character initialization
vector to add entropy to the deck order before encryption/decryption. This can
be disabled, if you want to use this to interact with other implementations.

Also, this implementation uses PKCS#7 padding, which Bruce Schneier sort of
addressed. Bruce mentions padding the plaintext message with "X" until the
length of the message is a multiple of five characters. However, PKCS#7 offers
an improved padding scheme:

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
