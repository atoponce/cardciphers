import sys
import math
import random

class Cipher(object):
    """ The full algorithm for the Card-Chameleon playing card cipher.
    
    Attributes:
        red_values (dict): Red letters-to-values
        red_letters (dict): Red values-to-letters
        black_values (dict): Black letters-to-values
        black_letters (dict): Black values-to-letters

    """

    def __init__(self):
        """ Initialize the lookup dictionaries for the algorithm."""

        self.red_values = {
            'A':27,'B':28,'C':29,'D':30,'E':31,'F':32,'G':33,
            'H':34,'I':35,'J':36,'K':37,'L':38,'M':39,
            'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,
            'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26
        }

        self.red_letters = {
            27:'A',28:'B',29:'C',30:'D',31:'E',32:'F',33:'G',
            34:'H',35:'I',36:'J',37:'K',38:'L',39:'M',
            14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',
            21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'
        }

        self.black_values = {
            'A':40,'B':41,'C':42,'D':43,'E':44,'F':45,'G':46,
            'H':47,'I':48,'J':49,'K':50,'L':51,'M':52,
            'N': 1,'O': 2,'P': 3,'Q': 4,'R': 5,'S': 6,'T': 7,
            'U': 8,'V': 9,'W':10,'X':11,'Y':12,'Z':13
        }

        self.black_letters = {
            40:'A',41:'B',42:'C',43:'D',44:'E',45:'F',46:'G',
            47:'H',48:'I',49:'J',50:'K',51:'L',52:'M',
             1:'N', 2:'O', 3:'P', 4:'Q', 5:'R', 6:'S', 7:'T',
             8:'U', 9:'V',10:'W',11:'X',12:'Y',13:'Z'
        }

    def _find_black_card(self, deck, letter):
        """ Find the black card in the deck matching the supplied letter
        
        Args:
            deck (list): A full 52-card deck. State is maintained.
            letter (str): One character of the message.

        Returns:
            int: Deck location of the black card letter.
            
        """

        return deck.index(self.black_values[letter])

    def _find_red_card(self, deck, letter):
        """ Find the red card in the deck matching the supplied letter
        
        Args:
            deck (list): A full 52-card deck. State is maintained.
            letter (int): The integer representation of a character.

        Returns:
            int: Deck location of the red card letter.
            
        """

        return deck.index(self.red_values[letter])

    def prepare_deck(self, deck):
        """ Prepares the deck for strictly alternating red/black cards

        Args:
            deck (list): A full 52-card deck. State is maintained.

        """

        black_pile = []
        red_pile = []

        for card in deck:
            if 14 <= card <= 39: # diamonds through hearts
                red_pile.insert(0, card)
            else: # clubs and spades
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

    def prng(self, deck, letter, iv=False, method='encrypt'):
        """ Find the ciphertext or plaintext while also mixing the deck.

        Two separate algorithms are needed:

            If encrypting: find the black card first.
            If decrypting: find the red card first.

        Args:
            deck (list): A full 52-card deck. State is maintained.
            letter (char): A single character to be encrypted/decrypted.
            iv (bool): Mix the deck with the IV. Default: False
            method (str): Either method='encrypt' or method='decrypt'.

        Returns:
            char: Either the ciphertext or plaintext character.
        
        """

        b1 = None
        b2 = None
        r1 = None
        r2 = None

        if method == 'encrypt':
            b1 = self._find_black_card(deck, letter) # deck location
            r1 = deck[b1-1] # card value
            b2 = self._find_black_card(deck, self.red_letters[r1]) # deck location
            r2 = deck[b2-1] # card value
            self.mix_deck(deck, deck.index(r2), iv)
            return self.red_letters[r2]

        elif method == 'decrypt':
            r1 = self._find_red_card(deck, letter) # deck location
            b1 = deck[r1+1] # card value
            r2 = self._find_red_card(deck, self.black_letters[b1]) # deck location
            b2 = deck[r2+1] # card value
            self.mix_deck(deck, r1, iv)
            return self.black_letters[b2]
