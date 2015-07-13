Chaocipher
==========

Chaocipher is a substitution cipher. That is, each card in the deck is assigned
to an English Latin character, and the sender looks up the plaintext character
in the deck, to find its paired ciphertext character. The reverse is true for
the recipient who wishes to decrypt a message, by looking up the ciphertext
character in the deck, to find its paired plaintext character.

Chaocipher uses a special ordering of suits, which are in turn assigned to
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

Chaocipher does not requires an initialization vector as part of the algorithm.
However, this implementation create a 5-character initialization vector by
default. The algorithm does not use the jokers. As such, everything is done
modulo 26.

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

Definitions
-----------

Before beginning with the encryption and decryption algorithms, we must make
some definitions clear:

Red pile
    The pile of cards comprised solely of Diamonds and Hearts. This is the
    ciphertext pile.

Black pile
    The pile of cards comprised solely of Clubs and Spades. This is the
    plaintext pile.

Zenith
    The top card in the pile.

Nadir
    The 14th card in the pile.

Overview of the Chaocipher Process
----------------------------------
Given the red and black piles, with the alphabets aligned relative to their
respective zenith positions, encrypting plaintext is as follows:

1. Determine the ciphertext character corresponding to the plaintext characer.
2. Permute the red pile.

    a) Extract the zenith + 1 card (the 2nd card).
    b) Insert this extracted card at the nadir (becomes the 14th card).

3. Permute the black pile.

    a) Move the zenith card to the bottom of the pile.
    b) Extract the new zenith + 2 card (the 3rd card).
    c) Insert this extracted card at the nadir (becomes the 14th card).

Encryption Algorithm
--------------------
In detail, the algorithm is as follows:

1. Create an initialization vector of 5 random Latin characters.
2. Pad the plaintext message with PKCS#7 padding as described above.
3. For each character in the IV and the plaintext message:

    a. Find the black card corresponding to each character. Identify this
       location as "n".
    b. Cut the black pile, such that the IV character card is at the zenith.
    c. Count to card "n" in the red pile, identifying the ciphertext character.
       Write down this ciphertext character during message encryption only.
    d. Cut the red pile, such that the ciphertext character card is at the
       zenith.
    e. Permute the red pile as described above.
    d. Permute the black pile as described above.

4. Prepend the 5-character IV to the ciphertext.
5. Send the message, which has 5 characters more than the plaintext.

Decryption Algorithm
--------------------
Given the red and black piles, with the alphabets aligned relative to their
respective zenith positions, decrypting ciphertext is as follows:

1. The first 5 characters are the initialization vector.
2. For each character in the IV:

    a. Find the black card corresponding to each character. Identify this
       location as "n".
    b. Cut the black pile, such that the IV character card is at the zenith.
    c. Count to card "n" in the red pile, identifying the ciphertext character.
    d. Cut the red pile, such that the ciphertext character card is at the
       zenith.
    e. Permute the red pile as described above.
    f. Permute the black pile as described above.

3. For each character in the ciphertext:

    a. Find the red card corresponding to the ciphertext character. Identify
       this location as "n".
    b. Cut the red pile, such that the ciphertext character card is at the
       zenith.
    c. Count to card "n" in the black pile, identifying the plaintext
       character. Write down this plaintext character.
    d. Cut the black pile, such that the plaintext character card is at the
       zenith.
    e. Permute the black pile as described above.
    f. Permute the red pile as described above.

3. Unpad the message using the PKCS#7 padding as described above.
