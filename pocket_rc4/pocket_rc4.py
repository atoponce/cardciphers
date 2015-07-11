import math
import random

class Cipher(object):
    """ The full algorithm for the Pocket-RC4 playing card cipher.

    This cipher assigns the values of the deck differently from the others.
    Instead of using Bridge Order of suits, it will use the following
    assignments:

        Hearts: 1-13
        Diamonds: 14-26
        Spades: 27-39
        Clubs: 40-52
    
    Attributes:
        j (int): A running total in the RC4 algorithm
        red_values (dict): Red letters-to-values
        red_letters (dict): Red values-to-letters
        black_values (dict): Black letters-to-values
        black_letters (dict): Black values-to-letters

    """

    def __init__(self):
        """ Initialize the lookup dictionaries for the algorithm."""

        self.j = None

        self.black_values = {
            'A':27,'B':28,'C':29,'D':30,'E':31,'F':32,'G':33,
            'H':34,'I':35,'J':36,'K':37,'L':38,'M':39,
            'N':40,'O':41,'P':42,'Q':43,'R':44,'S':45,'T':46,
            'U':47,'V':48,'W':49,'X':50,'Y':51,'Z':52
        }

    def find_black_card(self, deck, letter):
        """ Find the black card in the deck matching the supplied letter
        
        Args:
            deck (list): A full 52-card deck. State is maintained.
            letter (str): One character of the message.

        Returns:
            int: Deck location of the black card letter.
            
        """

        return deck.index(self.black_values[letter])

    def prepare_deck(self, deck):
        """ Prepares the deck for strictly alternating red/black cards

        This cipher assigns the values of the deck differently from the others.
        Instead of using Bridge Order of suits, it will use the following
        assignments:

            Hearts: 1-13
            Diamonds: 14-26
            Spades: 27-39
            Clubs: 40-52

        Args:
            deck (list): A full 52-card deck. State is maintained.

        """

        black_pile = []
        red_pile = []

        for card in deck:
            if 1 <= card <= 26: # hearts through diamonds
                red_pile.insert(0, card)
            else: # spades through clubs
                black_pile.insert(0, card)

        for i in xrange(26):
            deck.insert(0, black_pile[i])
            deck.insert(0, red_pile[i])
            deck.pop(53)
            deck.pop(52)

    def shuffle_deck(self, deck):
        """ Shuffle the deck randomly with a Fisher-Yates shuffle

        Args:
            deck (list): A full 52-card deck. State is maintained.

        """

        i = 52
        while i > 1:
            i = i - 1
            j = int(math.floor(random.SystemRandom().random()*i))
            deck[j], deck[i] = deck[i], deck[j]

    def mix_deck(self, deck, location, iv=False):
        """ Swap the red card corresponding to the message with the top card

        Deck mixing happens one of two ways- using the passphrase/IV card
        swapping, or just standard encryption/decryption. If a passphrase is
        provided, the algorithm for the IV is used for mixing the deck, and
        "iv=True" must be set.

        First, the top card is always swapped with the ciphertext character
        (whether encrypting or decrypting). If "iv=True", then the ciphertext
        card and it's black pairing are appended to the bottom of the deck. The
        top two cards are always appended to the bottom of the deck at the end
        of the algorithm.

        Args:
            deck (list): A full 52-card deck. State is maintained.
            location (int): The location in the deck for IV card swapping.
            iv (bool): Mix the deck with the IV. Default: False.
        
        """

        deck[0], deck[location] = deck[location], deck[0]

        if iv:
            # append [loc, loc+1] to bottom
            deck.append(deck[location])
            deck.append(deck[location+1])
            deck.pop(location+1)
            deck.pop(location)

        deck.append(deck[0])
        deck.append(deck[1])
        deck.pop(1)
        deck.pop(0)

    def prng(self, deck, iv=False):
        """ Mix the deck with the standard algorithm, output an integer.

        Args:
            deck (list): A full 52-card deck. State is maintained.
            iv (bool): Mix the deck with the IV. Default: False

        Returns:
            char: Either the ciphertext or plaintext character.
        
        """

        black_loc = None
        red_val = None

        if self.j == None:
            self.j = deck[50] # bottom red card

        top_card = deck[0] # top red card
        self.j = (self.j + top_card) % 26

        if not self.j:
            self.j = 26

        black_loc = deck.index(self.j + 26) # 27 <= spades/clubs <= 52
        red_loc = black_loc - 1
        red_val = deck[red_loc]
        self.mix_deck(deck, red_loc, iv)
        return (red_val + top_card) % 26
