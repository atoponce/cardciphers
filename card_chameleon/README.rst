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

Encryption Algorithm
--------------------

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

   a) Find the black card corresponding to the IV character.
   b) Interpret the red card above this black card as letter "t".
   c) Find the black card corresponding to "t".
   d) Exchange the red card above this black card with the top red card.
   e) Move the black card corresponding to "t" and the red card above to the
      bottom of the deck.
   f) Move the top two cards (one red, one black) to the bottom of the deck.

5. Pad the IV + plaintext message with PKCS#7 padding as described above.
6. Encrypt each letter in the plaintext with the following steps:

   a) Find the black corresponding to the plaintext character.
   b) Interpret the red card above this black card as letter "t".
   c) Find the black card corresponding to "t".
   d) Interpret the red card above this black card as your ciphertext character
      and write it down.
   e) Exchange this ciphertext red card with the top red card.
   f) Move the top two cards (one red, one black) to the bottom of the deck.

7. Send the message, which has 26 character more than the plaintext.

Decryption Algorithm
--------------------

1. Key the deck, either by agreed upon random shuffle, or deterministic
   algorithm.
2. Deal out two face-up piles- a red pile and a black pile, card-for-card,
   preserving deck order. Do not place down color groups.
3. Make a new face-up pile, by interleaving the two piles, starting with the
   black pile, then the red pile. When finished, the new pile should strictly
   alternate red and black cards every card, starting with red on the top, and
   black on the bottom.
4. The first 26 characters are the initialization vector. For each character in
   the IV with the following steps (identical to the encryption algorthim):

   a) Find the black card correpsonding to the IV character.
   b) Interpret the red card above this black card as letter "t".
   c) Find the black card corresponding to "t".
   d) Exchange the red card above this black card with the top red card.
   e) Move the black card corresponding to "t" and the red card above to the
      bottom of the deck.
   f) Move the top two cards (one red, one black) to the bottom of the deck.

5. Decrypt each letter in the ciphertext with the following steps;

   a) Find the red card corresponding to the ciphertext character. Interpret
      this card as letter "c".
   b) Interpret the black card underneath the red card "C" as letter "t".
   c) Find the red card corresponding to "t".
   d) Interpret the black card below this red card as your plaintext character
      and write it down.
   e) Exchange the first red ciphertext card "c" with the top red card.
   f) Move the top two cards (one red, one black) to the bottom of the deck.

6. Unpad the message using the PKCS#7 padding as described above.
